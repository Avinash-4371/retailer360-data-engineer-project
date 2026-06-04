from datetime import datetime, timezone
from pathlib import Path
from google.cloud import storage

storage_client = storage.Client()

def copy_files_to_raw(source_path: str, config_file: dict) -> list[str]:
    """
    Copy all files from a source GCS folder to a raw GCS folder.
    """
    # Parse source bucket + prefix
    src_bucket_name, src_prefix = source_path.replace("gs://", "").split("/", 1)
    src_bucket = storage_client.bucket(src_bucket_name)

    # Parse destination bucket + prefix
    raw_path = config_file["raw_path"]  # e.g. "gs://retailer360-data/raw/inventory/"
    dest_bucket_name, dest_prefix = raw_path.replace("gs://", "").split("/", 1)
    dest_bucket = storage_client.bucket(dest_bucket_name)

    copied_files = []

    # List all blobs under source prefix
    for blob in src_bucket.list_blobs(prefix=src_prefix):
        file_name = Path(blob.name).name   # actual file name
        dest_blob_name = f"{dest_prefix}/{file_name}"

        src_bucket.copy_blob(blob, dest_bucket, dest_blob_name)
        copied_files.append(f"gs://{dest_bucket_name}/{dest_blob_name}")

    return copied_files



def copy_file_to_archive(file_path: str, config_file: dict, load_date: str) -> str:
    """
    Copy a file from source GCS path into archive bucket, under a date folder.
    """
    # Parse source bucket + blob
    src_bucket_name, src_blob_name = file_path.replace("gs://", "").split("/", 1)
    src_bucket = storage_client.bucket(src_bucket_name)
    src_blob = src_bucket.blob(src_blob_name)

    # Parse destination bucket + prefix
    archive_path = config_file["archive_path"]  # e.g. "gs://retailer360-data/archive/inventory/"
    dest_bucket_name, dest_prefix = archive_path.replace("gs://", "").split("/", 1)
    dest_bucket = storage_client.bucket(dest_bucket_name)

    # Build destination blob name with date folder + timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = Path(file_path).name
    dest_blob_name = f"{dest_prefix}/{load_date}/{file_name}_{timestamp}"

    # Copy blob into archive bucket
    src_bucket.copy_blob(src_blob, dest_bucket, dest_blob_name)

    return f"gs://{dest_bucket_name}/{dest_blob_name}"
