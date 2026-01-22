# ---- VPC ----
resource "aws_vpc" "admin_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "Administration-service-VPC"
  }
}

# ---- Subnet ----
resource "aws_subnet" "admin_subnet" {
  vpc_id                  = aws_vpc.admin_vpc.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "Administration-service-Subnet"
  }
}

# ---- Security Group ----
resource "aws_security_group" "admin_sg" {
  name        = "Administration-service"
  description = "Permitir SSH y puerto 8090"
  vpc_id      = aws_vpc.admin_vpc.id

  ingress {
    description = "Puerto microservicio"
    from_port   = 8090
    to_port     = 8090
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
    Name = "Administration-service"
  }
}

# ---- EC2 Instance ----
resource "aws_instance" "admin_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.admin_subnet.id
  vpc_security_group_ids      = [aws_security_group.admin_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "Administration-service"
  }
}
