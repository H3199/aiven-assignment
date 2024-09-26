  resource "aiven_pg" "pg" {
    project                = data.aiven_project.my_project.project
    service_name           = "postgresql"
    cloud_name             = "google-europe-west3"
    plan                   = "startup-4"
  }

  output "postgresql_service_uri" {
    value     = aiven_pg.postgresql.service_uri
    sensitive = true
  }
