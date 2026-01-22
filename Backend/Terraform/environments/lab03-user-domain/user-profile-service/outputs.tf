output "instance_id" {
  value = aws_instance.user_profile_instance.id
}

output "private_ip" {
  value = aws_instance.user_profile_instance.private_ip
}

output "security_group_id" {
  value = aws_security_group.profile_sg.id
}

output "subnet_id" {
  value = var.subnet_id
}

output "vpc_id" {
  value = var.vpc_id
}
