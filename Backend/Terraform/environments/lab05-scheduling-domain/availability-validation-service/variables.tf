variable "ami" {
  description = "AMI para la instancia del microservicio"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Amazon Linux 2, us-east-1
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Key pair para acceder a la instancia"
  type        = string
  default     = "aq-key5"  # Tu key pair creado en AWS
}

variable "vpc_id" {
  description = "ID de la VPC existente"
  type        = string
  default     = "vpc-081ef70e7871c1417"  # Tu VPC creada en Administration-service
}

variable "subnet_id" {
  description = "ID de la Subnet existente"
  type        = string
  default     = "subnet-01d6a59cc8520232c"  # Tu Subnet creada en Administration-service
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}