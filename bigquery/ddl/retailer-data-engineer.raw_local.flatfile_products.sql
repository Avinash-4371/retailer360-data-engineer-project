-- Description: Products Table
-- Author: Avinash
-- Created Date: 2026-06-20

drop table if exists `retailer-data-engineer.raw_local.flatfile_products`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_products`
(
  product_id STRING OPTIONS(description="Product identifier"),
  sku STRING OPTIONS(description="Stock keeping unit"),
  product_name STRING OPTIONS(description="Name of the product"),
  brand STRING OPTIONS(description="Brand of the product"),
  category STRING OPTIONS(description="Category of the product"),
  sub_category STRING OPTIONS(description="Sub-category of the product"),
  unit_cost STRING OPTIONS(description="Unit cost of the product"),
  mrp STRING OPTIONS(description="Maximum retail price"),
  launch_date STRING OPTIONS(description="Launch date of the product"),
  active_flag STRING OPTIONS(description="Active indicator (Y/N or 0/1)"),
  updated_at STRING OPTIONS(description="Record updated timestamp"),
  load_date STRING OPTIONS(description="Receive date"),
  load_timestamp TIMESTAMP OPTIONS(description="Timestamp of ingestion"),
  source_file_name STRING OPTIONS(description="Source filename")
)
OPTIONS (
  description = "Raw products data stored in string format"
)