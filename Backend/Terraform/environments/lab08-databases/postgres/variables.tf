variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID where Postgres EC2 will live"
  type        = string
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "my_ip" {
  description = "Your public IP for SSH access"
  type        = string
}
