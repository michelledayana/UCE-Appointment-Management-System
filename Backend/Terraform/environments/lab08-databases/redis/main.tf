provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "redis_sg" {
  name        = "lab9-redis-sg"
  description = "Allow Redis access"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.bastion_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "lab9-redis-sg"
    Env  = "QA"
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "redis" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = var.private_subnet_id
  vpc_security_group_ids = [aws_security_group.redis_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras enable redis6
              yum install redis -y
              sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' /etc/redis.conf
              systemctl enable redis
              systemctl start redis
              EOF

  tags = {
    Name = "lab9-redis"
    Env  = "QA"
  }
}
