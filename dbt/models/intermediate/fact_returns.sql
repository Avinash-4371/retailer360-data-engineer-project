{{ config(materialized='table') }}

SELECT
  r.return_id,
  r.order_id,
  r.order_item_id,
  r.return_date,
  CAST(FORMAT_DATE('%Y%m%d', r.return_date) AS INT64) AS date_sk,
  r.customer_id,
  r.product_id,
  r.store_id,
  r.return_reason,
  r.refund_amount,
  r.return_status
FROM {{ ref('stg_returns') }} r
