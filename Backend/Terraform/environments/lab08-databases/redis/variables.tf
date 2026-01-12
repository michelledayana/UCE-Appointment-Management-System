variable "vpc_id" {}
variable "private_subnet_id" {}
variable "bastion_sg_id" {}

variable "instance_type" {
  default = "t3.micro"
}