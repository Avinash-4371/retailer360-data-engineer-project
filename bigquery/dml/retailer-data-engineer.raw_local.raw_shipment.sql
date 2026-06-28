DECLARE last_load_timestamp TIMESTAMP;

SET last_load_timestamp = (
  SELECT IFNULL(MAX(load_timestamp), TIMESTAMP("1900-01-01"))
  FROM `retailer-data-engineer.raw_local.raw_shipment`
);

INSERT INTO `retailer-data-engineer.raw_local.raw_shipment`
SELECT
  shipment_id,
  supplier_id,
  warehouse_id,
  product_id,
  PARSE_DATE('%Y-%m-%d', shipment_date),
  PARSE_DATE('%Y-%m-%d', expected_delivery_date),
  PARSE_DATE('%Y-%m-%d', actual_delivery_date),
  SAFE_CAST(quantity_shipped AS INT64),
  shipment_status,
  CAST(load_date AS DATE),
  load_timestamp,
  source_file_name
FROM `retailer-data-engineer.raw_local.flatfile_shipment`
WHERE load_timestamp > last_load_timestamp;
