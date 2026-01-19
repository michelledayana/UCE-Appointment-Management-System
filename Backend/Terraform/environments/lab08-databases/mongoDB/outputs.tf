output "mongo_public_ip" {
  description = "Public IP (Elastic) of MongoDB EC2"
  value       = aws_eip.mongo_eip.public_ip
}

output "mongo_private_ip" {
  description = "Private IP of MongoDB EC2"
  value       = aws_instance.mongo.private_ip
}

output "mongo_sg_id" {
  description = "Security Group ID for MongoDB"
  value       = aws_security_group.mongo_sg.id
}
