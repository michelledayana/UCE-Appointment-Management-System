output "user_registration_elastic_ip" {
  description = "Elastic IP assigned to the Network Load Balancer (QA)"
  value       = aws_eip.user_registration_nlb_eip.public_ip
}

output "user_registration_nlb_dns" {
  description = "DNS name of the User Registration NLB"
  value       = aws_lb.user_registration_nlb.dns_name
}
