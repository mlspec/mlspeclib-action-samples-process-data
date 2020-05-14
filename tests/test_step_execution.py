import os
import logging
from pathlib import Path
import yaml as YAML
import uuid
import sys
from mlspeclib import MLSchema
import unittest

sys.path.append(str(Path.cwd().parent))

from step_execution import StepExecution
from utils import verify_result_contract

def StepExecutionTester(unittest):

    def setUp(self):
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stdout_handler.setFormatter(formatter)
        rootLogger.addHandler(stdout_handler)

    def test_e2e(self):
        MLSchema.populate_registry()
        MLSchema.append_schema_to_registry(Path.cwd().parent / '.parameters' / 'schemas')

        # Execute step
        input_parameters = {
            # Put sample required input parameters here
        }

        execution_parameters = {
            # Put sample required execution parameters here
        }

        expected_results_schema_type = 'datapath' # MUST BE A LOADED SCHEMA
        expected_results_schema_version = '0.0.1' # MUST BE A SEMVER

        step_execution_object = StepExecution(input_parameters, execution_parameters)

        results_object = step_execution_object.execute(result_object_schema_type=expected_results_schema_type, result_object_schema_version=expected_results_schema_version)

        verify_result_contract(results_object, expected_results_schema_type, expected_results_schema_version, "SAMPLESTEPNAME")

if __name__ == "__main__":
    main()
