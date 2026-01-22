################################
# SECURITY GROUP
################################
resource "aws_security_group" "registration_sg" {
  name        = "registration-sg"
  description = "Permitir SSH y puerto 8081"
  vpc_id      = var.vpc_id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
    description = "SSH desde IP autorizada"
  }

  # Microservicio
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Puerto del microservicio"
  }

  # Salida total
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "registration-sg"
  }
}

################################
# EC2 INSTANCE
################################
resource "aws_instance" "user_registration_instance" {
  ami                         = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.registration_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "user-registration-instance"
  }
}
