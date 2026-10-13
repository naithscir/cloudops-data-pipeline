resource "google_bigquery_table" "metricas_servidores" {
  dataset_id = google_bigquery_dataset.operaciones_dataset.dataset_id
  table_id   = "metricas_servidores"

  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }

  schema = jsonencode([
    {
      name = "timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "servidor"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "ambiente"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "cpu_porcentaje"
      type = "FLOAT"
      mode = "NULLABLE"
    },
    {
      name = "memoria_porcentaje"
      type = "FLOAT"
      mode = "NULLABLE"
    },
    {
      name = "disco_porcentaje"
      type = "FLOAT"
      mode = "NULLABLE"
    },
    {
      name = "estado"
      type = "STRING"
      mode = "REQUIRED"
    }
  ])
}