variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "my_ip" {
  description = "Your public IP for SSH and Mongo access"
  type        = string
}
