"""
Retailer360 - Parallel Ingestion DAG 
====================================================
Triggers Cloud Run Job (retailer360-ingestion-job) once per enabled source.
All sources run in parallel — one Cloud Run execution per source.

Author: Avinash Kumar
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

import yaml

# :white_check_mark: Airflow 3.x SDK imports
from airflow.sdk import DAG, TaskGroup

# :white_check_mark: Standard operators moved to standard provider in Airflow 3.x
from airflow.providers.standard.operators.empty import EmptyOperator

# :white_check_mark: Google provider for Cloud Run
from airflow.providers.google.cloud.operators.cloud_run import (
   CloudRunExecuteJobOperator,
)

# =====================================================================
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "retailer-data-engineer")
REGION = os.getenv("GCP_REGION", "us-central1")
INGESTION_JOB = os.getenv("INGESTION_JOB_NAME", "retailer360-ingestion-job")

# Auto-detect config.yml location (local + Composer)
_CONFIG_CANDIDATES = [
   Path("/home/airflow/gcs/data/config.yml"),      # Composer
   Path("/usr/local/airflow/include/config.yml"),  # Astro local
]
CONFIG_PATH = next(
   (p for p in _CONFIG_CANDIDATES if p.exists()),
   _CONFIG_CANDIDATES[-1],
)


def load_enabled_sources() -> dict:
   """Read config.yml and return only enabled sources."""
   with open(CONFIG_PATH) as f:
       cfg = yaml.safe_load(f)
   return {
       name: source_cfg
       for name, source_cfg in cfg.get("sources", {}).items()
       if source_cfg.get("enabled", False)
   }


ENABLED_SOURCES = load_enabled_sources()

default_args = {
   "owner": "avinash",
   "depends_on_past": False,
   "retries": 1,
   "retry_delay": timedelta(minutes=3),
}


with DAG(
   dag_id="retailer360_ingestion",
   description="Parallel Cloud Run ingestion per source",
   schedule=None,
   start_date=datetime(2026, 7, 1),
   catchup=False,
   max_active_runs=1,
   default_args=default_args,
   tags=["retailer360", "ingestion", "cloud-run"],
) as dag:

   start = EmptyOperator(task_id="start")
   end = EmptyOperator(task_id="end")

   with TaskGroup(group_id="ingestion") as ingestion_group:

       for source_name in ENABLED_SOURCES.keys():

           CloudRunExecuteJobOperator(
               task_id=f"ingest_{source_name}",
               project_id=PROJECT_ID,
               region=REGION,
               job_name=INGESTION_JOB,
               overrides={
                   "container_overrides": [
                       {
                           "env": [
                               {"name": "SOURCE_NAME", "value": source_name},
                           ],
                       }
                   ],
                   "task_count": 1,
                   "timeout": "1800s",
               },
               gcp_conn_id="google_cloud_default",
           )

   start >> ingestion_group >> end