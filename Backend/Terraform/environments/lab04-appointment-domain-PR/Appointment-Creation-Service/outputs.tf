output "instance_id" {
  value = aws_instance.creation_instance.id
}

output "private_ip" {
  value = aws_instance.creation_instance.private_ip
}

output "public_ip" {
  value = aws_instance.creation_instance.public_ip
}

output "security_group_id" {
  value = aws_security_group.creation_sg.id
}

output "subnet_id" {
  value = aws_subnet.microservice_subnet.id
}

output "vpc_id" {
  value = aws_vpc.microservice_vpc.id
}
