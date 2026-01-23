
##################################################
# VPC
##################################################
resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = "Appointment-Creation-Service-VPC" }
}

##################################################
# Internet Gateway
##################################################
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = { Name = "Appointment-Creation-Service-IGW" }
}

##################################################
# Public Subnet
##################################################
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = { Name = "Appointment-Creation-Service-Subnet" }
}

##################################################
# Route Table y asociación
##################################################
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = { Name = "Appointment-Creation-Service-Public-RT" }
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

##################################################
# Security Group
##################################################
resource "aws_security_group" "sg" {
  name        = "Appointment-Creation-Service-SG"
  description = "Permite SSH y puerto microservicio"
  vpc_id      = aws_vpc.vpc.id

  # SSH solo desde tu IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
    description = "SSH desde mi IP"
  }

  # Puerto microservicio abierto a todo
  ingress {
    from_port   = 8087
    to_port     = 8087
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

  tags = { Name = "Appointment-Creation-Service-SG" }
}

##################################################
# Network ACL (permitiendo todo tráfico)
##################################################
resource "aws_network_acl" "nacl" {
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  egress {
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = { Name = "Appointment-Creation-Service-NACL" }
}

resource "aws_network_acl_association" "nacl_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  network_acl_id = aws_network_acl.nacl.id
}

##################################################
# EC2 Instance
##################################################
resource "aws_instance" "instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public_subnet.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.sg.id]
  key_name                    = var.key_name

  tags = { Name = "appointment-creation-service" }  # Nombre exacto de la instancia
}

