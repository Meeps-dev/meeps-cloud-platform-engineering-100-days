# Day 12: Launch EC2 in Private Subnet

## Goal

Launch an EC2 instance inside a private subnet without a public IP address.

## EC2 Details

- Instance name: meeps-private-ec2
- VPC: meeps-week2-vpc
- Subnet: meeps-private-subnet
- Public IP: Disabled
- Private IP: 10.0.2.x
- OS: Ubuntu Server
- Instance type: t2.micro or t3.micro

## Security Group

Inbound access was restricted.

SSH was not opened to the internet.

The private EC2 was configured to allow internal access only from the public EC2 security group.

## Route Table Check

The private subnet does not have this route:

0.0.0.0/0 → Internet Gateway

It only uses the local VPC route:

10.0.0.0/16 → local

## What I Learned

A private EC2 instance should not have a public IP address.

Private servers are protected because they are placed in private subnets and are not directly reachable from the internet.

Databases, workers, and internal backend services should usually live in private subnets.
