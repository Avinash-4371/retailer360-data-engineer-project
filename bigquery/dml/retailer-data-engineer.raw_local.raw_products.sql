DECLARE last_load_timestamp TIMESTAMP;

SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.raw_products`
);

INSERT INTO `retailer-data-engineer.raw_local.raw_products`
SELECT
  product_id,
  sku,
  product_name,
  brand,
  category,
  sub_category,
  SAFE_CAST(unit_cost AS NUMERIC),
  SAFE_CAST(mrp AS NUMERIC),
  PARSE_DATE('%Y-%m-%d', launch_date),
  active_flag,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', updated_at),
  CAST(load_date AS DATE),
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_products`
WHERE load_timestamp > last_load_timestamp;
