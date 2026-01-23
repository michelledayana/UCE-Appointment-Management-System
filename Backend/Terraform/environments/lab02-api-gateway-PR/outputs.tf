# =========================
# OUTPUTS
# =========================
output "instance_id" {
  value = aws_instance.api_instance.id
}

output "instance_public_ip" {
  value = aws_instance.api_instance.public_ip
}

output "lb_dns_name" {
  value = aws_lb.api_lb.dns_name
}

output "vpc_id" {
  value = aws_vpc.api_vpc.id
}
