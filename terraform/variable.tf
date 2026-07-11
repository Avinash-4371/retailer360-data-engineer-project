variable "project_id" {
    type        = string
    description = "GCP project ID"
  
}
variable "region" {
    type        = string
    description = "GCP region"
    default     = "us-central1"
  
}
variable "location" {
    type        = string
    description = "Bigquery and GCS location"
  default     = "us-central1"
  
}
variable "artifact_repo" {
    type        = string
    default     = "retailer360-repo"
  
}   

variable "ingestion_image" {
    type        = string
    default     = "retailer360-ingestion"
  
}

variable "dbt_image" {
    type        = string
    default     = "retailer360-dbt"
  
}
variable "ingestion_job_name" {
    type        = string
    default     = "retailer360-ingestion-job"
  
}

variable "dbt_job_name" {
    type        = string
    default     = "retailer360-dbt-job"
  
}

