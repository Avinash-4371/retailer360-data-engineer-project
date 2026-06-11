from datetime import datetime, timezone
from pathlib import Path
from google.cloud import storage
import yaml

from file_read import read_gcs_file_to_dataframe
from bq_load import load_to_bigquery
from metadata_colums import add_metadata_columns, convert_all_columns_to_string


from validate_schema import validate_schema
from file_movement import copy_file_to_archive, copy_file_to_raw

storage_client = storage.Client()

def process_source(source_name,source_config):
    results=[]
        # Create run folder once per pipeline run
    run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    raw_path = source_config["raw_path"]
    _, raw_prefix = raw_path.replace("gs://", "").split("/", 1)
    run_folder = f"{raw_prefix}/run_{run_id}"

    # List landing files
    src_bucket_name, src_prefix = source_config["source_path"].replace("gs://", "").split("/", 1)
    landing_bucket = storage_client.bucket(src_bucket_name)
    blobs = landing_bucket.list_blobs(prefix=src_prefix)

    for blob in blobs:
        file_name = Path(blob.name).name
        target_table = source_config["target_table"]

        try:
            # Copy single file → raw
            raw_uri = copy_file_to_raw(blob, source_config, run_folder)

            df=read_gcs_file_to_dataframe(raw_uri,source_config)
            df=convert_all_columns_to_string(df)
            df=add_metadata_columns(df,source_name)
            # Schema validation
            schema_result = validate_schema(df.columns.tolist(), target_table)
            if not schema_result["is_valid"]:
                raise ValueError(f"Schema validation failed: {schema_result['message']}")

            # Load to BigQuery
            load_to_bigquery(df, target_table)

            # Archive
            archive_uri = copy_file_to_archive(raw_uri, source_config, load_date=datetime.now().strftime("%Y-%m-%d"))

            results.append({
                "source": source_name,
                "file_name": file_name,
                "status": "SUCCESS",
                "target_table": target_table,
                "record_count": len(df),
                "archive_uri": archive_uri
            })

        except Exception as e:
            results.append({
                "source": source_name,
                "file_name": file_name,
                "status": "FAILED",
                "error": str(e)
            })

    return results
            


def main():
    # Load config directly
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    for source_name, source_config in config["sources"].items():
        if not source_config.get("enabled", False):
            print(f"Skipping disabled source: {source_name}")
            continue

        print(f"Processing source: {source_name}")
        results = process_source(source_name, source_config)

        for res in results:
            print(res)

if __name__ == "__main__":
    main()


