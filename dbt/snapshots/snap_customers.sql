{% snapshot snap_customers %}

{{
   config(
       target_database='retailer-data-engineer',
       target_schema='retailer_staging',
       unique_key='customer_id',


       strategy='check',
       check_cols=['city','state','country','loyalty_tier','customer_status'] 
   )
}}

SELECT
  customer_id,
  first_name,
  last_name,
  email,
  phone_number,
  gender,
  date_of_birth,
  city,
  state,
  country,
  loyalty_tier,
  customer_status,
  updated_at
FROM {{ ref('stg_customers') }}


{% endsnapshot %}