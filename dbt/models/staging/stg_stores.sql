{{ config(materialized='view') }}

SELECT
  TRIM(store_id) AS store_id,
  store_name,
  store_type,
  city,
  state,
  country,
  region,
  opening_date,
  manager_id,
  SAFE_CAST(active_flag AS BOOL) AS active_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at) as updated_at,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_stores') }}
WHERE store_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY updated_at DESC) = 1
