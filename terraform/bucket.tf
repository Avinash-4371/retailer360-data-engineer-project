resource "google_storage_bucket" "landing_bucket_not_build" {
  name                        = "${var.project_id}-landing-bucket"
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = false

  labels = {
    project = "retailer360"
    layer   = "landing"
  }


}

resource "google_storage_bucket" "landing_bucket" {
  name                        = "retailer_landing_data"
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = false

  labels = {
    project = "retailer360"
    layer   = "landing"
  }


}
resource "google_storage_bucket" "processed_bucket" {
  name                        = "retailer_data"
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = false

  labels = {
    project = "retailer360"
    layer   = "processed"
  }


}