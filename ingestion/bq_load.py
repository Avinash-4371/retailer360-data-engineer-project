from google.cloud import bigquery

def load_to_bigquery(df: pd.DataFrame, target_table: str):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",  # append data
        autodetect=True                    # infer schema if not provided
    )

    job = client.load_table_from_dataframe(
        df,
        target_table,   # e.g. "project.dataset.raw_inventory_snapshot"
        job_config=job_config
    )

    job.result()  # wait for job to finish
    print(f"Loaded {df.shape[0]} rows into {target_table}.")
