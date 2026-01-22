# Security Group para el microservicio
resource "aws_security_group" "scheduling_sg" {
  name        = "${var.service_name}-sg"
  description = "Security group para ${var.service_name}"
  vpc_id      = var.vpc_id

  # Puerto del microservicio
  ingress {
    from_port   = var.service_port
    to_port     = var.service_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH
  ingress {
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
    Name = "${var.service_name}-sg"
  }
}

# Instancia EC2 del microservicio
resource "aws_instance" "scheduling_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.scheduling_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = var.service_name
  }
}
