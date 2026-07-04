{{ config(materialized='table') }}

SELECT
  TO_HEX(MD5(CONCAT(customer_id,'|',CAST(dbt_valid_from AS STRING)))) AS customer_sk,
  customer_id,
  first_name,
  last_name,
  email,
  phone_number,
  gender,
  date_of_birth,
  city,
  state,
  country,
  loyalty_tier,
  customer_status,
  dbt_valid_from AS effective_start_date,
  COALESCE(dbt_valid_to, TIMESTAMP('9999-12-31')) AS effective_end_date,
  dbt_valid_to IS NULL AS is_current
FROM {{ ref('snap_customers') }}
