# Day 9: Created Public and Private Subnets

## Goal

Create two subnets inside my custom VPC.

## VPC Used

- VPC Name: meeps-week2-vpc
- VPC CIDR: 10.0.0.0/16

## Subnets Created

### Public Subnet

- Name: meeps-public-subnet
- CIDR: 10.0.1.0/24
- Auto-assign public IPv4: Enabled

### Private Subnet

- Name: meeps-private-subnet
- CIDR: 10.0.2.0/24
- Auto-assign public IPv4: Disabled

## What I Learned

A subnet is a smaller network inside a VPC.

The public subnet is designed for resources that may need internet access, such as a load balancer or public web server.

The private subnet is designed for internal resources that should not be directly exposed to the internet, such as databases, workers, and backend services.

## Result

Both subnets were created successfully inside the custom VPC.
