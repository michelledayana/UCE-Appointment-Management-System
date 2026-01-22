# =========================
# VPC
# =========================
resource "aws_vpc" "mqtt_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "mqtt-vpc" }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.mqtt_vpc.id
  tags = { Name = "mqtt-igw" }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.mqtt_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "mqtt-public-rt" }
}

# Subnet pública
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.mqtt_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "mqtt-public-subnet" }
}

# Asociar Route Table a Subnet
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# =========================
# Security Group
# =========================
resource "aws_security_group" "mqtt_sg" {
  name        = "mqtt-sg"
  description = "MQTT SG - SSH desde mi IP, MQTT interno"
  vpc_id      = aws_vpc.mqtt_vpc.id

  # SSH desde tu IP pública
  ingress {
    description = "SSH from my public IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # MQTT interno dentro de la VPC
  ingress {
    description = "MQTT port"
    from_port   = var.mqtt_port
    to_port     = var.mqtt_port
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  # Egress abierto
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "mqtt-sg" }
}

# =========================
# Traer Elastic IP existente
# =========================
data "aws_eip" "mqtt_existing" {
  public_ip = var.elastic_ip
}

# =========================
# Instancia MQTT
# =========================
resource "aws_instance" "mqtt_broker" {
  ami                         = "ami-0c02fb55956c7d316"
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.mqtt_sg.id]
  associate_public_ip_address = true

  tags = { Name = "mqtt-broker" }

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras enable epel
    yum install -y mosquitto
    systemctl enable mosquitto
    systemctl start mosquitto
  EOF
}

# =========================
# Asociar Elastic IP existente
# =========================
resource "aws_eip_association" "mqtt_eip_assoc" {
  instance_id   = aws_instance.mqtt_broker.id
  allocation_id = data.aws_eip.mqtt_existing.id
}
