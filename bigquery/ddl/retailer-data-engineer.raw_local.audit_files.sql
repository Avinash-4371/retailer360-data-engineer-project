drop table if exists `retailer-data-engineer.raw_local.audit_files`;
CREATE TABLE IF NOT EXISTS `retailer-data-engineer.raw_local.audit_files` (
source_name STRING,
file_name STRING,
checksum STRING,
status STRING, -- SUCCESS / FAILED / DUPLICATE
processed_at TIMESTAMP
);