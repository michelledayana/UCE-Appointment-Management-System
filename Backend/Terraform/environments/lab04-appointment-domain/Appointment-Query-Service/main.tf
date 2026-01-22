
# Security Group
resource "aws_security_group" "query_sg" {
  name        = "Appointment-Query-Service"
  description = "Permitir SSH y puerto 8089"
  vpc_id      = var.vpc_id

  ingress {
    description = "Puerto microservicio"
    from_port   = 8089
    to_port     = 8089
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
    Name = "Appointment-Query-Service"
  }
}

# EC2 Instance
resource "aws_instance" "query_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.query_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "Appointment-Query-Service"
  }
}
