output "mqtt_private_ip" {
  description = "Private IP of MQTT Broker"
  value       = aws_instance.mqtt_broker.private_ip
}
