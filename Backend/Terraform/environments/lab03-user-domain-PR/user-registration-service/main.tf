############################
# SECURITY GROUP
############################
resource "aws_security_group" "register_sg_prod" {
  name        = "register-sg-prod"
  description = "Security Group User Register Service (PROD)"
  vpc_id      = var.vpc_id

  ingress {
    description = "User Register API"
    from_port   = 8081
    to_port     = 8081
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
    Name        = "register-sg-prod"
    Environment = "production"
    Service     = "user-register"
  }
}

############################
# EC2 INSTANCE (IGUAL QUE LOS OTROS)
############################
resource "aws_instance" "user_register_instance" {
  ami                         = "ami-0c02fb55956c7d316"
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_ids[0]
  vpc_security_group_ids      = [aws_security_group.register_sg_prod.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ec2-user

    docker pull dayanaheredia/user-register-service:latest

    docker run -d \
      --restart always \
      --name user-register-service \
      -p 8081:8081 \
      dayanaheredia/user-register-service:latest
  EOF

  tags = {
    Name        = "user-register-prod"
    Environment = "production"
    Service     = "user-register"
  }
}
