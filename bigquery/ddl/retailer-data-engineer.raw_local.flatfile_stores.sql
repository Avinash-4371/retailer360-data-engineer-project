-- Description: Stores Table
-- Author: Avinash
-- Created Date: 2026-06-20

drop table if exists `retailer-data-engineer.raw_local.flatfile_stores`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_stores`
(
  store_id STRING OPTIONS(description="Store identifier"),
  store_name STRING OPTIONS(description="Name of the store"),
  store_type STRING OPTIONS(description="Type of store (e.g., retail, online)"),
  city STRING OPTIONS(description="City where the store is located"),
  state STRING OPTIONS(description="State where the store is located"),
  country STRING OPTIONS(description="Country where the store is located"),
  region STRING OPTIONS(description="Region of the store"),
  opening_date STRING OPTIONS(description="Opening date of the store"),
  manager_id STRING OPTIONS(description="Manager identifier"),
  active_flag STRING OPTIONS(description="Active indicator (Y/N or 0/1)"),
  updated_at STRING OPTIONS(description="Record updated timestamp"),
  load_date STRING OPTIONS(description="Receive date"),
  load_timestamp TIMESTAMP OPTIONS(description="Timestamp of ingestion"),
  source_file_name STRING OPTIONS(description="Source filename")
)
OPTIONS (
  description = "Raw stores data stored in string format"
);
