provider "aws" {
  region = var.aws_region
}

# -----------------------------
# Security Group para Redis
# -----------------------------
resource "aws_security_group" "redis_sg" {
  name        = "redis-public-sg"
  description = "Allow SSH and Redis from my IP"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    description = "Redis from my IP"
    from_port   = 6379
    to_port     = 6379
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
    Name = "redis-public-sg"
  }
}

# -----------------------------
# EC2 Instance Redis
# -----------------------------
resource "aws_instance" "redis_instance" {
  ami                         = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type               = "t3.micro"
  key_name                    = var.key_name
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [aws_security_group.redis_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "redis-instance"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras enable redis6
              yum install -y redis
              systemctl enable redis
              systemctl start redis
              EOF
}



