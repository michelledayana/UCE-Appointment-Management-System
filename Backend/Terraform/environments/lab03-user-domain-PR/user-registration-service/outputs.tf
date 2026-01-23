output "instance_id" {
  value = aws_instance.user_register_instance.id
}

output "public_ip" {
  value = aws_instance.user_register_instance.public_ip
}

output "private_ip" {
  value = aws_instance.user_register_instance.private_ip
}

output "security_group_id" {
  value = aws_security_group.register_sg_prod.id
}
