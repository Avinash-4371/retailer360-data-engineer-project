{{ config(materialized='table') }}
SELECT
  TO_HEX(MD5(store_id)) AS store_sk,
  store_id,
  store_name,
  store_type,
  city,
  state,
  country,
  region,
  opening_date,
  manager_id,
  active_flag,
  updated_at
FROM {{ ref('stg_stores') }}
