{{ config(materialized='table') }}

SELECT
  TO_HEX(MD5(CONCAT(product_id,'|',CAST(dbt_valid_from AS STRING)))) AS product_sk,
  product_id,
  sku,
  product_name,
  brand,
  category,
  sub_category,
  unit_cost,
  mrp,
  launch_date,
  active_flag,
  dbt_valid_from AS effective_start_ts,
  COALESCE(dbt_valid_to, TIMESTAMP('9999-12-31')) AS effective_end_ts,
  dbt_valid_to IS NULL AS is_current
FROM {{ ref('snap_products') }}
