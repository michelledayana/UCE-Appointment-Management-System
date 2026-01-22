output "instance_id" {
  value = aws_instance.user_auth_instance.id
}

output "public_ip" {
  value = aws_instance.user_auth_instance.public_ip
}

output "private_ip" {
  value = aws_instance.user_auth_instance.private_ip
}

output "security_group_id" {
  value = aws_security_group.sg_authentication.id
}
