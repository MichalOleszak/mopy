import json
import joblib
import os

import pandas as pd
import s3fs

import constants


class S3FSClient:
    """
    AWS S3 filesystem with ready-made methods for dumping, loading and deleting data
    """
    def __init__(self):
        self.fs = s3fs.S3FileSystem(
            key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config_kwargs={"region_name": os.getenv("AWS_REGION")}
        )

    def ls(self, path):
        return self.fs.ls(path)

    def rm(self, path):
        if path.endswith("prod"):
            raise PermissionError(
                f"Permission denied, this filesystem does not allow for removing files "
                f"from production buckets (with suffix 'prod')"
            )
        if not path.startswith(constants.S3_BUCKET):
            raise PermissionError(
                f"Permission denied, this filesystem only allows for removing files "
                f"from the following bucket: '{constants.S3_BUCKET}'"
            )
        else:
            self.fs.rm(path)

    def dump_df_to_zipped_csv(self, df, filepath):
        with self.fs.open(filepath, "wb") as f:
            df.to_csv(f, index=False, compression="gzip")

    def load_zipped_csv_to_df(self, filepath):
        with self.fs.open(filepath, "rb") as f:
            return pd.read_csv(f, compression="gzip")

    def dump_object_to_pickle(self, obj, filepath):
        with self.fs.open(filepath, "wb") as f:
            joblib.dump(obj, f)

    def load_object_from_pickle(self, filepath):
        with self.fs.open(filepath, "rb") as f:
            return joblib.load(f)

    def dump_dict_to_json(self, d, filepath):
        with self.fs.open(filepath, "w") as f:
            json.dump(d, f)

    def load_json_to_dict(self, filepath):
        with self.fs.open(filepath, "r") as f:
            return json.load(f)

