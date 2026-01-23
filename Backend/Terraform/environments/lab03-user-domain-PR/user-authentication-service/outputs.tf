output "security_group_id" {
  value = aws_security_group.authentication_prod.id
}

output "launch_template_id" {
  value = aws_launch_template.auth_lt.id
}

output "autoscaling_group_name" {
  value = aws_autoscaling_group.auth_asg.name
}
