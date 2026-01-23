# -------------------------------
# Security Group para Appointment-Management-Service
# -------------------------------
resource "aws_security_group" "management_sg" {
  name        = "Appointment-Management-Service"
  description = "Permitir SSH y puerto 8088"
  vpc_id      = var.vpc_id

  # SSH desde tu IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
    description = "SSH desde mi IP"
  }

  # Puerto del microservicio abierto al mundo
  ingress {
    from_port   = 8088
    to_port     = 8088
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Puerto microservicio"
  }

  # Salida a internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Appointment-Management-Service"
  }
}

# -------------------------------
# EC2 Instance
# -------------------------------
resource "aws_instance" "management_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.management_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "appointment-management-service"
  }
}
