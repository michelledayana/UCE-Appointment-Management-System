variable "vpc_id" {
  description = "VPC existente donde se desplegará el microservicio"
  type        = string
}

variable "subnet_id" {
  description = "Subnet pública existente"
  type        = string
}

variable "my_ip" {
  description = "IP pública autorizada para SSH (x.x.x.x/32)"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Nombre del key pair para SSH"
  type        = string
}
