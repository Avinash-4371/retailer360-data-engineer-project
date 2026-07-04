{{ config(materialized='view') }}

SELECT
  TRIM(return_id) AS return_id,
  TRIM(order_id) AS order_id,
  TRIM(order_item_id) AS order_item_id,
  TRIM(product_id) AS product_id,
  TRIM(customer_id) AS customer_id,
  TRIM(store_id) AS store_id,
  DATE(return_date) AS return_date,
  UPPER(return_reason) AS return_reason,
  SAFE_CAST(refund_amount AS NUMERIC) AS refund_amount,
  UPPER(return_status) AS return_status,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_returns') }}
WHERE return_id IS NOT NULL
