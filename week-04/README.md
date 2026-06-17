````md
# Week 4: Application Load Balancer, Target Groups, Health Checks, and Multi-AZ

## Overview

In Week 4, I built a production-style AWS web architecture where public traffic reaches private EC2 web servers through an Application Load Balancer.

The goal was to understand how production traffic is distributed, how backend servers are protected, how health checks work, and how a load balancer handles failure and recovery.

---

## Architecture

```text
Internet
   ↓
Application Load Balancer
   ↓
Target Group
   ↓
Private EC2 Web Server 1
Private EC2 Web Server 2
```
````

The Application Load Balancer was placed in public subnets, while the EC2 web servers were placed in private subnets.

Users access the application through the ALB DNS name, not directly through the EC2 instances.

---

## Week 4 Learning Objectives

- Understand what a Load Balancer does.
- Learn the difference between ALB and NLB.
- Understand how Target Groups work.
- Configure ALB listeners.
- Configure health checks.
- Build a Multi-AZ architecture.
- Place backend EC2 instances in private subnets.
- Use Security Group chaining.
- Monitor ALB metrics in CloudWatch.
- Perform failure testing and recovery.

---

## AWS Services Used

- Amazon VPC
- Public Subnets
- Private Subnets
- Internet Gateway
- NAT Gateway
- Route Tables
- EC2
- AWS Systems Manager Session Manager
- Application Load Balancer
- Target Groups
- Security Groups
- CloudWatch Metrics
- Nginx

---

## Final Architecture Setup

### VPC

A new Week 4 VPC was created for the load balancing architecture.

### Subnets

The network was designed across two Availability Zones.

```text
Public Subnet A
Public Subnet B
Private Subnet A
Private Subnet B
```

The ALB was placed in the public subnets.

The EC2 web servers were placed in the private subnets.

### Route Tables

The public route table allowed internet access through the Internet Gateway.

```text
0.0.0.0/0 → Internet Gateway
```

The private route table allowed outbound internet access through the NAT Gateway.

```text
0.0.0.0/0 → NAT Gateway
```

The private EC2 instances used this route to install packages like Nginx.

---

## Compute Setup

I launched two private EC2 instances:

```text
Private Web Server 1
Private Web Server 2
```

Both instances:

- Were launched in private subnets.
- Had no public IPv4 address.
- Were accessed using AWS Systems Manager Session Manager.
- Used an IAM role with Systems Manager permissions.
- Had Nginx installed.
- Served different homepage text.

---

## Nginx Setup

On Web Server 1:

```bash
echo "<h1>Hello from Week 4 Private Web Server 1</h1>" | sudo tee /var/www/html/index.html
```

On Web Server 2:

```bash
echo "<h1>Hello from Week 4 Private Web Server 2</h1>" | sudo tee /var/www/html/index.html
```

I confirmed Nginx was working locally on both servers using:

```bash
curl http://localhost
curl -I http://localhost
```

Expected response:

```text
HTTP/1.1 200 OK
```

---

## Target Group Setup

I created a Target Group for the two private EC2 web servers.

### Target Group Configuration

```text
Target type: Instances
Protocol: HTTP
Port: 80
Health check path: /
Success code: 200
```

Both private EC2 instances were registered as targets.

The Target Group health check was configured to check the `/` path on each server.

---

## Application Load Balancer Setup

I created an internet-facing Application Load Balancer.

### ALB Configuration

```text
Scheme: Internet-facing
Subnets: Public Subnet A and Public Subnet B
Listener: HTTP on port 80
Default action: Forward to Target Group
```

The ALB received public traffic on port `80` and forwarded it to the Target Group.

The Target Group then forwarded traffic to the healthy private EC2 instances.

---

## Security Group Design

### ALB Security Group

The ALB Security Group allowed public HTTP traffic.

```text
Inbound:
HTTP 80 from 0.0.0.0/0
```

### Private Web Server Security Group

The private EC2 Security Group allowed HTTP traffic only from the ALB Security Group.

```text
Inbound:
HTTP 80 from ALB Security Group only
```

This means:

```text
Internet → ALB → Private EC2
```

Not:

```text
Internet → Private EC2
```

The private EC2 instances were not directly exposed to the internet.

---

## Security Group Chaining

Security Group chaining was used to make the architecture more secure.

Instead of allowing public access to the private EC2 instances, the EC2 Security Group only accepted traffic from the ALB Security Group.

This ensures that users can only reach the web servers through the Application Load Balancer.

---

## Systems Manager Instead of Bastion Host

I used AWS Systems Manager Session Manager instead of a Bastion Host.

This allowed secure access to the private EC2 instances without opening SSH port `22`.

Benefits:

- No public IP needed on private EC2.
- No Bastion Host required.
- No inbound SSH rule required.
- Access is managed through IAM and Systems Manager.

---

## Testing the ALB

After creating the ALB, I copied the ALB DNS name and tested it in the browser.

Example:

```text
http://my-week4-alb-dns-name.amazonaws.com
```

The browser returned the Nginx homepage from one of the private web servers.

I also tested using:

```bash
curl http://my-week4-alb-dns-name
```

The ALB successfully routed traffic to the private EC2 instances.

---

## Health Checks

The ALB used Target Group health checks to confirm which EC2 instances were working.

Health check configuration:

```text
Path: /
Expected response: 200 OK
```

A target was marked healthy when Nginx responded successfully.

A target was marked unhealthy when Nginx stopped responding or the port/security rule was wrong.

---

## CloudWatch ALB Metrics

