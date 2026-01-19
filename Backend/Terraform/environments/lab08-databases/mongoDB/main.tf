# Security Group para MongoDB
resource "aws_security_group" "mongo_sg" {
  name        = "mongo-sg"
  description = "Security group for MongoDB EC2"
  vpc_id      = var.vpc_id

  # SSH desde Bastion
  ingress {
    description = "SSH access from Bastion"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.bastion_public_ip_cidr]
  }

  # MongoDB (27017) acceso desde VPC
  ingress {
    description = "MongoDB access from VPC"
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Ajusta según tu rango de VPC
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mongo-sg"
  }
}

# Instancia EC2 pública para MongoDB
resource "aws_instance" "mongo" {
  ami                         = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type               = "t3.micro"
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [aws_security_group.mongo_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              docker pull mongo:6
              docker run -d --name mongodb -p 27017:27017 \
                  -e MONGO_INITDB_DATABASE=appointments_db \
                  -e MONGO_INITDB_ROOT_USERNAME=admin \
                  -e MONGO_INITDB_ROOT_PASSWORD=adminpass mongo:6
EOF

  tags = {
    Name = "mongo-ec2"
    Role = "database"
  }
}

# Elastic IP para MongoDB
resource "aws_eip" "mongo_eip" {
  vpc      = true            # indica que es en la VPC existente
  instance = aws_instance.mongo.id
  tags = {
    Name = "mongo-eip"
  }
}
