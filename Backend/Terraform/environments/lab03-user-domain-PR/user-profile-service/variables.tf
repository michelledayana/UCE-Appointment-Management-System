variable "vpc_id" {
  description = "VPC donde se desplegara el servicio"
  type        = string
}

variable "subnet_ids" {
  description = "Subnets para el Auto Scaling Group"
  type        = list(string)
}

variable "my_ip" {
  description = "IP publica para acceso SSH"
  type        = string
}

variable "key_name" {
  description = "Key pair para acceso SSH"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}
