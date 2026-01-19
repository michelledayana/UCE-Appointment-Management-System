variable "project_name" {
  type    = string
  default = "appointment"
}

variable "environment" {
  type    = string
  default = "qa"
}
variable "my_ip" {
  description = "Public IP allowed to SSH into bastion"
  type        = string
}

