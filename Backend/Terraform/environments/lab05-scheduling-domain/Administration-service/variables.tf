variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "ami" {
  description = "AMI para la instancia EC2"
  type        = string
  default     = "ami-0c02fb55956c7d316" # Amazon Linux 2
}

variable "key_name" {
  description = "Nombre de la key pair para SSH"
  type        = string
  default     = "aq-key5" # Asegúrate de crear esta key en AWS
}

variable "vpc_cidr" {
  description = "CIDR de la VPC"
  type        = string
  default     = "10.1.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR de la Subnet"
  type        = string
  default     = "10.1.1.0/24"
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}