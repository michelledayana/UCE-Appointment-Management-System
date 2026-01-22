resource "aws_security_group" "postgres_sg" {
  name        = "postgres-sg"
  description = "Security group for PostgreSQL EC2"
  vpc_id      = var.vpc_id

  # SSH desde tu IP (o bastion después)
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # PostgreSQL (por ahora abierto solo a VPC)
  ingress {
    description = "Postgres access from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "postgres-sg"
  }
}

resource "aws_instance" "postgres" {
  ami                         = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type               = "t3.micro"
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [aws_security_group.postgres_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  tags = {
    Name = "postgres-ec2"
    Role = "database"
  }
}
