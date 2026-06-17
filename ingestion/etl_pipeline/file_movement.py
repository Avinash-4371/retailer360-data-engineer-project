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


def copy_file_to_archive(raw_file_path: str, config_file: dict, load_date: str) -> str:
    """
    Copy a file from RAW GCS path into archive bucket, under a date folder.
    """
    # Parse RAW bucket + blob
    raw_bucket_name, raw_blob_name = raw_file_path.replace("gs://", "").split("/", 1)
    raw_blob_name = raw_blob_name.rstrip("/")  # Remove leading slash if present
    raw_bucket = storage_client.bucket(raw_bucket_name)
    raw_blob = raw_bucket.blob(raw_blob_name)

    # Parse destination bucket + prefix
    archive_path = config_file["archive_path"]  # e.g. "gs://retailer360-data/archive/inventory/"
    dest_bucket_name, dest_prefix = archive_path.replace("gs://", "").split("/", 1)
    dest_bucket = storage_client.bucket(dest_bucket_name)

    # Build destination blob name with date folder + timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = Path(raw_file_path).name
    dest_blob_name = f"{dest_prefix}/{load_date}/{file_name}_{timestamp}"

    # Copy blob from RAW → ARCHIVE
    raw_bucket.copy_blob(raw_blob, dest_bucket, dest_blob_name)

    # Optional: delete from RAW after archiving

    return f"gs://{dest_bucket_name}/{dest_blob_name}"

