import os
import zipfile
import tempfile
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

class GCSBucket:
    def __init__(self, bucket_name: str = "hc-bucket-404notfound"):
        """Initialize the GCSBucket object with the specified bucket name."""
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def download_file(self, source_blob_name: str, destination_file_name: str) -> None:
        """
        Download a file from the Google Cloud Storage bucket.
        
        :param source_blob_name: The name of the file in the bucket.
        :param destination_file_name: The local file path to save the downloaded file.
        """
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            print(f"Downloaded {source_blob_name} to {destination_file_name}.")
        except GoogleAPIError as e:
            print(f"Error downloading file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def upload_file(self, source_file_name: str, destination_blob_name: str) -> None:
        """
        Upload a file to the Google Cloud Storage bucket.
        
        :param source_file_name: The local file path to upload.
        :param destination_blob_name: The name of the file in the bucket.
        """
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            print(f"Uploaded {source_file_name} to {destination_blob_name}.")
        except GoogleAPIError as e:
            print(f"Error uploading file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_file(self, blob_name: str) -> None:
        """
        Delete a file from the Google Cloud Storage bucket.
        
        :param blob_name: The name of the file to delete from the bucket.
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            print(f"Deleted {blob_name} from the bucket {self.bucket_name}.")
        except GoogleAPIError as e:
            print(f"Error deleting file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
