-- Description: promotions
-- Author: Avinash
-- Created Date: 2026-06-20


drop table if exists `retailer-data-engineer.raw_local.flatfile_promotions`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.flatfile_promotions`
(
  promotion_id STRING,
  promotion_name STRING,
  product_id STRING,
  discount_percentage STRING,
  start_date STRING,
  end_date STRING,
  campaign_channel STRING,
  budget STRING,
  active_flag STRING,
  load_date STRING OPTIONS(description="receive date"),
  load_timestamp timestamp OPTIONS(description=" timestamp"),
  source_file_name STRING OPTIONS(description="filename")
)
OPTIONS (
  description = "promotions data stored in string format"
)