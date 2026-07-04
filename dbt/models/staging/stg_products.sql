{{ config(materialized='view') }}

SELECT
  TRIM(product_id) AS product_id,
  sku,
  product_name,
  brand,
  category,
  sub_category,
  SAFE_CAST(unit_cost AS NUMERIC) AS unit_cost,
  SAFE_CAST(mrp AS NUMERIC) AS mrp,
  launch_date,
  SAFE_CAST(active_flag AS BOOL) AS active_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at) as updated_at,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_products') }}
WHERE product_id IS NOT NULL
