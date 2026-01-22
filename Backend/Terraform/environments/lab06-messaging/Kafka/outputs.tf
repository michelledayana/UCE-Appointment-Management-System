output "vpc_id" {
  value = aws_vpc.kafka_vpc.id
}

output "public_subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "zookeeper_public_ip" {
  value = aws_instance.zookeeper.public_ip
}

output "kafka_public_ip" {
  value = aws_instance.kafka.public_ip
}

output "kafka_sg_id" {
  value = aws_security_group.kafka_sg.id
}
