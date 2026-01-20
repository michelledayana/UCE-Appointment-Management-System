# -----------------------------
# SECURITY GROUP - MONGODB
# -----------------------------
resource "aws_security_group" "mongo_sg" {
  name        = "mongo-public-sg"
  description = "Public MongoDB access"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    description = "MongoDB from my IP"
    from_port   = 27017
    to_port     = 27017
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
    Name = "mongo-public-sg"
  }
}

# -----------------------------
# EC2 INSTANCE - MONGODB
# -----------------------------
resource "aws_instance" "mongo" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type = "t3.micro"

  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [aws_security_group.mongo_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "mongo-instance"
  }
}
