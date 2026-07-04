-- Description:  supplier_shipments Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.faltfile_supplier_shipments`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_supplier_shipments`
(
  shipment_id STRING,
  supplier_id STRING,
  warehouse_id STRING,
  product_id STRING,
  shipment_date STRING,
  expected_delivery_date STRING,
  actual_delivery_date STRING,
  quantity_shipped STRING,
  shipment_status STRING,
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "supplier_shipments data stored in string format"
)