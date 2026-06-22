DECLARE last_load_timestamp TIMESTAMP;

SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.raw_returns`
);

INSERT INTO `retailer-data-engineer.raw_local.raw_returns`
SELECT
  return_id,
  order_id,
  order_item_id,
  product_id,
  customer_id,
  store_id,
  PARSE_DATE('%Y-%m-%d', return_date),
  return_reason,
  SAFE_CAST(refund_amount AS NUMERIC),
  return_status,
  CAST(load_date AS DATE),
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_returns`
WHERE load_timestamp > last_load_timestamp;
