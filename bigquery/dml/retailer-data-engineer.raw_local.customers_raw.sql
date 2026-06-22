DECLARE last_load_timestamp TIMESTAMP;

-- Step 1: Get last load timestamp (fallback if empty)
SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.customers_raw`
);

-- Step 2: Insert latest batch from flatfile
INSERT INTO `retailer-data-engineer.raw_local.customers_raw`
SELECT
  SAFE_CAST(customer_id AS STRING) AS customer_id,
  SAFE_CAST(first_name AS STRING) AS first_name,
  SAFE_CAST(last_name AS STRING) AS last_name,
  SAFE_CAST(email AS STRING) AS email,
  SAFE_CAST(phone AS STRING) AS phone,
  SAFE_CAST(gender AS STRING) AS gender,
  SAFE_CAST(dob AS DATE) AS dob,
  SAFE_CAST(city AS STRING) AS city,
  SAFE_CAST(state AS STRING) AS state,
  SAFE_CAST(country AS STRING) AS country,
  SAFE_CAST(loyalty_tier AS STRING) AS loyalty_tier,
  SAFE_CAST(registration_date AS DATE) AS registration_date,
  SAFE_CAST(customer_status AS STRING) AS customer_status,
  SAFE_CAST(updated_at AS TIMESTAMP) AS updated_at,
  CAST(load_date AS DATE) AS load_date,
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_customers`
WHERE load_timestamp > last_load_timestamp;
