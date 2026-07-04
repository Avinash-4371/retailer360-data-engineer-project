-- Description:  inventory_snapshot Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_inventory_snapshot`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_inventory_snapshot`
(
  snapshot_date STRING,
  store_id STRING,
  product_id STRING,
  warehouse_id STRING,
  available_qty STRING,
  reserved_qty STRING,
  damaged_qty STRING,
  reorder_level STRING,
  updated_at STRING,
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "inventory_snapshot data stored in string format"
)