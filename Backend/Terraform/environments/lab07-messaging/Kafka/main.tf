
# =========================
# VPC
# =========================
resource "aws_vpc" "kafka_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "kafka-vpc" }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.kafka_vpc.id
  tags = { Name = "kafka-igw" }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.kafka_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "public-rt" }
}

# Subnet pública
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.kafka_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "public-subnet" }
}

# Asociar Route Table a Subnet
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# =========================
# Security Group
# =========================
resource "aws_security_group" "kafka_sg" {
  name        = "kafka-sg"
  description = "Kafka SG (private, allow SSH from my IP)"
  vpc_id      = aws_vpc.kafka_vpc.id

  ingress {
    description      = "SSH"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = [var.my_ip]  # Usando la variable sin espacios
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "kafka-sg"
  }
}

# =========================
# Zookeeper Instance
# =========================
resource "aws_instance" "zookeeper" {
  ami                         = "ami-0a3c3a20c09d6f377"
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public_subnet.id
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true

  tags = { Name = "zookeeper-instance" }

  user_data = <<-EOT
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user

              docker run -d \
                --name zookeeper \
                -p 2181:2181 \
                confluentinc/cp-zookeeper:7.5.0
            EOT
}

# =========================
# Kafka Instance
# =========================
resource "aws_instance" "kafka" {
  ami                         = "ami-0a3c3a20c09d6f377"
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public_subnet.id
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true

  depends_on = [aws_instance.zookeeper]

  tags = { Name = "kafka-instance" }

  user_data = <<-EOT
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user

              docker run -d \
                --name kafka \
                -p 9092:9092 \
                -e KAFKA_ZOOKEEPER_CONNECT=${aws_instance.zookeeper.private_ip}:2181 \
                -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
                -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
                confluentinc/cp-kafka:7.5.0
            EOT
}
