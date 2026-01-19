output "postgres_public_ip" {
  description = "Public IP of PostgreSQL EC2"
  value       = aws_instance.postgres.public_ip
}

output "postgres_private_ip" {
  description = "Private IP of PostgreSQL EC2"
  value       = aws_instance.postgres.private_ip
}

output "postgres_sg_id" {
  description = "Security Group ID for PostgreSQL"
  value       = aws_security_group.postgres_sg.id
}
