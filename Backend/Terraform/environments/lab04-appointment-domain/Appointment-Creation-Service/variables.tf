
##################################################
# Variables
##################################################
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
  description = "Nombre del key pair para SSH"
  type        = string
  default     = "qa-key4"
}

variable "my_ip" {
  description = "IP pública autorizada para SSH"
  type        = string
}
