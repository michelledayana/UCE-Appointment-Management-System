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
  default     = "qa-key4"
}

variable "vpc_id" {
  description = "ID de la VPC donde se desplegarán los recursos"
  type        = string
  default     = "vpc-062dba627e9014a42"  # VPC pública QA
}

variable "subnet_id" {
  description = "ID de la Subnet dentro de la VPC"
  type        = string
  default     = "subnet-02a50bf2703966d77" # Subnet pública QA
}

variable "my_ip" {
  description = "IP pública autorizada para acceso SSH"
  type        = string
  default     = "190.11.3.161/32" # Cambia a tu IP actual
}
