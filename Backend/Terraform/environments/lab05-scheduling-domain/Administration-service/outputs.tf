output "instance_id" {
  value = aws_instance.admin_instance.id
}

output "public_ip" {
  value = aws_instance.admin_instance.public_ip
}

output "private_ip" {
  value = aws_instance.admin_instance.private_ip
}

output "security_group_id" {
  value = aws_security_group.admin_sg.id
}

output "subnet_id" {
  value = aws_subnet.admin_subnet.id
}

output "vpc_id" {
  value = aws_vpc.admin_vpc.id
}
