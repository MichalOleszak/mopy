import os
import subprocess

from utils.aws.s3_client import S3FSClient
import config


DATA_VALIDATION_DIRPATHS = config.S3_DATA_VALIDATION_DIRPATH


def fetch_validation_results_from_s3():
    fs = S3FSClient()
    for dp in DATA_VALIDATION_DIRPATHS:
        for path, _, file in fs.walk(dp):
            if file and file[0].endswith(".json"):
                local_destination_path = os.path.join(
                    config.GREAT_EXPECTATIONS_VALIDATIONS_DIRPATH,
                    path.split(config.S3_DATA_VALIDATION_DIRPATH.split("/")[-1])[-1][1:],
                    file[0],
                )
                fs.get(os.path.join(path, file[0]), local_destination_path)


def build_data_docs():
    fetch_validation_results_from_s3()
    subprocess.run(["great_expectations", "--assume-yes", "docs", "build"])


if __name__ == "__main__":
    build_data_docs()
