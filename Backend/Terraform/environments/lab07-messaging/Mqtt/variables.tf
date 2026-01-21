variable "aws_region" {
  description = "Región donde se desplegarán los recursos AWS"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "Key pair para acceder a EC2 vía SSH"
  type        = string
}

variable "my_ip" {
  description = "IP pública desde la cual permitimos SSH"
  type        = string
}

variable "elastic_ip" {
  description = "Elastic IP existente para la instancia MQTT"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
}

variable "mqtt_port" {
  description = "Puerto MQTT"
  type        = number
  default     = 1883
}
