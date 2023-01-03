import glob
import json
import os
from pathlib import Path
import tempfile

import pandas as pd
from google.cloud import storage
from PIL import Image
import torch

from mopy.utils.log import logger


class StorageClient:
    """
    Google Cloud Storage client with ready-made methods for loading and saving data, plus other utils

    Usage example:
        # setup client
        storage_client = StorageClient()

        # list all files in the data/processed directory
        storage_client.ls_recursive("data")

        # load a jpg image from Storage
        img = storage_client.read_image_to_pil('data/image.jpg')

        # save the image back to a different location
        storage_client.write_image(img, 'data/new_image.jpg')
    """

    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def ls_recursive(self, path=None):
        """
        List all the blobs in the project bucket that begin with the specified prefix.
        """
        blobs = self.client.list_blobs(self.bucket_name, prefix=path)
        return [blob.name for blob in blobs]

    def exists(self, filepath):
        """
        Return True if filepath exists on Storage, false otherwise.
        """
        return storage.Blob(bucket=self.bucket, name=filepath).exists(client=self.client)

    def read_image_to_pil(self, filepath):
        """
        Load an image file from Storage to a PIL Image.
        :param filepath: str, e.g. 'data/image.jpg'
        """
        with tempfile.TemporaryFile() as fp:
            gs_filepath = f"gs://{self.bucket_name}/{filepath}"
            self.client.download_blob_to_file(gs_filepath, fp)
            img = Image.open(fp)
            img.load()
        return img

    def write_image(self, img, filepath, force_overwrite=True):
        """
        Save a PIL Image on Storage.
        :param img: PIL Image
        :param filepath: destination filepath including extension, e.g. 'data/image.jpg'
        :param force_overwrite: if True, existing file on Storage will be overwritten
        """
        destination_exists = self.exists(filepath)
        if destination_exists and not force_overwrite:
            logger.error(f"Destination {filepath} exists on Storage. Set `force_overwrite=True` to overwrite it.")
            raise Exception(f"destination {filepath} exists")
        else:
            if destination_exists and force_overwrite:
                logger.info(f"Overwriting an existing file: {filepath}")
            blob = self.bucket.blob(filepath)
            extension = Path(filepath).suffix
            with tempfile.TemporaryDirectory() as dp:
                temp_filepath = os.path.join(dp, f"myfile{extension}")
                img.save(temp_filepath)
                blob.upload_from_filename(temp_filepath)

    def load_json_to_dict(self, filepath):
        """
        Load a json file from Storage to a dictionary
        :param filepath: str, e.g. 'data/my_json.json'
        """
        blob = self.bucket.blob(filepath)
        return json.loads(blob.download_as_string())

    def save_dict_to_json(self, dic, filepath):
        """
        Save a dictionary to a JSON file on Storage
        :param dic: dict to save
        :param filepath: str, e.g. 'data/my_json.json'
        """
        blob = self.bucket.blob(filepath)
        with tempfile.TemporaryDirectory() as dp:
            temp_filepath = os.path.join(dp, "tempfile.json")
            with open(temp_filepath, "w") as f:
                json.dump(dic, f)
            blob.upload_from_filename(temp_filepath)

    def load_torch_model(self, filepath, map_location=None):
        """
        Load a torch model from a .pt or .pth file to its proper model class, e.g. torchvision.models.resnet.ResNet
        :param filepath: str, e.g. 'models/model.pt'
        """
        with tempfile.NamedTemporaryFile() as fp:
            blob = self.bucket.blob(filepath)
            blob.download_to_filename(fp.name)
            model = torch.load(fp, map_location=map_location)
        return model

    def load_excel(self, filepath):
        """
        Load an excel file to the DataFrame.
        :param filepath: a path to the excel file
        """
        with tempfile.NamedTemporaryFile() as fp:
            blob = self.bucket.blob(filepath)
            blob.download_to_filename(fp.name)
            df = pd.read_excel(fp)
        return df

    def load_csv(self, filepath):
        """
        Load an CSV file to a pd.DataFrame.
        :param filepath: a path to the CSV file
        """
        with tempfile.NamedTemporaryFile() as fp:
            blob = self.bucket.blob(filepath)
            blob.download_to_filename(fp.name)
            df = pd.read_csv(fp)
        return df

    def save_torch_model(self, model, filepath, force_overwrite=False):
        """
        Save a torch model to a .pt or .pth file to its proper model class, e.g. torchvision.models.resnet.ResNet
        :param model: A PyTorch model
        :param filepath: str, e.g. 'models/model.pt'
        :param force_overwrite: if True, existing file on Storage will be overwritten
        """
        destination_exists = self.exists(filepath)
        if destination_exists and not force_overwrite:
            logger.error(f"Destination {filepath} exists on Storage. Set `force_overwrite=True` to overwrite it.")
            raise Exception(f"destination {filepath} exists")
        else:
            if destination_exists and force_overwrite:
                logger.info(f"Overwriting an existing file: {filepath}")
            blob = self.bucket.blob(filepath)
            extension = Path(filepath).suffix
            with tempfile.TemporaryDirectory() as dp:
                temp_filepath = os.path.join(dp, f"myfile{extension}")
                torch.save(model, temp_filepath)
                blob.upload_from_filename(temp_filepath)

    def save_df(self, df, filepath, force_overwrite=False):
        """
        Save pandas DataFrame into Storage.
        :param df: A pd.DataFrame
        :param filepath: str
        :param force_overwrite: if True, existing file on Storage will be overwritten
        """
        destination_exists = self.exists(filepath)
        if destination_exists and not force_overwrite:
            logger.error(f"Destination {filepath} exists on Storage. Set `force_overwrite=True` to overwrite it.")
            raise Exception(f"destination {filepath} exists")
        else:
            if destination_exists and force_overwrite:
                logger.info(f"Overwriting an existing file: {filepath}")
            blob = self.bucket.blob(filepath)
            extension = Path(filepath).suffix
            with tempfile.TemporaryDirectory() as dp:
                temp_filepath = os.path.join(dp, f"myfile{extension}")
                df.to_excel(temp_filepath, index=False)
                blob.upload_from_filename(temp_filepath)

    def read_df(self, filepath):
        """
        Read pandas DataFrame from Storage.
        :param filepath: str
        """
        with tempfile.NamedTemporaryFile() as fp:
            blob = self.bucket.blob(filepath)
            blob.download_to_filename(fp.name)
            df = pd.read_excel(fp)
        return df

    def upload_file(self, filepath, force_overwrite=False):
        """
        Upload a file to the Storage.
        :param filepath: str, e.g. 'models/model.pt'
        :param force_overwrite: if True, existing file on Storage will be overwritten
        """
        destination_exists = self.exists(filepath)
        if destination_exists and not force_overwrite:
            logger.error(f"Destination {filepath} exists on Storage. Set `force_overwrite=True` to overwrite it.")
            raise Exception(f"destination {filepath} exists")
        else:
            if destination_exists and force_overwrite:
                logger.info(f"Overwriting an existing file: {filepath}")
            blob = self.bucket.blob(filepath)
            blob.upload_from_filename(filepath)

    def upload_folder(self, folder_dir):
        """
        Upload a whole folder to the GCP.

        :param folder_dir: Directory to the folder to upload.
        :return:
        """
        rel_paths = glob.glob(os.path.join(folder_dir, "**"), recursive=True)
        for file_path in rel_paths:
            if os.path.isfile(file_path):
                self.upload_file(file_path)
