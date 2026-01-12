variable "private_subnet_id" {
  description = "Private subnet A ID"
  type        = string
}

variable "private_subnet_b_id" {
  description = "Private subnet B ID"
  type        = string
}

variable "security_group_id" {
  description = "Security group for Postgres"
  type        = string
}

variable "db_password" {
  description = "Postgres master password"
  type        = string
  sensitive   = true
}
