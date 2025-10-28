from azure.storage.blob import BlobClient, BlobServiceClient
from utils.blob_client import get_blob_client

def load_bytes(container: str, blob_name: str)->bytes:
    blob_client = get_blob_client(container, blob_name)
    stream = blob_client.download_blob()
    return stream.readall()