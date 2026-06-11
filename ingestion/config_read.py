
import os
import yaml
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime, timezone
from google.cloud import storage
storage_client = storage.Client()

# BEST PRACTICE: Use a relative path so your code works on any computer (or in the cloud),
# not just on your personal local C: drive.
CONFIG_PATH =  r"C:\Users\avi72\retailer360-data-engineer-project\ingestion\config.yml"
storage_client = storage.Client()

def yaml_load(path=CONFIG_PATH):
    if not os.path.exists(path):
        print(f"path = {path} not exist")

    with open(path,"r",encoding="utf-8") as file:
      return yaml.safe_load(file)
def read_gcs_file_to_dataframe(file_path: str, config_file: dict) -> pd.DataFrame:
    """
    Read a single file from GCS into a DataFrame.
    Detects file type automatically from extension.
    """
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".csv":
        return read_csv_file(file_path, config_file)
    elif file_ext == ".json":
        return read_json_file(file_path, config_file)
    elif file_ext in [".xls", ".xlsx"]:
        return read_excel_file(file_path, config_file)
    elif file_ext == ".parquet":
        return read_parquet_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def read_csv_file(file_path: str, config_file: dict) -> pd.DataFrame:
    delimiter = config_file.get("delimiter", ",")
    header = 0 if config_file.get("header", True) else None
    return pd.read_csv(file_path, delimiter=delimiter, header=header, dtype=str)


def read_json_file(file_path: str, config_file: dict) -> pd.DataFrame:
    try:
        return pd.read_json(file_path, dtype=str, lines=True)
    except ValueError:
        return pd.read_json(file_path, dtype=str)


def read_excel_file(file_path: str, config_file: dict) -> pd.DataFrame:
    sheet_name = config_file.get("sheet_name")
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")


def read_parquet_file(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)


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
 



if __name__ == "__main__":
    print("--- Starting Local Test ---")

    try:
        print("Loading config file")
        config = yaml_load(CONFIG_PATH)
        print("Config file loaded successfully")

        sources = config["sources"]

        for source_name, source_config in sources.items():
            if not source_config.get("enabled", False):
                print(f"Skipping {source_name} (disabled)")
                continue

            source_dir = Path(source_config["source_path"])
            pattern = source_config.get("file_pattern", "*")
            load_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            print(f"\n--- Reading {source_name} from {source_dir} ({source_config['file_type']}) ---")

            # Find all files in the landing folder
            files = list(source_dir.glob(pattern))
            if not files:
                print(f"❌ No files found for {source_name} with pattern {pattern}")
                continue

            # Copy each file to raw and read it
            for f in files:
                try:
                    raw_file_new = copy_file_to_raw(f, source_config, load_date)
                    print(f"Copied {f} → {raw_file_new}")

                    df = read_all_file_to_dataframe(raw_file_new, source_config)
                    if df is None:
                        print(f"❌ Could not load {source_name} from {raw_file_new}")
                        continue

                    print(f"{source_name} loaded successfully from {raw_file_new} with {len(df)} rows")
                    print("\n--- Success! Here is your data ---")
                    print(df.head())
                except Exception as e:
                    print(f"Failed to load {source_name} from {f}: {e}")

    except Exception as e:
        print(f"Pipeline failed: {e}")











