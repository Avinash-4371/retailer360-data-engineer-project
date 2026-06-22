from google.cloud import bigquery
import logging

from pendulum import datetime

logger = logging.getLogger(__name__)

def convert_all_columns_to_string(df):
    return df.astype(str)

def add_metadata_columns(df,source_file_path):
    df["_source_file_name"] = source_file_path.split("/")[-1]
    df["_load_timestamp"] = datetime.now()
    df["_date"]= datetime.now().date()

    return df

def validate_schema(df_columns: list[str], target_table: str) -> dict:

    client = bigquery.Client()

    try:
        table = client.get_table(target_table)  # e.g. "myproject.mydataset.raw_inventory_snapshot"
    except Exception as e:
        msg = f"Could not fetch schema for {target_table}: {e}"
        logger.error(msg)
        return {"is_valid": False, "message": msg}

    # Expected columns from BigQuery schema
    expected = set([field.name for field in table.schema])

    # Actual columns from DataFrame (ignore metadata prefixed with "_")
    actual = set(col for col in df_columns if not col.startswith("_"))

    missing = list(expected - actual)
    extra = list(actual - expected)

    if missing or extra:
        msg = f"Schema mismatch for {target_table}. Missing: {missing}. Extra: {extra}."
        logger.error(msg)
        return {"is_valid": False, "message": msg}

    logger.info("Schema validated for table: %s", target_table)
    return {"is_valid": True, "message": "Schema validation passed."}


