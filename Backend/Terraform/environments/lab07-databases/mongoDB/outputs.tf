output "mongo_public_ip" {
  description = "Public IP of MongoDB instance"
  value       = aws_instance.mongo.public_ip
}

output "mongo_private_ip" {
  description = "Private IP of MongoDB instance"
  value       = aws_instance.mongo.private_ip
}

output "mongo_sg_id" {
  description = "Security group ID"
  value       = aws_security_group.mongo_sg.id
}
