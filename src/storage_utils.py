from datetime import datetime, timezone
from pathlib import Path
from google.cloud import storage

storage_client = storage.Client()

def copy_file_to_raw(blob, config_file: dict, run_folder: str) -> str:
    """
    Copy a single file from landing GCS folder to the given run-specific raw folder.
    Returns the raw URI of the copied file.
    """
    raw_path = config_file["raw_path"]  # e.g. "gs://retailer360-data/raw/orders"
    dest_bucket_name, dest_prefix = raw_path.replace("gs://", "").split("/", 1)
    dest_bucket = storage_client.bucket(dest_bucket_name)

    file_name = Path(blob.name).name
    dest_blob_name = f"{run_folder}/{file_name}"

    # Copy from landing → raw
    src_bucket = blob.bucket
    src_bucket.copy_blob(blob, dest_bucket, dest_blob_name)

    # Optional: delete from landing after successful copy
   # blob.delete()

    return f"gs://{dest_bucket_name}/{dest_blob_name}"


def copy_file_to_target(source_path_uri: str, target_path: str, load_date: str):

    src_bucket_name,src_blob_name=source_path_uri.replace("gs://", "").split("/", 1)
    src_bucket=storage_client.bucket(src_bucket_name)
    src_blob = src_bucket.blob(src_blob_name)

    dest_bucket_name,dest_blob_name = target_path.replace("gs://", "").split("/", 1)
    dest_bucket=storage_client.bucket(dest_bucket_name)
    

    file_name = Path(src_blob.name).name

    dest_blob = f"{dest_blob_name}/{load_date}/{file_name}"

    src_bucket.copy_blob(src_blob,dest_bucket,dest_blob)

    return f"gs://{dest_bucket_name}/{dest_blob}"