import os
from azure.storage.blob import BlobClient, BlobServiceClient

def get_blob_client(container: str, blob_name: str) -> BlobClient:
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set up as envirorment variables")
    bsc = BlobServiceClient.from_connection_string(conn_str)
    return bsc.get_blob_client(container=container,blob=blob_name)