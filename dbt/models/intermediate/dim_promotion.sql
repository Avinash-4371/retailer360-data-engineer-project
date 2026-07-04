{{ config(materialized='table') }}

SELECT
  TO_HEX(MD5(promotion_id)) AS promotion_sk,
  promotion_id,
  promotion_name,
  product_id,
  discount_percentage,
  start_date,
  end_date,
  campaign_channel,
  budget,
  active_flag
FROM {{ ref('stg_promotions') }}
