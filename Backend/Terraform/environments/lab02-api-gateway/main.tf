
# =========================
# VPC
# =========================
resource "aws_vpc" "api_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "api-vpc" }
}

# =========================
# INTERNET GATEWAY
# =========================
resource "aws_internet_gateway" "api_igw" {
  vpc_id = aws_vpc.api_vpc.id
  tags   = { Name = "api-igw" }
}

# =========================
# ROUTE TABLE PUBLICA
# =========================
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.api_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.api_igw.id
  }
  tags = { Name = "public-rt" }
}

# =========================
# SUBNETS PUBLICAS
# =========================
resource "aws_subnet" "subnet_a" {
  vpc_id                  = aws_vpc.api_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = { Name = "subnet-a" }
}

resource "aws_subnet" "subnet_b" {
  vpc_id                  = aws_vpc.api_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = { Name = "subnet-b" }
}

# =========================
# ASOCIACIONES TABLA DE RUTAS
# =========================
resource "aws_route_table_association" "subnet_a_assoc" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "subnet_b_assoc" {
  subnet_id      = aws_subnet.subnet_b.id
  route_table_id = aws_route_table.public_rt.id
}

# =========================
# SECURITY GROUP
# =========================
resource "aws_security_group" "api_sg" {
  name        = "api-sg"
  description = "SG para API Gateway"
  vpc_id      = aws_vpc.api_vpc.id

  ingress {
    description      = "SSH desde tu IP"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = [var.my_ip]
  }

  ingress {
    description = "HTTP para LB"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "api-sg" }
}

# =========================
# EC2 INSTANCE
# =========================
resource "aws_instance" "api_instance" {
  ami                         = "ami-0771b6766e1e61632" # Amazon Linux 2
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.subnet_a.id
  associate_public_ip_address = true
  key_name                    = "aq-key6" # Tu key pair de AWS
  vpc_security_group_ids      = [aws_security_group.api_sg.id]

  user_data = <<-EOT
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -a -G docker ec2-user
  EOT

  tags = { Name = "API-Gateway-Instance" }
}

# =========================
# LOAD BALANCER
# =========================
resource "aws_lb" "api_lb" {
  name               = "api-gateway-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
  security_groups    = [aws_security_group.api_sg.id]
  enable_http2       = true
  idle_timeout       = 60

  tags = { Name = "API-Gateway-LB" }
}

# =========================
# TARGET GROUP
# =========================
resource "aws_lb_target_group" "api_tg" {
  name     = "api-gateway-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.api_vpc.id
  target_type = "instance"

  health_check {
    path                = "/"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 2
    timeout             = 5
    matcher             = "200"
  }
}

# =========================
# ATTACH INSTANCE TO TG
# =========================
resource "aws_lb_target_group_attachment" "api_attachment" {
  target_group_arn = aws_lb_target_group.api_tg.arn
  target_id        = aws_instance.api_instance.id
  port             = 8080
}

# =========================
# LB LISTENER
# =========================
resource "aws_lb_listener" "api_listener" {
  load_balancer_arn = aws_lb.api_lb.arn
  port              = 8080
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_tg.arn
  }
}

