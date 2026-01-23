
############################
# Security Group
############################
resource "aws_security_group" "profile_sg_prod" {
  name        = "profile-sg-prod"
  description = "Security Group User Profile Service (PROD)"
  vpc_id      = var.vpc_id

  ingress {
    description = "User Profile API"
    from_port   = 8083
    to_port     = 8083
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "profile-sg-prod"
    Service     = "user-profile"
    Environment = "production"
  }
}

############################
# Launch Template
############################
resource "aws_launch_template" "profile_lt" {
  name_prefix   = "profile-lt-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = var.instance_type
  key_name      = var.key_name

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.profile_sg_prod.id]
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ec2-user

    docker pull dayanaheredia/user-profile-service:latest

    docker run -d \
      --restart always \
      --name user-profile-service \
      -p 8083:8083 \
      dayanaheredia/user-profile-service:latest
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "user-profile-prod"
      Environment = "production"
    }
  }
}

############################
# Auto Scaling Group
############################
resource "aws_autoscaling_group" "profile_asg" {
  name                      = "asg-profile-prod"
  min_size                  = 1
  max_size                  = 2
  desired_capacity          = 1
  health_check_type         = "EC2"
  health_check_grace_period = 300

  vpc_zone_identifier = var.subnet_ids

  launch_template {
    id      = aws_launch_template.profile_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "user-profile-prod"
    propagate_at_launch = true
  }
}
