output "profile_security_group_id" {
  value = aws_security_group.profile_sg_prod.id
}

output "profile_launch_template_id" {
  value = aws_launch_template.profile_lt.id
}

output "profile_autoscaling_group_name" {
  value = aws_autoscaling_group.profile_asg.name
}
