# Security Group para user-authentication-service
resource "aws_security_group" "sg_authentication" {
  name        = "sg_authentication"
  description = "Security group for user authentication service"
  vpc_id      = var.vpc_id

  # Regla de entrada para SSH
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Regla de entrada para el puerto del microservicio
  ingress {
    description = "Authentication service port"
    from_port   = 8082
    to_port     = 8082
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Salida de todo el tráfico
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg_authentication"
  }
}

# EC2 Instance
resource "aws_instance" "user_auth_instance" {
  ami                         = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.sg_authentication.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "user-authentication-instance"
  }
}
