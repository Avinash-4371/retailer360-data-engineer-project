{{ config(materialized='view') }}

SELECT
  TRIM(shipment_id) AS shipment_id,
  TRIM(supplier_id) AS supplier_id,
  TRIM(warehouse_id) AS warehouse_id,
  TRIM(product_id) AS product_id,
  DATE(shipment_date) AS shipment_date,
  DATE(expected_delivery_date) AS expected_delivery_date,
  DATE(actual_delivery_date) AS actual_delivery_date,
  SAFE_CAST(quantity_shipped AS INT64) AS quantity_shipped,
  UPPER(shipment_status) AS shipment_status,
  load_timestamp,
  source_file_name as file_name
FROM {{ source('retailer_raw','flatfile_supplier_shipments') }}
WHERE shipment_id IS NOT NULL
