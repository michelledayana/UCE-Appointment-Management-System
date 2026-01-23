# -------------------------------
# Security Group para Appointment-Query-Service
# -------------------------------
resource "aws_security_group" "query_sg" {
  name        = "Appointment-Query-Service"
  description = "Permitir SSH y puerto 8089"
  vpc_id      = var.vpc_id

  # SSH desde tu IP
  ingress {
    description = "SSH desde mi IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Puerto del microservicio abierto al mundo
  ingress {
    description = "Puerto microservicio"
    from_port   = 8089
    to_port     = 8089
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Salida a internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Appointment-Query-Service"
  }
}

# -------------------------------
# EC2 Instance (solo una)
# -------------------------------
resource "aws_instance" "query_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.query_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  tags = {
    Name = "appointment-query-service"
  }
}
