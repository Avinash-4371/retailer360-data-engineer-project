{{ config(materialized='view') }}
select 
  TRIM(order_id) AS order_id,
  DATE(order_date) AS order_date,
  TRIM(customer_id) AS customer_id,
  TRIM(store_id) AS store_id,
  UPPER(TRIM(channel)) AS channel,
  UPPER(TRIM(payment_status)) AS payment_status,
  UPPER(TRIM(order_status)) AS order_status,
  SAFE_CAST(gross_amount AS NUMERIC) AS gross_amount,
  SAFE_CAST(discount_amount AS NUMERIC) AS discount_amount,
  SAFE_CAST(tax_amount AS NUMERIC) AS tax_amount,
  SAFE_CAST(net_amount AS NUMERIC) AS net_amount,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', created_at) as created_at,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at) as updated_at,
  load_timestamp,
  source_file_name as file_name
from
{{ source('retailer_raw', 'flatfile_orders') }}
WHERE store_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY updated_at DESC) = 1