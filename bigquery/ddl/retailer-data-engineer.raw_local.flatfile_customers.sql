-- Description: Customers Table
-- Author: Avinash
-- Created Date: 2026-06-20

drop table if exists `retailer-data-engineer.raw_local.flatfile_customers`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_customers`
(
  customer_id STRING OPTIONS(description="Unique customer identifier"),
  first_name STRING OPTIONS(description="Customer first name"),
  last_name STRING OPTIONS(description="Customer last name"),
  email STRING OPTIONS(description="Customer email address"),
  phone STRING OPTIONS(description="Customer phone number"),
  gender STRING OPTIONS(description="Customer gender"),
  dob STRING OPTIONS(description="Date of birth"),
  city STRING OPTIONS(description="City"),
  state STRING OPTIONS(description="State"),
  country STRING OPTIONS(description="Country"),
  loyalty_tier STRING OPTIONS(description="Customer loyalty tier"),
  registration_date STRING OPTIONS(description="Customer registration date"),
  customer_status STRING OPTIONS(description="Customer status"),
  updated_at STRING OPTIONS(description="Last updated timestamp"),
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "Raw customer master data stored in string format"
)