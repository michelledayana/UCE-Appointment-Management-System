output "api_gateway_instance_id" {
  value = aws_instance.api_gateway.id
}

output "alb_dns" {
  value = aws_lb.api_gateway_alb.dns_name
}

output "eip" {
  value = aws_eip.api_gateway_eip.public_ip
}
