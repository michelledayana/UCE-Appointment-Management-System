variable "vpc_id" {
  default = "vpc-00fc9781a7aa82739"  # La nueva VPC creada con authentication-service
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}

variable "subnet_id" {
  default = "subnet-0df43fa54d65ede62"  # Subnet creada dentro de la nueva VPC
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  default = "aq-key3"
}
