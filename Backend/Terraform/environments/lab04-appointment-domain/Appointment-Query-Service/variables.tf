variable "vpc_id" {
  description = "ID de la VPC donde se desplegarán los recursos"
  type        = string
}

variable "subnet_id" {
  description = "ID de la Subnet dentro de la VPC"
  type        = string
}

variable "ami" {
  description = "AMI para la instancia EC2"
  type        = string
  default     = "ami-0c02fb55956c7d316" # Amazon Linux 2
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Nombre de la key pair para SSH"
  type        = string
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}
