from google.cloud import bigquery
import logging

logger = logging.getLogger(__name__)

def validate_schema(df_columns: list[str], target_table: str) -> dict:
    client = bigquery.Client()

    try:
        table = client.get_table(target_table)
    except Exception as e:
        msg = f"Could not fetch schema for {target_table}: {e}"
        logger.error(msg)
        return {"is_valid": False, "message": msg}

    expected = set([field.name for field in table.schema])
    actual = set(df_columns)

    missing = list(expected - actual)
    extra = list(actual - expected)

    if missing or extra:
        msg = f"Schema mismatch for {target_table}. Missing: {missing}. Extra: {extra}."
        logger.error(msg)
        return {"is_valid": False, "message": msg}

    logger.info("Schema validated for table: %s", target_table)
    return {"is_valid": True, "message": "Schema validation passed."}
