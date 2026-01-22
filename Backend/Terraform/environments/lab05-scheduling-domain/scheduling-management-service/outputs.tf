output "instance_id" {
  value = aws_instance.scheduling_instance.id
}

output "private_ip" {
  value = aws_instance.scheduling_instance.private_ip
}

output "public_ip" {
  value = aws_instance.scheduling_instance.public_ip
}

output "security_group_id" {
  value = aws_security_group.scheduling_sg.id
}
