output "instance_id" {
  description = "ID de la instancia EC2"
  value       = aws_instance.user_registration_instance.id
}

output "public_ip" {
  description = "IP pública para SSH"
  value       = aws_instance.user_registration_instance.public_ip
}

output "private_ip" {
  description = "IP privada de la instancia"
  value       = aws_instance.user_registration_instance.private_ip
}

output "security_group_id" {
  description = "ID del Security Group"
  value       = aws_security_group.registration_sg.id
}

output "subnet_id" {
  value = var.subnet_id
}

output "vpc_id" {
  value = var.vpc_id
}
