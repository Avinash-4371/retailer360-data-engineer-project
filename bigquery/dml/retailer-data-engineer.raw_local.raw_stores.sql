DECLARE last_load_timestamp TIMESTAMP;

SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.raw_stores`
);

INSERT INTO `retailer-data-engineer.raw_local.raw_stores`
SELECT
  store_id,
  store_name,
  store_type,
  city,
  state,
  country,
  region,
  PARSE_DATE('%Y-%m-%d', opening_date),
  manager_id,
  active_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at),
  CAST(load_date AS DATE),
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_stores`
WHERE load_timestamp > last_load_timestamp;
