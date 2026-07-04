{{ config(materialized='view') }}

SELECT
  TRIM(promotion_id) AS promotion_id,
  promotion_name,
  TRIM(product_id) AS product_id,
  SAFE_CAST(discount_percentage AS INT64) AS discount_percentage,
  DATE(start_date) AS start_date,
  DATE(end_date) AS end_date,
  UPPER(campaign_channel) AS campaign_channel,
  SAFE_CAST(budget AS NUMERIC) AS budget,
  SAFE_CAST(active_flag AS BOOL) AS active_flag,
  source_file_name as file_name,
  load_timestamp
FROM {{ source('retailer_raw','flatfile_promotions') }}
WHERE promotion_id IS NOT NULL
