# -------------------------------
# VPC
# -------------------------------
resource "aws_vpc" "microservice_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "Appointment-Creation-Service-VPC"
  }
}

# -------------------------------
# Subnet
# -------------------------------
resource "aws_subnet" "microservice_subnet" {
  vpc_id                  = aws_vpc.microservice_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "Appointment-Creation-Service-Subnet"
  }
}

# -------------------------------
# Security Group
# -------------------------------
resource "aws_security_group" "creation_sg" {
  name        = "Appointment-Creation-Service"
  description = "Permitir SSH y puerto 8087"
  vpc_id      = aws_vpc.microservice_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
    description = "SSH"
  }

  ingress {
    from_port   = 8087
    to_port     = 8087
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Puerto microservicio"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Appointment-Creation-Service"
  }
}

# -------------------------------
# EC2 Instance
# -------------------------------
resource "aws_instance" "creation_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.microservice_subnet.id
  vpc_security_group_ids      = [aws_security_group.creation_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "Appointment-Creation-Service"
  }
}
