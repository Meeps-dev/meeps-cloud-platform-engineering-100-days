# Day 11: Launch EC2 in Public Subnet

## Goal

Launch an EC2 instance inside the public subnet and serve a basic Nginx page.

## EC2 Details

- Instance name: meeps-public-ec2
- VPC: meeps-week2-vpc
- Subnet: meeps-public-subnet
- Public IP: Enabled
- OS: Ubuntu Server
- Instance type: t2.micro or t3.micro

## Security Group Rules

### Inbound Rules

- SSH, TCP, Port 22, Source: My IP
- HTTP, TCP, Port 80, Source: Anywhere IPv4

## Commands Used

sudo apt update
sudo apt install nginx -y
sudo systemctl status nginx

# What i learned

EC2 instances run inside a VPC and subnet.

A public EC2 instance needs a public subnet, public IP address, route to an Internet Gateway, and correct Security Group rules.

SSH on port 22 allows server management.

HTTP on port 80 allows browser access to the web server.
