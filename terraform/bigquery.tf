resource "google_bigquery_dataset" "raw_local" {
    dataset_id                  = "raw_local"
    location                    = var.location
    delete_contents_on_destroy   = false
 
  
}
resource "google_bigquery_dataset" "retailer_staging" {
    dataset_id                  = "retailer_staging"
    location                    = var.location
    delete_contents_on_destroy   = false
 
  
}

resource "google_bigquery_dataset" "mart" {
    dataset_id                  = "retailer_mart"
    location                    = var.location
    delete_contents_on_destroy   = false
 
  
}