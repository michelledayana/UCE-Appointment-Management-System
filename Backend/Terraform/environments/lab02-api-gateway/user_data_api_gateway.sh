#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -aG docker ec2-user

# Levantar API Gateway (Docker)
docker pull ${docker_image}
docker run -d --name api-gateway -p 80:80 ${docker_image}