I checked basic ALB metrics in CloudWatch.

Metrics reviewed:

- `HealthyHostCount`
- `UnHealthyHostCount`
- `RequestCount`
- `TargetResponseTime`
- `HTTPCode_ELB_5XX_Count`
- `HTTPCode_Target_5XX_Count`

These metrics help with monitoring traffic, backend health, response time, and errors.

---

## Failure Testing

I intentionally broke different parts of the setup to understand how ALB health checks and debugging work.

### Failure Test 1: Stopped Nginx on One Server

I stopped Nginx on one private EC2 instance.

```bash
sudo systemctl stop nginx
```

Result:

- The Target Group marked the instance as unhealthy.
- The ALB stopped routing traffic to that unhealthy target.
- Traffic continued going to the healthy server.

Fix:

```bash
sudo systemctl start nginx
sudo systemctl status nginx
```

After restarting Nginx, the target passed health checks and became healthy again.

---

### Failure Test 2: Wrong Port in Security Group

At one point, I allowed inbound traffic using HTTPS instead of HTTP.

This caused the ALB Target Group to keep showing the targets as unhealthy.

Problem:

```text
Private EC2 Security Group allowed HTTPS 443 instead of HTTP 80.
```

The ALB listener and Target Group were using HTTP port `80`, so the ALB could not reach the backend EC2 instances correctly.

Fix:

```text
Updated the private EC2 Security Group to allow HTTP 80 from the ALB Security Group.
```

Correct rule:

```text
HTTP 80 from ALB Security Group
```

After fixing the inbound rule, the Target Group health checks passed and the targets became healthy.

---

### Failure Test 3: Health Check Failure

I tested what happens when a backend server does not return the expected health check response.

Expected health check:

```text
Path: /
Success code: 200
```

If the server does not respond correctly, the target becomes unhealthy.

Fix:

- Confirmed Nginx was running.
- Confirmed the health check path was `/`.
- Confirmed the server returned `200 OK`.
- Confirmed Security Groups allowed HTTP port `80`.

---

## Challenges Faced

### Challenge: Target Group Kept Showing Unhealthy

The main issue I faced was that my ALB Target Group kept showing the private EC2 targets as unhealthy.

After debugging, I discovered that I had allowed inbound traffic for HTTPS instead of HTTP.

Since the ALB listener and Target Group were configured for HTTP port `80`, the backend EC2 Security Group needed to allow HTTP traffic from the ALB Security Group.

### Fix

I updated the private web server Security Group to allow:

```text
HTTP 80 from ALB Security Group
```

After this fix, the ALB was able to reach the private EC2 instances, and the targets became healthy.

---

## Debugging Notes

When the Target Group showed unhealthy, I checked:

- Whether Nginx was running.
- Whether the health check path was correct.
- Whether the target port was `80`.
- Whether the private EC2 Security Group allowed HTTP from the ALB Security Group.
- Whether the EC2 instances were in the correct VPC.
- Whether the ALB listener was forwarding to the correct Target Group.

Useful commands:

```bash
sudo systemctl status nginx
curl http://localhost
curl -I http://localhost
sudo ss -tulnp | grep :80
```

---

## Screenshots

Screenshots to include in this project:

```text
1. Architecture diagram
2. VPC subnets across two Availability Zones
3. Public and private route tables
4. Two private EC2 instances with no public IP
5. Session Manager access to private EC2
6. Nginx running on Web Server 1
7. Nginx running on Web Server 2
8. Target Group configuration
9. Target Group showing healthy targets
10. ALB details page
11. ALB listener on HTTP port 80
12. Browser showing ALB DNS working
13. Security Group showing HTTP 80 from ALB SG only
14. Target Group showing unhealthy target after failure test
15. Target Group showing recovered healthy target
16. CloudWatch ALB metrics
```

---

## What I Broke and Fixed

| Issue                       | Cause                                      | Fix                                     |
| --------------------------- | ------------------------------------------ | --------------------------------------- |
| Target Group unhealthy      | Used HTTPS instead of HTTP in inbound rule | Allowed HTTP 80 from ALB Security Group |
| One target became unhealthy | Nginx was stopped intentionally            | Restarted Nginx                         |
| Health check failed         | Backend did not respond correctly          | Verified `/` path and `200 OK` response |
| ALB could not route traffic | Security Group rule was incorrect          | Corrected ALB-to-EC2 access on port 80  |

---

## Key Lessons

- ALB should be placed in public subnets.
- Backend EC2 instances should be placed in private subnets.
- Target Groups connect the ALB to backend servers.
- Health checks decide which targets receive traffic.
- A target must return `200 OK` to pass the health check.
- Security Group chaining is important for production security.
- The private EC2 Security Group should allow traffic only from the ALB Security Group.
- Wrong ports can cause Target Group health checks to fail.
- CloudWatch metrics help with monitoring and debugging.
- Failure testing helps prove that the architecture can recover.

---

## Final Outcome

By the end of Week 4, I successfully built a production-style AWS load balancing architecture.

The final setup allows users to access an Application Load Balancer through the internet. The ALB forwards traffic to a Target Group, and the Target Group routes traffic only to healthy private EC2 web servers.

I also tested failure scenarios by intentionally breaking parts of the setup and fixing them. This helped me understand how ALB health checks, target recovery, Security Groups, and CloudWatch metrics work in a real AWS environment.

Final traffic flow:

```text
Internet
   ↓
Application Load Balancer
   ↓
Target Group
   ↓
Healthy Private EC2 Web Servers
```
