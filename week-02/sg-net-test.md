# Day 13: Security Groups and Network Testing

## Goal

Review Security Groups and test network access for public and private EC2 instances.

## Tests Performed

### 1. Public EC2 Browser Access

I opened the public EC2 IPv4 address in the browser using HTTP.

Result:
The Nginx welcome page loaded successfully.

### 2. SSH Access Into Public EC2

I connected to the public EC2 using SSH.

Command used:
ssh -i meeps-week2-key.pem ubuntu@PUBLIC_EC2_IP

Result:
SSH access worked successfully.

3. Private EC2 Public Access Check

I checked the private EC2 instance and confirmed it has no public IPv4 address.

Result:
The private EC2 cannot be accessed directly from the internet.

4. Security Group Review

The public EC2 allows:

SSH on port 22 from my IP only
HTTP on port 80 from anywhere

The private EC2 allows:

SSH on port 22 only from the public EC2 security group

### Commands Practiced

ping google.com
curl http://PUBLIC_EC2_IP
ssh -i meeps-week2-key.pem ubuntu@PUBLIC_EC2_IP
ip addr
sudo netstat -tulnp
sudo ss -tulnp
What I Learned

Security Groups control inbound and outbound traffic for EC2 instances.

Inbound rules define who can access the server.

Outbound rules define where the server can send traffic.

Only required ports should be opened.

Public servers can expose HTTP traffic, but SSH should be restricted.

Private servers should not be reachable directly from the internet.

### Result

The public EC2 was accessible through HTTP and SSH, while the private EC2 remained protected inside the private subnet.
