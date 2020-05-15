import os
import sys
import logging
from pathlib import Path
import yaml as YAML
import uuid
import datetime
from mlspeclib import MLObject, MLSchema, Metastore
import random
import unittest
import subprocess

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / "bin"))

from utils import setupLogger  # noqa


class E2ETester(unittest.TestCase):
    def setUp(self):
        (self.rootLogger, self._buffer) = setupLogger()
        self.rootLogger.setLevel(logging.DEBUG)

    def test_e2e(self):
        parameters_from_environment = {}

        for var in os.environ:
            if "INPUT" in var:
                parameters_from_environment[var] = os.environ.get(var, default=None)

        integration_tests_dir = parameters_from_environment.get("INPUT_integration_tests_directory", "integration")
        parameters_dir_name = parameters_from_environment.get("INPUT_parameters_directory", ".parameters")
        variables_file_name = parameters_from_environment.get("INPUT_integration_tests_variable_file_name", "integration_test_variables.yaml")
        schemas_dir_name = parameters_from_environment.get("INPUT_integration_tests_schemas_dir_name", "schemas")
        container_name = parameters_from_environment.get("INPUT_container_name", "mlspeclib-action-sample-process-data")

        parameters_from_file = YAML.safe_load((Path(integration_tests_dir) / variables_file_name).read_text('utf-8'))

        parameters = {**parameters_from_environment, **parameters_from_file}

        MLSchema.append_schema_to_registry(Path.cwd() / integration_tests_dir / parameters_dir_name / schemas_dir_name)

        workflow_dict = YAML.safe_load(YAML.safe_dump(parameters.get("INPUT_workflow")))
        workflow_version = str('999999999999.9.' + str(random.randint(0, 9999)))
        workflow_dict["workflow_version"] = workflow_version
        workflow_dict["run_id"] = str(uuid.uuid4())
        workflow_dict["step_id"] = str(uuid.uuid4())
        workflow_dict["run_date"] = datetime.datetime.now()

        workflow_string = YAML.safe_dump(workflow_dict)
        (workflow_object, errors) = MLObject.create_object_from_string(workflow_string)

        workflow_partition_id = uuid.uuid4()

        credentials = parameters_from_environment.get("INPUT_METASTORECREDENTIALS", None)
        if credentials is None:
            credential_string = (Path(integration_tests_dir) / "metastore_credentials.yaml").read_text(encoding="utf-8")
            credentials = YAML.safe_load(credential_string)

        ms = Metastore(credentials)
        step_name = list(workflow_object.steps.keys())[0]
        environment_vars = ""
        environment_vars_list = []

        try:
            ms.empty_graph()
            workflow_node_id = ms.create_workflow_node(workflow_object, workflow_dict["run_id"])
            ms.create_workflow_steps(workflow_node_id, workflow_object)
            workflow_node = ms.get_workflow_object(workflow_node_id)

            for param in parameters:
                if isinstance(parameters[param], dict):
                    env_value = YAML.safe_dump(parameters[param])
                else:
                    env_value = parameters[param]
                environment_vars += f' -e "{param}={env_value}"'
                environment_vars_list.append('-e')
                environment_vars_list.append(f"{param}={env_value}")

            exec_statement = ["docker", "run"] + environment_vars_list + [f"{container_name}:latest"]

            print(f"exec statement: '{exec_statement}'")
            self.rootLogger.debug(f"exec_statement = {exec_statement}")

            p = subprocess.Popen(
                exec_statement, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            out, err = p.communicate()
            self.rootLogger.debug(f"out = {str(out)}")
            self.rootLogger.debug(f"error = {str(err)}")
            self.assertTrue("ConfigurationException" in str(err))

        finally:
            pass


if __name__ == "__main__":
    unittest.main()
