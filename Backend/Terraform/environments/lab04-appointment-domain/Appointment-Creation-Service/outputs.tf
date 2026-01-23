##################################################
# Outputs
##################################################
output "instance_id" {
  value = aws_instance.instance.id
}

output "public_ip" {
  value = aws_instance.instance.public_ip
}

output "private_ip" {
  value = aws_instance.instance.private_ip
}

output "security_group_id" {
  value = aws_security_group.sg.id
}

output "subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "vpc_id" {
  value = aws_vpc.vpc.id
}
