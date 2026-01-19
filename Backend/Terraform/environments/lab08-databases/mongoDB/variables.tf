variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID where MongoDB EC2 will live"
  type        = string
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "bastion_public_ip_cidr" {
  description = "CIDR of Bastion to allow SSH"
  type        = string
}
