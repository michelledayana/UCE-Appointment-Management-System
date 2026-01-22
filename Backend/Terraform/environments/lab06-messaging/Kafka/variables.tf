variable "aws_region" {
  default = "us-east-1"
}

variable "key_name" {
  description = "Key pair para EC2"
  type        = string
}

variable "my_ip" {
  description = "IP desde la cual permitimos SSH"
  type        = string
}
