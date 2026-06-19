-- Description: Returns Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_returns`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_returns`
(
  return_id STRING OPTIONS(description="Unique return identifier"),
  order_id STRING OPTIONS(description="Order identifier"),
  order_item_id STRING OPTIONS(description="Order item identifier"),
  product_id STRING OPTIONS(description="Product identifier"),
  customer_id STRING OPTIONS(description="Customer identifier"),
  store_id STRING OPTIONS(description="Store identifier"),
  return_date STRING OPTIONS(description="Return date"),
  return_reason STRING OPTIONS(description="Reason for return"),
  refund_amount STRING OPTIONS(description="Refund amount"),
  return_status STRING OPTIONS(description="Return status"),
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "Raw returns data stored as string format"
)