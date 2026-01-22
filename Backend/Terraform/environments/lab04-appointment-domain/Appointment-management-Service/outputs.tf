output "instance_id" {
  description = "ID de la instancia EC2"
  value       = aws_instance.management_instance.id
}

output "private_ip" {
  description = "IP privada de la instancia"
  value       = aws_instance.management_instance.private_ip
}

output "public_ip" {
  description = "IP pública de la instancia"
  value       = aws_instance.management_instance.public_ip
}

output "security_group_id" {
  description = "ID del Security Group"
  value       = aws_security_group.management_sg.id
}
