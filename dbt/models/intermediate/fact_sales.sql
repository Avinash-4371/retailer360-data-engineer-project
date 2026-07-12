{{ config(
  materialized='incremental',
  unique_key='order_item_id',
  incremental_strategy='merge',
  partition_by={"field": "order_date", "data_type": "date"},
  cluster_by=["store_id","product_id","customer_id"]
) }}

WITH orders AS (
  SELECT *
  FROM {{ ref('stg_orders') }}
  WHERE payment_status='PAID'
    AND order_status NOT IN ('CANCELLED','FAILED')
),

items AS (
  SELECT * FROM {{ ref('stg_order_items') }}
),

customers AS (
  SELECT * FROM {{ ref('dim_customer') }}
),

products AS (
  SELECT * FROM {{ ref('dim_product') }}
),

stores AS (
  SELECT * FROM {{ ref('dim_store') }}
),

promotions AS (
  SELECT promotion_id, promotion_sk, discount_percentage, campaign_channel
  FROM {{ ref('dim_promotion') }}
)

SELECT
  items.order_item_id,
  orders.order_id,
  orders.order_date,
  CAST(FORMAT_DATE('%Y%m%d', orders.order_date) AS INT64) AS date_sk,

  orders.store_id,
  orders.customer_id,
  items.product_id,
  orders.channel,

  stores.store_sk,

  -- AS-OF SCD2 joins
  customers.customer_sk,
  products.product_sk,

  items.promotion_id,
  promotions.promotion_sk,
  promotions.discount_percentage,
  promotions.campaign_channel,

  items.quantity,
  items.unit_price,
  items.discount_amount,
  items.tax_amount,
  items.line_total AS net_amount,

  products.unit_cost,
  (items.quantity * products.unit_cost) AS cost_amount,
  (items.line_total - (items.quantity * products.unit_cost)) AS profit_amount,

  CURRENT_TIMESTAMP() AS loaded_at

FROM orders
JOIN items ON orders.order_id = items.order_id
LEFT JOIN stores ON orders.store_id = stores.store_id

LEFT JOIN customers
  ON orders.customer_id = customers.customer_id
 AND TIMESTAMP(orders.order_date) >= customers.effective_start_date
 AND TIMESTAMP(orders.order_date) <  customers.effective_end_date

LEFT JOIN products
  ON items.product_id = products.product_id
 AND TIMESTAMP(orders.order_date) >= products.effective_start_date
 AND TIMESTAMP(orders.order_date) <  products.effective_end_date

LEFT JOIN promotions
  ON items.promotion_id = promotions.promotion_id

{% if is_incremental() %}
  {% set max_load_time = "(SELECT COALESCE(MAX(loaded_at), TIMESTAMP('1900-01-01')) FROM " ~ this ~ ")" %}
  WHERE orders.load_timestamp > {{ max_load_time }}
     OR items.load_timestamp > {{ max_load_time }}
{% endif %}
