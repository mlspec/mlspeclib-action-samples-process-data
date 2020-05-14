import logging
from mlspeclib import MLObject
import sys
from io import StringIO

class ConfigurationException(Exception):
    pass


def report_found_params(expected_params: list, offered_params: dict) -> None:
    for param in expected_params:
        if param not in offered_params or offered_params[param] is None:
            raise ValueError(f"No parameter set for {param}.")
        else:
            logging.debug(f"Found value for {param}.")


def verify_result_contract(result_object: MLObject, expected_schema_type, expected_schema_version, step_name: str):
    """ Creates an MLObject based on an input string, and validates it against the workflow object
    and step_name provided.

    Will fail if the .validate() fails on the object or the schema mismatches what is seen in the
    workflow.
    """
    rootLogger = logging.getLogger()

    (contract_object, errors) = MLObject.create_object_from_string(result_object.dict_without_internal_variables())

    if errors is not None and len(errors) > 0:
        error_string = f"Error verifying result object for '{step_name}.output': {errors}"
        rootLogger.debug(error_string)
        raise ValueError(error_string)

    if (
        contract_object.schema_type
        != expected_schema_type
    ) or (
        contract_object.schema_version
        != expected_schema_version
    ):
        error_string = f"""Actual data does not match the expected schema and version:
    Expected Type: {expected_schema_type}
    Actual Type: {contract_object.schema_type}

    Expected Version: {expected_schema_version}
    Actual Version: {contract_object.schema_version}")"""
        rootLogger.debug(error_string)
        raise ValueError(error_string)

    rootLogger.debug(
        f"Successfully loaded and validated contract object: {contract_object.schema_type} on step {step_name}.output"
    )

    return True

def setupLogger():
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s\n"
    )

    buffer = StringIO()
    bufferHandler = logging.StreamHandler(buffer)
    bufferHandler.setLevel(logging.DEBUG)
    bufferHandler.setFormatter(formatter)
    rootLogger.addHandler(bufferHandler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    rootLogger.addHandler(stdout_handler)

    return (rootLogger, buffer)
