drop table if exists `retailer-data-engineer.raw_local.audit_files`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.audit_files` (
source STRING,
file_name STRING,
checksum STRING,
status STRING, -- SUCCESS / FAILED / DUPLICATE
load_timestamp TIMESTAMP
);