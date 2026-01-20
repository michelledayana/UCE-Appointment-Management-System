data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "mqtt_sg" {
  name        = "mqtt-sg"
  description = "Security group for MQTT broker"
  vpc_id      = data.aws_vpc.default.id

  # 🔐 SSH
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 📡 MQTT
  ingress {
    description = "MQTT"
    from_port   = var.mqtt_port
    to_port     = var.mqtt_port
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  # 🌍 Outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mqtt-sg"
  }
}

resource "aws_instance" "mqtt_broker" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.mqtt_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras enable epel
    yum install -y mosquitto
    systemctl enable mosquitto
    systemctl start mosquitto
  EOF

  tags = {
    Name = "mqtt-broker"
  }
}
