# Day 8: Created a Custom VPC

## Goal

Create a custom Virtual Private Cloud in AWS.

## VPC Details

- VPC Name: meeps-week2-vpc
- CIDR Block: 10.0.0.0/16
- IPv6: Disabled
- Tenancy: Default

## What I Learned

A VPC is a private network inside AWS where cloud resources are deployed.

The CIDR block defines the private IP address range available inside the VPC.

I used 10.0.0.0/16 because it gives enough private IP addresses for learning how to split the network into public and private subnets later.

## Result

The VPC was created successfully and is now available.
