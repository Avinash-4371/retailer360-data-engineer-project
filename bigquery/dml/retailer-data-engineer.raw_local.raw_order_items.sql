DECLARE last_load_timestamp TIMESTAMP;

SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.raw_order_items`
);

INSERT INTO `retailer-data-engineer.raw_local.raw_order_items`
SELECT
  order_id,
  product_id,
  promotion_id,
  SAFE_CAST(quantity AS INT64),
  SAFE_CAST(unit_price AS NUMERIC),
  SAFE_CAST(discount_amount AS NUMERIC),
  SAFE_CAST(tax_amount AS NUMERIC),
  SAFE_CAST(line_total AS NUMERIC),
  return_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', created_at),
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at),
  CAST(load_date AS DATE),
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_order_items`
WHERE load_timestamp > last_load_timestamp;
