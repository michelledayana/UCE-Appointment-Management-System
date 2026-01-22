output "redis_public_ip" {
  value = aws_instance.redis_instance.public_ip
}

output "redis_private_ip" {
  value = aws_instance.redis_instance.private_ip
}
