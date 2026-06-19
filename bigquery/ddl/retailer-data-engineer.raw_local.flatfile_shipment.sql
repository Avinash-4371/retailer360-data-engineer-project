
-- Description: Shipment Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_shipment`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_shipment`
(
  shipment_id STRING OPTIONS(description="Unique shipment identifier"),
  supplier_id STRING OPTIONS(description="Supplier identifier"),
  warehouse_id STRING OPTIONS(description="Warehouse identifier"),
  product_id STRING OPTIONS(description="Product identifier"),
  shipment_date STRING OPTIONS(description="Shipment date"),
  expected_delivery_date STRING OPTIONS(description="Expected delivery date"),
  actual_delivery_date STRING OPTIONS(description="Actual delivery date"),
  quantity_shipped STRING OPTIONS(description="Quantity shipped"),
  shipment_status STRING OPTIONS(description="Shipment status"),
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "Raw shipment data stored in string format"
);