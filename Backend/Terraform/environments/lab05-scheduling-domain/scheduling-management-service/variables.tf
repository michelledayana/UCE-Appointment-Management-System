variable "ami" {
  description = "AMI para la instancia del microservicio"
  type        = string
  default     = "ami-0c02fb55956c7d316"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Key pair para SSH"
  type        = string
  default     = "aq-key5"
}

variable "vpc_id" {
  description = "VPC donde se desplegará la instancia"
  type        = string
  default     = "vpc-081ef70e7871c1417"   # <-- tu VPC
}

variable "subnet_id" {
  description = "Subnet donde se desplegará la instancia"
  type        = string
  default     = "subnet-01d6a59cc8520232c"  # <-- tu Subnet
}

variable "service_name" {
  description = "Nombre del microservicio"
  type        = string
  default     = "scheduling-management-service"
}

variable "service_port" {
  description = "Puerto del microservicio"
  type        = number
  default     = 8085
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}