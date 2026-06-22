from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
from unittest import result
from google.cloud import bigquery

def file_checksum(blob):
    blob.reload()  # Ensure the blob's metadata is up to date

    if blob.md5_hash:
        checksum = blob.md5_hash
    elif blob.crc32c:
        checksum = blob.crc32c
    else:
        checksum = f"{blob.name}_{blob.generation}_{blob.size}"

    return checksum

def file_process_check(audit_table,source_name,file_name,checksum):
    
    query=f"""
       select * from {audit_table}
         where source= @source_name
         and file_name=@file_name
         and checksum = @checksum
         and status='SUCCESS'
         limit 1
         
         """

    job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("source_name", "STRING", source_name),
        bigquery.ScalarQueryParameter("file_name", "STRING", file_name),
        bigquery.ScalarQueryParameter("checksum", "STRING", checksum)
    ]
  )
    result = bigquery.Client().query(query,job_config=job_config).result()
    return result.total_rows > 0
  
def insert_audit_record(audit_table,source_name,file_name,checksum,status):
    raw={
        "source":source_name,
        "file_name":file_name,
        "checksum":checksum,
        "status":status,
        "load_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }
    errors = bigquery.Client().insert_rows_json(audit_table, [raw])
    if errors:
        print(f"Error inserting audit record: {errors}")


