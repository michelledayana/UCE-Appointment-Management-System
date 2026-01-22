output "instance_id" {
  value = aws_instance.catalog_instance.id
}

output "private_ip" {
  value = aws_instance.catalog_instance.private_ip
}

output "public_ip" {
  value = aws_instance.catalog_instance.public_ip
}

output "security_group_id" {
  value = aws_security_group.catalog_sg.id
}
