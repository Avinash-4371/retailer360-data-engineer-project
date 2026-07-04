{{ config(materialized='view') }}

SELECT
  DATE(snapshot_date) AS snapshot_date,
  TRIM(store_id) AS store_id,
  TRIM(product_id) AS product_id,
  TRIM(warehouse_id) AS warehouse_id,
  SAFE_CAST(available_qty AS INT64) AS available_qty,
  SAFE_CAST(reserved_qty AS INT64) AS reserved_qty,
  SAFE_CAST(damaged_qty AS INT64) AS damaged_qty,
  SAFE_CAST(reorder_level AS INT64) AS reorder_level,
  updated_at,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_inventory_snapshot') }}
