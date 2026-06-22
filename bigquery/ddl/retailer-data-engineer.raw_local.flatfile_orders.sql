-- Description: Order Table
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_orders`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_orders`
(
  order_id STRING OPTIONS(description="Unique order identifier"),
  order_date STRING OPTIONS(description="Order date"),
  customer_id STRING OPTIONS(description="Customer identifier"),
  store_id STRING OPTIONS(description="Store identifier"),
  channel STRING OPTIONS(description="Sales channel"),
  country STRING OPTIONS(description="Country of order"),
  payment_method STRING OPTIONS(description="Payment method used"),
  payment_status STRING OPTIONS(description="Payment status"),
  order_status STRING OPTIONS(description="Order status"),
  gross_amount STRING OPTIONS(description="Total order amount before discount"),
  discount_amount STRING OPTIONS(description="Discount applied"),
  tax_amount STRING OPTIONS(description="Tax amount"),
  net_amount STRING OPTIONS(description="Final payable amount"),
  currency STRING OPTIONS(description="Currency code"),
  created_at STRING OPTIONS(description="Record creation timestamp"),
  updated_at STRING OPTIONS(description="Record last update timestamp"),
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "Orders data table storing transactional details"
);