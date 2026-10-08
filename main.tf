terraform {
  required_version = ">= 1.5.0"

  backend "gcs" {
    bucket = "tfstate-naithscir-cloudops"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Creamos un Dataset en BigQuery (Nuestra base de datos analítica)
resource "google_bigquery_dataset" "operaciones_dataset" {
  dataset_id                  = "ops_automation_dataset"
  friendly_name               = "Dataset de Operaciones TI"
  description                 = "Dataset creado automáticamente mediante Terraform y CI/CD"
  location                    = "US"
  delete_contents_on_destroy = true # Útil para entornos de prueba
}

output "dataset_id" {
  value = google_bigquery_dataset.operaciones_dataset.dataset_id
}