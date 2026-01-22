variable "my_ip" {
  description = "Tu IP pública para permitir SSH"
  type        = string
}

variable "region" {
  description = "Región donde se desplegarán los recursos"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "Nombre del key pair de EC2"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR de la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_a_cidr" {
  description = "CIDR de la subnet A"
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_b_cidr" {
  description = "CIDR de la subnet B"
  type        = string
  default     = "10.0.2.0/24"
}
