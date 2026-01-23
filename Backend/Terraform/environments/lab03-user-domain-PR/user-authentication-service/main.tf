############################
# Data: VPC y Subnets DEFAULT
############################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

############################
# Security Group
############################
resource "aws_security_group" "authentication_prod" {
  name        = "authentication-sg-prod"
  description = "Security Group User Authentication Service (PROD)"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    description = "User Authentication API"
    from_port   = 8082
    to_port     = 8082
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "authentication-sg-prod"
    Service     = "user-authentication"
    Environment = "production"
  }
}

############################
# Launch Template
############################
resource "aws_launch_template" "auth_lt" {
  name_prefix   = "auth-lt-"
  image_id      = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type = var.instance_type
  key_name      = var.key_name

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.authentication_prod.id]
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ec2-user

    docker pull dayanaheredia/user-authentication-service:latest

    docker run -d \
      --restart always \
      --name user-authentication-service \
      -p 8082:8082 \
      dayanaheredia/user-authentication-service:latest
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "user-authentication-prod"
      Environment = "production"
    }
  }
}

############################
# Auto Scaling Group
############################
resource "aws_autoscaling_group" "auth_asg" {
  name                = "asg-authentication-prod"
  min_size            = 1
  max_size            = 2
  desired_capacity    = 1
  vpc_zone_identifier = data.aws_subnets.default.ids

  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.auth_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "user-authentication-prod"
    propagate_at_launch = true
  }
}
