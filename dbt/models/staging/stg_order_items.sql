{{ config(materialized='view') }}

SELECT
  TRIM(order_item_id) AS order_item_id,
  TRIM(order_id) AS order_id,
  TRIM(product_id) AS product_id,
  NULLIF(TRIM(promotion_id), '') AS promotion_id,
  SAFE_CAST(quantity AS INT64) AS quantity,
  SAFE_CAST(unit_price AS NUMERIC) AS unit_price,
  SAFE_CAST(discount_amount AS NUMERIC) AS discount_amount,
  SAFE_CAST(tax_amount AS NUMERIC) AS tax_amount,
  SAFE_CAST(line_total AS NUMERIC) AS line_total,
  SAFE_CAST(return_flag AS BOOL) AS return_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', created_at) as created_at,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at) as updated_at,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_order_items') }}
WHERE order_item_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_item_id ORDER BY updated_at DESC) = 1
