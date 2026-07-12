{{ config(materialized='table') }}

SELECT
  snapshot_date,
  CAST(FORMAT_DATE('%Y%m%d', snapshot_date) AS INT64) AS date_sk,
  store_id,
  product_id,
  warehouse_id,
  available_qty,
  reserved_qty,
  damaged_qty,
  reorder_level,
  (available_qty <= reorder_level) AS stockout_flag,
  (available_qty > reorder_level * 5) AS overstock_flag
FROM {{ ref('stg_inventory_snapshot') }}
