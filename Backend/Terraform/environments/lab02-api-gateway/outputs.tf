output "alb_dns" {
  description = "DNS name of the API Gateway ALB"
  value       = aws_lb.api_gateway_alb.dns_name
}

output "api_gateway_instance_id" {
  description = "ID of the API Gateway EC2 instance"
  value       = aws_instance.api_gateway.id
}

output "api_gateway_public_ip" {
  description = "Public IP of API Gateway EC2 instance"
  value       = aws_eip.api_gateway_eip.public_ip
}
