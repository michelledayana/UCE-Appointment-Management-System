output "mqtt_private_ip" {
  description = "Private IP of MQTT Broker"
  value       = aws_instance.mqtt_broker.private_ip
}

output "mqtt_public_ip" {
  description = "Public Elastic IP of MQTT Broker"
  value       = data.aws_eip.mqtt_existing.public_ip
}
