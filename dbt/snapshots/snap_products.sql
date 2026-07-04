{% snapshot snap_products %}
{{
   config(
       target_database='retailer-data-engineer',
       target_schema='retailer_staging',
       unique_key='product_id',

         strategy='check',
         check_cols=['brand','category','sub_category','unit_cost','mrp','launch_date','active_flag']
   )

}}


SELECT
  product_id,
  sku,
  product_name,
  brand,
  category,
  sub_category,
  unit_cost,
  mrp,
  launch_date,
  active_flag,
  updated_at
FROM {{ ref('stg_products') }}

{% endsnapshot %}
