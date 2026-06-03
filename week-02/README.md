# Week 2: AWS Networking Foundations

## Goal

The goal of Week 2 was to build a secure AWS network using a custom VPC with public and private subnets.

I wanted to understand how AWS networking works beyond just launching an EC2 instance. This week focused on how cloud resources are placed inside networks, how internet access is controlled, and how public and private infrastructure are separated.

---

## What I Learned

- What a VPC is and why AWS uses it
- How CIDR blocks define private IP address ranges
- The difference between public and private IP addresses
- What subnets are and why they are important
- Difference between public and private subnets
- How an Internet Gateway connects a VPC to the internet
- How route tables control traffic flow
- How `0.0.0.0/0` represents all IPv4 internet traffic
- How Security Groups control inbound and outbound traffic
- How EC2 works inside a custom VPC
- Why public EC2 instances need a public IP address
- Why private EC2 instances should not have public IP addresses
- Why internal resources like databases should stay private
- How to test network access using basic Linux commands

---

## Architecture

```txt
Internet
   |
   |
Internet Gateway
   |
   |
Public Route Table
   |
   |
Public Subnet: 10.0.1.0/24
   |
   |
Public EC2 Instance
- Public IP enabled
- SSH allowed from my IP only
- HTTP allowed from anywhere
- Nginx installed


Private Subnet: 10.0.2.0/24
   |
   |
Private EC2 Instance
- No public IP
- No direct internet access
- Not reachable directly from the browser or local machine
```

---

## AWS Resources Created

### VPC

```txt
VPC Name: meeps-week2-vpc
CIDR Block: 10.0.0.0/16
```

The VPC acts as the private network where all the resources for this week were created.

---

### Subnets

```txt
Public Subnet: meeps-public-subnet
CIDR Block: 10.0.1.0/24
Auto-assign public IPv4: Enabled
```

```txt
Private Subnet: meeps-private-subnet
CIDR Block: 10.0.2.0/24
Auto-assign public IPv4: Disabled
```

The public subnet was used for the internet-facing EC2 instance.

The private subnet was used for the internal EC2 instance that should not be directly exposed to the internet.

---

### Internet Gateway

```txt
Internet Gateway: meeps-week2-igw
Attached to: meeps-week2-vpc
```

The Internet Gateway allows the VPC to communicate with the internet.

---

### Route Table

```txt
Route Table: meeps-public-route-table
Associated Subnet: meeps-public-subnet
```

Route added:

```txt
0.0.0.0/0 → Internet Gateway
```

This route allows resources in the public subnet to send internet-bound traffic through the Internet Gateway.

The private subnet was kept separate and was not associated with the public route table.

---

## Steps Completed

### 1. Created a Custom VPC

I created a custom VPC named:

```txt
meeps-week2-vpc
```

with the CIDR block:

```txt
10.0.0.0/16
```

This gave me a private network range to use for my AWS resources.

---

### 2. Created Public and Private Subnets

I created two subnets inside the VPC:

```txt
Public Subnet: 10.0.1.0/24
Private Subnet: 10.0.2.0/24
```

The public subnet had auto-assign public IPv4 enabled.

The private subnet had auto-assign public IPv4 disabled.

---

### 3. Attached an Internet Gateway

I created an Internet Gateway and attached it to the custom VPC.

This gave the VPC a path to the internet.

---

### 4. Configured Route Tables

I created a public route table and added this route:

```txt
0.0.0.0/0 → Internet Gateway
```

Then I associated only the public subnet with this route table.

I kept the private subnet separate so it would not have direct internet access.

---

### 5. Launched Public EC2 Instance

I launched an EC2 instance inside the public subnet.

```txt
Instance Name: meeps-public-ec2
Subnet: meeps-public-subnet
Public IP: Enabled
```

The Security Group allowed:

```txt
SSH  | Port 22 | My IP only
HTTP | Port 80 | Anywhere
```

---

### 6. Installed Nginx on Public EC2

I connected to the public EC2 instance using SSH and installed Nginx.

Commands used:

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl status nginx
```

After installation, I opened the public IPv4 address in the browser and confirmed that the Nginx welcome page loaded successfully.

---

### 7. Launched Private EC2 Instance

I launched another EC2 instance inside the private subnet.

```txt
Instance Name: meeps-private-ec2
Subnet: meeps-private-subnet
Public IP: Disabled
```

This confirmed that private servers should not be directly reachable from the internet.

---

### 8. Tested Network Access

I tested the network setup by confirming:

- Public EC2 could be opened in the browser
- Public EC2 could be accessed using SSH
- Nginx was running on port 80
- Private EC2 had no public IP address
- Private EC2 could not be accessed directly from the internet
- Only required ports were open

---

## Commands Practiced

```bash
ssh -i meeps-week2-key.pem ubuntu@PUBLIC_EC2_IP
```

```bash
curl http://PUBLIC_EC2_IP
```

```bash
ip addr
```

```bash
sudo systemctl status nginx
```

```bash
netstat -tulnp
```

```bash
sudo netstat -tulnp
```

```bash
ping google.com
```

---

## Network Testing Result

When I checked the listening ports on the public EC2 instance, I confirmed that the server was listening on the required ports.

Important ports observed:

```txt
0.0.0.0:22  → SSH
0.0.0.0:80  → HTTP/Nginx
```

This showed that:

- SSH was listening on port 22
- Nginx was listening on port 80
- HTTP traffic could reach the web server
- The public EC2 was correctly configured

---

## Screenshots

Add screenshots for:

- Custom VPC created
- Public and private subnets
- Internet Gateway attached to VPC
- Public route table with `0.0.0.0/0 → Internet Gateway`
- Public EC2 instance running
- Private EC2 instance running without public IP
- Security Group inbound rules
- Nginx welcome page in browser
- SSH access into public EC2
- `netstat` output showing listening ports

## Challenge Faced

The main challenge I faced was when I tried to check the listening ports on the EC2 instance using:

```bash
netstat -tulnp
```

The command failed because `netstat` was not installed by default on the Ubuntu server.

The terminal showed that the command could be installed using:

```bash
sudo apt install net-tools
```

To fix it, I installed the required package:

```bash
sudo apt install net-tools -y
```

After installing `net-tools`, I ran the command again:

```bash
sudo netstat -tulnp
```

This worked successfully and showed the active listening ports on the server.

The output confirmed that:

```txt
Port 22 was listening for SSH
Port 80 was listening for Nginx/HTTP
```

This helped me understand that some Linux networking tools may not come installed by default, and part of cloud debugging is knowing how to install and use the right diagnostic tools.

---

## Key Lessons

Cloud networking is about controlling how resources communicate safely.

This week helped me understand that launching servers is only one part of cloud engineering. The more important part is knowing where those servers live, how traffic reaches them, which ports are open, and which resources should stay private.

The biggest lesson from Week 2:

```txt
Public resources should be exposed carefully.
Private resources should be protected by design.
```

A secure AWS setup depends on correct VPC design, subnet separation, route tables, Internet Gateways, and Security Groups.

---

## Final Summary

In Week 2, I built a secure AWS networking foundation from scratch.

I created a custom VPC, added public and private subnets, attached an Internet Gateway, configured route tables, launched public and private EC2 instances, installed Nginx, reviewed Security Groups, and tested network access using Linux commands.

This gave me a stronger understanding of how AWS networking works in real cloud environments.
