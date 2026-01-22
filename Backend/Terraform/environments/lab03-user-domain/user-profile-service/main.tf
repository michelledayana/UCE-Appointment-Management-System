# Security Group
resource "aws_security_group" "profile_sg" {
  name        = "profile-sg"
  description = "Permitir SSH y puerto 8083"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
    description = "SSH"
  }

  ingress {
    from_port   = 8083
    to_port     = 8083
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Puerto microservicio"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "profile-sg"
  }
}

# EC2 Instance
resource "aws_instance" "user_profile_instance" {
  ami                         = "ami-0c02fb55956c7d316"
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.profile_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "user-profile-instance"
  }
}
