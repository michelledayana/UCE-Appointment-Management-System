variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
  default     = "vpc-00fc9781a7aa82739"
}

variable "subnet_id" {
  description = "Subnet pública (con Internet Gateway)"
  type        = string
  default     = "subnet-0df43fa54d65ede62"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Nombre del Key Pair en AWS"
  type        = string
  default     = "aq-key3"
}

variable "my_ip" {
  description = "IP pública autorizada para SSH (usar /32)"
  type        = string
}
