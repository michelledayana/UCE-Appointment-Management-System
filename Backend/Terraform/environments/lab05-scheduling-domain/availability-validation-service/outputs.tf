output "availability_instance_id" {
  description = "ID de la instancia del microservicio"
  value       = aws_instance.availability_instance.id
}

output "availability_private_ip" {
  description = "IP privada de la instancia"
  value       = aws_instance.availability_instance.private_ip
}

output "availability_public_ip" {
  description = "IP pública de la instancia"
  value       = aws_instance.availability_instance.public_ip
}

output "availability_sg_id" {
  description = "ID del Security Group del microservicio"
  value       = aws_security_group.availability_sg.id
}
