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
  default     = "aq-key4" # Tu keypair existente
}

variable "vpc_id" {
  description = "ID de la VPC donde se desplegarán los recursos"
  type        = string
  default     = "vpc-04bcf1d30127c5d10"  # <-- ID de VPC de Appointment-Creation-Service
}

variable "subnet_id" {
  description = "ID de la Subnet dentro de la VPC"
  type        = string
  default     = "subnet-0e0369897262e0289" # <-- ID de Subnet de Appointment-Creation-Service
}

variable "my_ip" {
  description = "IP pública autorizada para acceso al microservicio"
  type        = string
}
