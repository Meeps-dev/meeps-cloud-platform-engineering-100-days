# Day 10: Internet Gateway and Route Tables

## Goal

Attach an Internet Gateway to my custom VPC and configure a public route table.

## Resources Created

- Internet Gateway: meeps-week2-igw
- Public Route Table: meeps-public-route-table

## Route Added

0.0.0.0/0 → Internet Gateway

### Subnet Association

Public subnet associated with public route table
Private subnet kept separate

### What I Learned

An Internet Gateway connects a VPC to the internet.

A route table controls where network traffic goes.

The route 0.0.0.0/0 means all IPv4 internet traffic.

A subnet becomes public when it has a route to an Internet Gateway and its resources can receive public IP addresses.

### flow

Internet
|
Internet Gateway
|
Public Route Table
|
Public Subnet

Private Subnet stays separate
