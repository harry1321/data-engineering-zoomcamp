terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.51.0"
    }
  }
}

# Specify the provider (GCP, AWS, Azure)
provider "google" {
  credentials = file(var.credential)
  project     = var.project
  region      = "US-WEST1"
}

resource "google_storage_bucket" "taxi-bucket" {
  name          = "datacamp2024-bucket"
  location      = "US-WEST1"
  storage_class = "standard"
  force_destroy = true
}