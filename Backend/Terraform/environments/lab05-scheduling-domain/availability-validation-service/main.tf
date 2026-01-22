# Security Group del microservicio
resource "aws_security_group" "availability_sg" {
  name   = "availability-validation-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 8086
    to_port     = 8086
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Solo para pruebas; en producción restringir al rango necesario
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
    Name = "availability-validation-sg"
  }
}

# Instancia EC2 del microservicio
resource "aws_instance" "availability_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.availability_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "availability-validation-instance"
  }
}
