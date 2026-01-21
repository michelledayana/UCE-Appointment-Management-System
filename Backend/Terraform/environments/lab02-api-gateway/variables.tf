variable "vpc_id" {
  description = "ID de la VPC donde se desplegará la API Gateway"
  type        = string
}

variable "public_subnet_1" {
  description = "Subnet pública 1 en la VPC"
  type        = string
}

variable "public_subnet_2" {
  description = "Subnet pública 2 en la VPC"
  type        = string
}

variable "my_ip" {
  description = "Tu IP pública para reglas de seguridad SSH"
  type        = string
}

variable "docker_image" {
  description = "Imagen Docker de la API Gateway"
  type        = string
}
