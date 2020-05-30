import os
import logging
from pathlib import Path
import yaml as YAML
import uuid
import sys
import datetime
from mlspeclib import MLObject, MLSchema
import unittest

sys.path.append(str(Path.cwd().parent))

from step_execution import StepExecution
from utils.utils import verify_result_contract, setupLogger


class StepExecutionTester(unittest.TestCase):
    _buffer = ""
    rootLogger = None

    def setUp(self):
        (self.rootLogger, self._buffer) = setupLogger().get_loggers()

    def test_e2e(self):
        MLSchema.populate_registry()
        MLSchema.append_schema_to_registry(Path.cwd() / ".parameters" / "schemas")

        # Execute step
        input_parameters = {
            # Put sample required input parameters here
        }

        execution_parameters = {
            # Put sample required execution parameters here
        }

        # THESE SHOULD BE THE ONLY SETTINGS FOR THIS FILE
        step_name = "process_data"
        expected_results_schema_type = "data_result"  # MUST BE A LOADED SCHEMA
        expected_results_schema_version = "500.0.1"  # MUST BE A SEMVER

        step_execution_object = StepExecution(input_parameters, execution_parameters)

        results_object = MLObject()
        results_object.set_type(
            schema_type=expected_results_schema_type,
            schema_version=expected_results_schema_version,
        )

        # Should error due to missing fields
        with self.assertRaises(ValueError) as context:
            verify_result_contract(
                results_object,
                expected_results_schema_type,
                expected_results_schema_version,
                step_name,
            )

        self.assertTrue(
            f"Error verifying result object for '{step_name}.output'"
            in str(context.exception)
        )

        results_object = step_execution_object.execute(
            result_object_schema_type=expected_results_schema_type,
            result_object_schema_version=expected_results_schema_version,
        )

        results_object.run_date = datetime.datetime.now()
        results_object.step_id = uuid.uuid4()
        results_object.run_id = uuid.uuid4()

        self.assertTrue(verify_result_contract(
            results_object,
            expected_results_schema_type,
            expected_results_schema_version,
            step_name))


if __name__ == "__main__":
    unittest.main()
