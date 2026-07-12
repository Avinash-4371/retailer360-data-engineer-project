{{ config(materialized='table') }}

WITH sales AS (
  SELECT
    customer_id,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(net_amount) AS total_spent,
    AVG(net_amount) AS avg_order_value
  FROM {{ ref('fact_sales') }}
  GROUP BY customer_id
),

returns AS (
  SELECT
    customer_id,
    COUNT(return_id) AS return_count,
    SUM(refund_amount) AS refund_total
  FROM {{ ref('fact_returns') }}
  GROUP BY customer_id
)

SELECT
  c.customer_id,
  CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
  c.country,
  c.loyalty_tier,
  s.first_order_date,
  s.last_order_date,
  s.total_orders,
  s.total_spent,
  s.avg_order_value,
  COALESCE(r.return_count, 0) AS return_count,
  COALESCE(r.refund_total, 0) AS refund_total,
  DATE_DIFF(CURRENT_DATE(), s.last_order_date, DAY) AS days_since_last_purchase,
  CASE
    WHEN s.total_spent > 50000 THEN 'VIP'
    WHEN s.total_orders >= 10 THEN 'LOYAL'
    WHEN DATE_DIFF(CURRENT_DATE(), s.last_order_date, DAY) > 90 THEN 'AT_RISK'
    WHEN s.first_order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN 'NEW'
    ELSE 'NORMAL'
  END AS customer_segment
FROM {{ ref('dim_customer') }} c
JOIN sales s ON c.customer_id = s.customer_id
LEFT JOIN returns r ON c.customer_id = r.customer_id
WHERE c.is_current = TRUE
