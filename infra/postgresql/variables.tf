variable "aiven_api_token" {
  description = "Aiven token"
  type        = string
}

variable "project_name" {
  description = "Aiven console project name"
  type        = string
}

variable "admin_username" {
  description = "pg admin username"
  type        = string
}

variable "admin_password" {
  description = "pg admin password"
  type        = string
  sensitive   = true
}
