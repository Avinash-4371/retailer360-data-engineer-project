{{ config(materialized='view') }}

with latest_customers as (
    select *,
    row_number() over( partition by customer_id order by updated_at desc ) as rn
    FROM {{ source('retailer_raw','flatfile_customers') }}

)

SELECT
customer_id,
trim(first_name) as first_name,
trim(last_name) as last_name,
lower(email) as email,
regexp_replace(phone,r'[^0-9]','') as phone_number,
upper(gender) as gender,
PARSE_DATE('%Y-%m-%d', SUBSTR(dob, 1, 10)) AS date_of_birth,
initcap(city) as city,
initcap(state) as state,
initcap(country) as country,
upper(loyalty_tier) as loyalty_tier,
upper(customer_status) as customer_status,
PARSE_TIMESTAMP('%Y-%m-%d', updated_at) AS updated_at
FROM latest_customers
where rn =1
