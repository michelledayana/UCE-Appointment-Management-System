variable "my_ip" {
  description = "IP pública autorizada para SSH (x.x.x.x/32)"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Key Pair existente en AWS"
  type        = string
}
