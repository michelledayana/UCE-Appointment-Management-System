#!/bin/bash
yum update -y

# Docker
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# MongoDB
docker volume create mongo_data

docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongo_data:/data/db \
  mongo:latest
