-- Description: Order Items Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_order_items`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_order_items`
(
  order_id STRING OPTIONS(description="Order identifier"),
  product_id STRING OPTIONS(description="Product identifier"),
  promotion_id STRING OPTIONS(description="Promotion identifier"),
  quantity STRING OPTIONS(description="Quantity of items"),
  unit_price STRING OPTIONS(description="Unit price of product"),
  discount_amount STRING OPTIONS(description="Discount applied"),
  tax_amount STRING OPTIONS(description="Tax applied"),
  line_total STRING OPTIONS(description="Total amount for line item"),
  return_flag STRING OPTIONS(description="Return indicator (Y/N or 0/1)"),
  created_at STRING OPTIONS(description="Record created timestamp"),
  updated_at STRING OPTIONS(description="Record updated timestamp"),
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "Raw order items data stored in string format"
)