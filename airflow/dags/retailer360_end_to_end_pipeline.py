"""
Retailer360 - Parallel Ingestion + dbt DAG
====================================================
1. Triggers Cloud Run Job retailer360-ingestion-job once per enabled source.
2. All enabled sources run in parallel.
3. dbt Cloud Run Job runs only after all ingestion tasks succeed.

Author: Avinash Kumar
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import yaml

# Airflow 3.x SDK imports
from airflow.sdk import DAG, TaskGroup

# Standard operators in Airflow 3.x
from airflow.providers.standard.operators.empty import EmptyOperator

# Google Cloud Run operator
from airflow.providers.google.cloud.operators.cloud_run import (
    CloudRunExecuteJobOperator,
)


# =====================================================================
# Environment / Project Config
# =====================================================================
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "retailer-data-engineer")
REGION = os.getenv("GCP_REGION", "us-central1")

INGESTION_JOB = os.getenv("INGESTION_JOB_NAME", "retailer360-ingestion-job")
DBT_JOB = os.getenv("DBT_JOB_NAME", "retailer360-dbt-job")


# =====================================================================
# Config File Auto Detection
# =====================================================================
_CONFIG_CANDIDATES = [
    Path("/home/airflow/gcs/data/config.yml"),      # Composer
    Path("/usr/local/airflow/include/config.yml"),  # Astro local
]

CONFIG_PATH = next(
    (p for p in _CONFIG_CANDIDATES if p.exists()),
    _CONFIG_CANDIDATES[-1],
)


def normalize_task_id(value: str) -> str:
    """
    Convert source name into valid Airflow task_id.
    Example:
      sales-data -> sales_data
      customer master -> customer_master
    """
    return re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_").lower()


def load_enabled_sources() -> dict:
    """
    Read config.yml and return only enabled sources.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

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
    dag_id="retailer360_end_to_end_pipeline",
    description="Parallel ingestion Cloud Run Jobs followed by dbt Cloud Run Job",
    schedule=None,
    start_date=datetime(2026, 7, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["retailer360", "ingestion", "dbt", "cloud-run"],
) as dag:

    start = EmptyOperator(task_id="start")

    end = EmptyOperator(task_id="end")

    # ================================================================
    # Parallel Ingestion Tasks
    # ================================================================
    with TaskGroup(group_id="ingestion") as ingestion_group:

        for source_name in ENABLED_SOURCES.keys():

            CloudRunExecuteJobOperator(
                task_id=f"ingest_{normalize_task_id(source_name)}",
                project_id=PROJECT_ID,
                region=REGION,
                job_name=INGESTION_JOB,
                overrides={
                    "container_overrides": [
                        {
                            "env": [
                                {
                                    "name": "SOURCE_NAME",
                                    "value": source_name,
                                },
                            ],
                        }
                    ],
                    "task_count": 1,
                    "timeout": "1800s",
                },
                gcp_conn_id="google_cloud_default",
            )

    # ================================================================
    # dbt Task - Runs only after all ingestion tasks are successful
    # ================================================================
    run_dbt = CloudRunExecuteJobOperator(
        task_id="run_dbt_transformations",
        project_id=PROJECT_ID,
        region=REGION,
        job_name=DBT_JOB,
        overrides={
            "task_count": 1,
            "timeout": "3600s",
        },
        gcp_conn_id="google_cloud_default",
    )

    # ================================================================
    # DAG Dependency
    # ================================================================
    start >> ingestion_group >> run_dbt >> end