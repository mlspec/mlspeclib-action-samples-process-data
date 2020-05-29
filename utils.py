import logging
from mlspeclib import MLObject
import sys
from io import StringIO
import os


class ConfigurationException(Exception):
    pass


def report_found_params(expected_params: list, offered_params: dict) -> None:
    for param in expected_params:
        if param not in offered_params or offered_params[param] is None:
            raise ValueError(f"No parameter set for {param}.")
        else:
            logging.debug(f"Found value for {param}.")


def verify_result_contract(
    result_object: MLObject,
    expected_schema_type,
    expected_schema_version,
    step_name: str,
):
    """ Creates an MLObject based on an input string, and validates it against the workflow object
    and step_name provided.

    Will fail if the .validate() fails on the object or the schema mismatches what is seen in the
    workflow.
    """
    rootLogger = setupLogger().get_root_logger()

    (contract_object, errors) = MLObject.create_object_from_string(
        result_object.dict_without_internal_variables()
    )

    if errors is not None and len(errors) > 0:
        error_string = (
            f"Error verifying result object for '{step_name}.output': {errors}"
        )
        rootLogger.debug(error_string)
        raise ValueError(error_string)

    if (contract_object.schema_type != expected_schema_type) or (
        contract_object.schema_version != expected_schema_version
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


class setupLogger:
    _rootLogger = None
    _buffer = None

    def __init__(self):
        # logging.config.fileConfig('logging.conf')

        # return (logger, None)
        self._rootLogger = logging.getLogger()
        self._rootLogger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("::%(levelname)s - %(message)s")

        if not self._rootLogger.hasHandlers():
            self._buffer = StringIO()
            bufferHandler = logging.StreamHandler(self._buffer)
            bufferHandler.setLevel(logging.DEBUG)
            bufferHandler.setFormatter(formatter)
            bufferHandler.set_name("buffer.logger")
            self._rootLogger.addHandler(bufferHandler)

            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.setFormatter(formatter)
            stdout_handler.set_name("stdout.logger")
            self._rootLogger.addHandler(stdout_handler)
        else:
            for i, handler in enumerate(self._rootLogger.handlers):
                if handler.name == "buffer.logger":
                    self._buffer = self._rootLogger.handlers[i].stream
                    break

            if self._buffer is None:
                raise SystemError(
                    "Somehow, we've lost the 'buffer' logger, meaning nothing will be printed. Exiting now."
                )

    def get_loggers(self):
        return (self._rootLogger, self._buffer)

    def get_root_logger(self):
        return self._rootLogger

    def get_buffer(self):
        return self._buffer

    @staticmethod
    def print_and_log(variable_name, variable_value):
        logger = setupLogger()
        rootLogger = logger.get_root_logger()
        # echo "::set-output name=time::$time"
        output_message = f"::set-output name={variable_name}::{variable_value}"
        print(output_message)
        rootLogger.debug(output_message)

        os.environ[variable_name] = variable_value
