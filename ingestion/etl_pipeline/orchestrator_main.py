from datetime import datetime, timezone
import logging
from pathlib import Path
from google.cloud import storage
import yaml

from file_read import read_gcs_file_to_dataframe
from bq_load import load_to_bigquery
from metadata_colums import add_metadata_columns, convert_all_columns_to_string
from audit import file_checksum, insert_audit_record, file_process_check
from validate_schema import validate_schema
from file_movement import (copy_file_to_archive, copy_file_to_duplicate,copy_file_to_raw,copy_file_to_rejected)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

storage_client = storage.Client()


def get_load_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_run_id():
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def process_source(source_name, source_config):
    results = []

    run_id = get_run_id()
    load_date = get_load_date()

    target_table = source_config["target_table"]
    audit_table = source_config["audit_table"]

    # Create raw run folder
    raw_path = source_config["raw_path"]
    _, raw_prefix = raw_path.replace("gs://", "").split("/", 1)
    run_folder = f"{raw_prefix}/run_{run_id}"

    # List files from landing/source path
    src_bucket_name, src_prefix = source_config["source_path"].replace("gs://", "").split("/", 1)
    landing_bucket = storage_client.bucket(src_bucket_name)
    blobs = landing_bucket.list_blobs(prefix=src_prefix)

    logging.info(f"Started processing source: {source_name}")
    logging.info(f"Run folder created: {run_folder}")

    for blob in blobs:
        # Skip folder paths
        if not Path(blob.name).suffix:
            continue

        file_name = Path(blob.name).name
        raw_uri = None
        checksum = None
        rejected_uri = None

        logging.info(f"Processing file: {file_name}")

        try:
            # ---------------------------------------------------------
            # Step 1: Copy landing file to raw
            # ---------------------------------------------------------
            raw_uri = copy_file_to_raw(blob, source_config, run_folder)
            logging.info(f"Copied file to raw: {raw_uri}")

            # ---------------------------------------------------------
            # Step 2: Generate checksum
            # ---------------------------------------------------------
            checksum = file_checksum(blob)
            logging.info(f"Checksum generated: {checksum}")

            # ---------------------------------------------------------
            # Step 3: Check duplicate
            # ---------------------------------------------------------
            duplicate_check = file_process_check(audit_table,source_name,file_name,checksum)

            if duplicate_check:
                logging.warning(f"Duplicate file detected: {file_name}")

                duplicate_uri = copy_file_to_duplicate(raw_uri,source_config,load_date)

                insert_audit_record(audit_table,source_name,file_name,checksum,"DUPLICATE")

                results.append({"source": source_name,"file_name": file_name,"status": "DUPLICATE","raw_uri": raw_uri,"duplicate_uri": duplicate_uri
                })

                logging.info(f"Duplicate file moved successfully: {duplicate_uri}")

                # Important: duplicate file should not be loaded to BigQuery
                continue

            # ---------------------------------------------------------
            # Step 4: Read file from raw
            # ---------------------------------------------------------
            df = read_gcs_file_to_dataframe(raw_uri, source_config)
            logging.info(f"File read successfully: {file_name}, records: {len(df)}")

            # ---------------------------------------------------------
            # Step 5: Convert all columns to string
            # ---------------------------------------------------------
            df = convert_all_columns_to_string(df)

            # ---------------------------------------------------------
            # Step 6: Add metadata columns
            # ---------------------------------------------------------
            df = add_metadata_columns(df, raw_uri)

            # ---------------------------------------------------------
            # Step 7: Validate schema
            # ---------------------------------------------------------
            schema_result = validate_schema(df.columns.tolist(),target_table)

            if not schema_result["is_valid"]:
                logging.error(
                    f"Schema validation failed for {file_name}: {schema_result['message']}"
                )

                rejected_uri = copy_file_to_rejected(raw_uri,source_config,load_date)

                insert_audit_record(audit_table,source_name,file_name,checksum,"FAILED")

                results.append({"source": source_name,
                                "file_name": file_name,
                                "status": "FAILED",
                                "error": schema_result["message"],
                                "raw_uri": raw_uri,
                                "rejected_uri": rejected_uri
                })

                continue

            # ---------------------------------------------------------
            # Step 8: Load to BigQuery
            # ---------------------------------------------------------
            load_to_bigquery(df,target_table)

            logging.info(f"Loaded file to BigQuery table: {target_table}")

            # ---------------------------------------------------------
            # Step 9: Move file to archive after successful load
            # ---------------------------------------------------------
            archive_uri = copy_file_to_archive(raw_uri,source_config,load_date )

            # ---------------------------------------------------------
            # Step 10: Insert SUCCESS audit
            # ---------------------------------------------------------
            insert_audit_record(audit_table,source_name,file_name,checksum,"SUCCESS")

            results.append({
                "source": source_name,
                "file_name": file_name,
                "status": "SUCCESS",
                "record_count": len(df),
                "target_table": target_table,
                "raw_uri": raw_uri,
                "archive_uri": archive_uri
            })

            logging.info(f"File processed successfully: {file_name}")

        except Exception as e:
            error_message = str(e)
            logging.exception(f"Processing failed for file: {file_name}")

            # Move failed file to rejected folder if it exists in raw
            if raw_uri:
                try:
                    rejected_uri = copy_file_to_rejected(raw_uri,source_config,load_date)

                    logging.info(f"Failed file moved to rejected: {rejected_uri}")

                except Exception as reject_error:
                    error_message += f" | Failed to move to rejected: {str(reject_error)}"
                    logging.exception(f"Failed to move file to rejected: {file_name}")

            # Insert FAILED audit
            try:
                insert_audit_record(audit_table,source_name,file_name,checksum,"FAILED")

            except Exception as audit_error:
                error_message += f" | Failed to insert FAILED audit: {str(audit_error)}"
                logging.exception(f"Failed to insert audit record for file: {file_name}")

            results.append({
                "source": source_name,
                "file_name": file_name,
                "status": "FAILED",
                "error": error_message,
                "raw_uri": raw_uri,
                "rejected_uri": rejected_uri
            })

    logging.info(f"Completed processing source: {source_name}")

    return results


def main():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    all_results = []

    for source_name, source_config in config["sources"].items():
        if not source_config.get("enabled", False):
            logging.info(f"Skipping disabled source: {source_name}")
            continue

        logging.info(f"Processing source: {source_name}")

        results = process_source(source_name, source_config)
        all_results.extend(results)

    logging.info("Pipeline execution completed")

    for res in all_results:
        print(res)


if __name__ == "__main__":
    main()
