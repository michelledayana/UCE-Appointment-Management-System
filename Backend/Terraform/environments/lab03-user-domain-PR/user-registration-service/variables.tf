variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "my_ip" {
  type = string
}

variable "key_name" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
