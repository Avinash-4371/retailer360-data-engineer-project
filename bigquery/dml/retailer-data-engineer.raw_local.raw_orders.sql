with

 new_1_0 as(
  select
  order_id ,
  parse_date("%Y-%m-%d",order_date),
  customer_id,
  store_id,
  channel,
  country,
  payment_method,
  payment_status,
  order_status,
 safe_cast('gross_amount' as numeric),
 safe_cast('discount_amount' as numeric),
 safe_cast('tax_amount' as numeric),
 safe_cast('net_amount' as numeric),
 currency,
parse_timestamp('%Y-%m-%d %H:%M:%S',created_at),
parse_timestamp('%Y-%m-%d %H:%M:%S',created_at),
updated_at,
cast(load_date as date),
load_timestamp,
source_file_name

  from `retailer-data-engineer.raw_local.flatfile_orders` 
  where load_timestamp =(select max(load_timestamp) from `retailer-data-engineer.raw_local.flatfile_orders` )


)
select * from new_1_0