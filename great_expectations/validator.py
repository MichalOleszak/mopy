import os

import great_expectations as ge

from utils.aws.s3_client import S3FSClient
import config
from utils.log import logger


def validate_data(df):
    logger.info(f"Validating data against expectation suite: {config.EXPECTATION_SUITE_NAME}")
    context = ge.get_context()
    checkpoint_config = {
        "name": "***",
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "run_name_template": "%Y%m%d-%H%M%S",
        "validations": [
            {
                "batch_request": {
                    "datasource_name": "***",
                    "data_connector_name": "default_runtime_data_connector_name",
                    "data_asset_name": "***",
                },
                "expectation_suite_name": config.EXPECTATION_SUITE_NAME,
            }
        ],
    }
    context.add_checkpoint(**checkpoint_config)
    validation_results = context.run_checkpoint(
        checkpoint_name="***",
        batch_request={
            "runtime_parameters": {"batch_data": df},
            "batch_identifiers": {"default_identifier_name": "***"},
        },
    )
    return validation_results


def upload_validation_results_to_s3(local_results_dirpath, dirname):
    fs = S3FSClient()
    destination_dirpath = os.path.join(
        config.DATA_VALIDATION_DIRPATH,
        config.EXPECTATION_SUITE_NAME,
        dirname,
    )
    logger.info(f"Uploading validation results to S3: {os.path.join(destination_dirpath, dirname)}")
    fs.put(local_results_dirpath, destination_dirpath, recursive=True)


def run_data_validation(df):
    validation_results = validate_data(df)
    local_results_dirpath = os.path.join(
        config.GREAT_EXPECTATIONS_VALIDATIONS_DIRPATH,
        config.EXPECTATION_SUITE_NAME,
        validation_results["_run_id"].run_name,
    )
    upload_validation_results_to_s3(local_results_dirpath, validation_results["_run_id"].run_name)
