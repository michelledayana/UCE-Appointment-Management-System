################################
# PROVIDER
################################
provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project = "UAMS-UCE"
      Owner   = "Heredia"
      Env     = "QA"
    }
  }
}

################################
# DATA
################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

################################
# SECURITY GROUP
################################
resource "aws_security_group" "user_registration_sg" {
  name   = "user-registration-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    description = "User Registration Service"
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH (only for QA / Bastion)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

################################
# ELASTIC IP (QA – 1 AZ)
################################
resource "aws_eip" "user_registration_nlb_eip" {
  domain = "vpc"
}

################################
# NETWORK LOAD BALANCER (QA – SINGLE AZ)
################################
resource "aws_lb" "user_registration_nlb" {
  name               = "user-registration-nlb"
  load_balancer_type = "network"
  internal           = false

  subnet_mapping {
    subnet_id     = data.aws_subnets.default.ids[0]
    allocation_id = aws_eip.user_registration_nlb_eip.id
  }
}

################################
# TARGET GROUP
################################
resource "aws_lb_target_group" "user_registration_tg" {
  name     = "user-registration-tg"
  port     = 8081
  protocol = "TCP"
  vpc_id   = data.aws_vpc.default.id

  health_check {
    protocol = "TCP"
  }
}

################################
# LISTENER
################################
resource "aws_lb_listener" "user_registration_listener" {
  load_balancer_arn = aws_lb.user_registration_nlb.arn
  port              = 8081
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.user_registration_tg.arn
  }
}

################################
# LAUNCH TEMPLATE
################################
resource "aws_launch_template" "user_registration_lt" {
  name_prefix   = "user-registration-lt-"
  image_id = "ami-0b72821e2f351e396" # Amazon Linux 2023 
  instance_type = "t2.micro"

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.user_registration_sg.id]
  }

  user_data = base64encode(<<EOF
#!/bin/bash
set -e

# Actualizar sistema
dnf update -y

# Instalar Docker (FORMA CORRECTA)
dnf install -y docker

# Habilitar Docker
systemctl enable docker
systemctl start docker

# Esperar a que Docker levante
sleep 10

# Descargar imagen
docker pull dayanaheredia/user-registration-service:latest

# Ejecutar contenedor
docker run -d \
  --name user-registration-service \
  --restart always \
  -p 8081:8081 \
  dayanaheredia/user-registration-service:latest
EOF
)

}

################################
# AUTO SCALING GROUP (QA – 1 AZ)
################################
resource "aws_autoscaling_group" "user_registration_asg" {
  name             = "user-registration-asg"
  min_size         = 1
  desired_capacity = 1
  max_size         = 2

  vpc_zone_identifier = [
    data.aws_subnets.default.ids[0]
  ]

  target_group_arns = [
    aws_lb_target_group.user_registration_tg.arn
  ]

  launch_template {
    id      = aws_launch_template.user_registration_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "user-registration-service"
    propagate_at_launch = true
  }
}
