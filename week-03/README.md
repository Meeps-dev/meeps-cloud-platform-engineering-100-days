# Week 3: AWS Networking Deep Dive

## Overview

This week focused on deeper AWS networking concepts used in real production environments.

In Week 2, I built the foundation of AWS networking by creating a custom VPC with public and private subnets. In Week 3, I extended that setup by learning how private resources access the internet securely, how engineers access private servers, how VPC endpoints reduce public internet dependency, how Security Groups and Network ACLs control traffic, and how VPC Flow Logs help debug networking issues.

The goal was not just to create AWS resources, but to understand how traffic flows through a cloud network and how to troubleshoot when something breaks.

---

## Week 3 Goal

Build a more production-like AWS network using:

- NAT Gateway
- Bastion Host
- AWS Systems Manager Session Manager
- VPC Endpoints
- Security Groups
- Network ACLs
- VPC Flow Logs
- CloudWatch Logs
- DNS basics
- Route 53 basics
- Load Balancer concepts

By the end of this week, I wanted to understand how private infrastructure communicates securely without exposing everything directly to the public internet.

---

## Architecture Overview

```text
Internet
   |
Internet Gateway
   |
Public Subnet
   |
Public EC2 / Bastion Host
   |
Private EC2
   |
Private Route Table
   |
NAT Gateway
   |
Internet Gateway
   |
Internet
```

For private AWS service access:

```text
Private EC2
   |
VPC Endpoint
   |
AWS Service
```

For logging and debugging:

```text
VPC Traffic
   |
VPC Flow Logs
   |
CloudWatch Logs
   |
CloudWatch Logs Insights
```

For production-style application routing:

```text
User
   |
Domain Name
   |
Route 53
   |
Load Balancer
   |
Private EC2 / App Servers
```

---

## AWS Services Used

- Amazon VPC
- Public Subnet
- Private Subnet
- Internet Gateway
- NAT Gateway
- Elastic IP
- Route Tables
- Security Groups
- Network ACLs
- Amazon EC2
- AWS Systems Manager Session Manager
- VPC Gateway Endpoint for S3
- VPC Interface Endpoints
- Amazon CloudWatch Logs
- VPC Flow Logs
- Amazon Route 53 basics
- Elastic Load Balancing concepts

---

## Day 16: NAT Gateway

### What I Did

I created a NAT Gateway to allow my private EC2 instance to access the internet without exposing the instance directly to the public internet.

The private EC2 instance had no public IPv4 address. Before NAT Gateway, it could not access the internet. After creating the NAT Gateway and updating the private route table, the private EC2 instance was able to reach the internet for outbound traffic.

---

### NAT Gateway Flow

```text
Private EC2
   |
Private Route Table
   |
NAT Gateway
   |
Internet Gateway
   |
Internet
```

---

### Steps Completed

1. Created a custom VPC.
2. Created one public subnet and one private subnet.
3. Created and attached an Internet Gateway.
4. Created a public route table with:

```text
0.0.0.0/0 → Internet Gateway
```

5. Created a private route table.
6. Allocated an Elastic IP.
7. Created a NAT Gateway inside the public subnet.
8. Attached the Elastic IP to the NAT Gateway.
9. Updated the private route table with:

```text
0.0.0.0/0 → NAT Gateway
```

10. Connected to the private EC2 instance.
11. Tested outbound internet access from the private EC2 instance.

---

### Commands Used

```bash
ping google.com
curl ifconfig.me
sudo apt update
```

---

### What I Learned

- NAT means Network Address Translation.
- A NAT Gateway allows private resources to access the internet.
- NAT Gateway must be placed in a public subnet.
- NAT Gateway needs an Elastic IP.
- Private subnets route internet-bound traffic to NAT Gateway.
- NAT Gateway supports outbound internet access only.
- NAT Gateway does not allow the public internet to directly connect to private EC2 instances.

---

### Key Takeaway

A private server should not need to become public just because it needs internet access.

NAT Gateway solves this by allowing outbound internet access while keeping the private server protected from direct inbound internet traffic.

---

## Day 17: Bastion Host and Secure Private EC2 Access

### What I Did

I used my public EC2 instance as a Bastion Host to securely access my private EC2 instance.

The private EC2 instance was placed inside a private subnet and had no public IPv4 address. Instead of exposing the private EC2 directly to the internet, I accessed it through the public EC2 instance.

---

### Bastion Host Architecture

```text
My Laptop
   |
SSH
   |
Public EC2 / Bastion Host
   |
SSH
   |
Private EC2
```

---

### Security Group Setup

#### Public EC2 Security Group

```text
SSH  | TCP | 22 | My IP
HTTP | TCP | 80 | 0.0.0.0/0
```

The important rule was:

```text
SSH | TCP | 22 | My IP
```

This ensured that only my own IP address could SSH into the Bastion Host.

---

#### Private EC2 Security Group

```text
SSH | TCP | 22 | Source: Public EC2 Security Group
```

This ensured that only the Bastion Host could SSH into the private EC2 instance.

---

### Commands Used

From my laptop:

```bash
ssh -i my-key.pem ubuntu@PUBLIC_EC2_PUBLIC_IP
```

From the public EC2:

```bash
ssh -i my-key.pem ubuntu@PRIVATE_EC2_PRIVATE_IP
```

To confirm the private EC2 connection:

```bash
hostname
hostname -I
ip addr
```

---

### What I Learned

- A Bastion Host is a controlled public entry point into private servers.
- Private EC2 instances should not be exposed directly to the internet.
- The public EC2 can act as a jump server.
- The private EC2 should only allow SSH from the Bastion Host Security Group.
- SSH should not be open to `0.0.0.0/0`.
- Copying private keys to a Bastion Host is not recommended in production.
- Production teams often prefer AWS Systems Manager Session Manager instead.

---

### Key Takeaway

A Bastion Host helps engineers securely reach private infrastructure without giving private servers public IP addresses.

However, modern production environments often prefer Session Manager because it avoids public SSH access completely.

---

## Day 18: AWS Systems Manager Session Manager

### What I Did

I used AWS Systems Manager Session Manager to connect to an EC2 instance without SSH.

Instead of using a key pair, opening port `22`, or connecting through a Bastion Host, I connected directly from the AWS Console using Session Manager.

---

### Session Manager Architecture

```text
AWS Console
   |
AWS Systems Manager Session Manager
   |
EC2 Instance
```

---

### Steps Completed

1. Created an IAM role for EC2.
2. Attached the AWS managed policy:

```text
AmazonSSMManagedInstanceCore
```

3. Launched an EC2 instance.
4. Attached the IAM role to the EC2 instance.
5. Used a Security Group with no inbound SSH rule.
6. Confirmed that the instance appeared in Systems Manager.
7. Started a Session Manager session.
8. Ran Linux commands inside the browser terminal.
9. Terminated the temporary EC2 instance after testing.

---

### Commands Used

Inside the Session Manager terminal:

```bash
whoami
hostname
ip addr
```

---

### Security Group Setup

For the EC2 instance, I used:

```text
Inbound rules:
None
```

Outbound traffic was left as default:

```text
Outbound rules:
All traffic allowed
```

This proved that Session Manager does not need inbound SSH access.

---

### What I Learned

- AWS Systems Manager helps manage AWS resources like EC2 instances.
- Session Manager gives shell access without SSH.
- No SSH key is required.
- Port `22` does not need to be open.
- EC2 does not need inbound SSH rules.
- Access is controlled through IAM.
- Sessions can be logged and audited.
- EC2 needs SSM Agent running.
- EC2 needs permission through an IAM role.
- Private EC2 instances can use Session Manager through NAT Gateway or VPC Interface Endpoints.

---

### Key Takeaway

Session Manager is a safer and more modern way to access EC2 instances because it removes the need for public SSH access, key sharing, and Bastion Hosts.

---

## Day 19: VPC Endpoints

### What I Did

I created VPC Endpoints to allow private resources inside my VPC to access AWS services without depending on the public internet or NAT Gateway.

The main endpoint I created was an S3 Gateway Endpoint. I also used Systems Manager Interface Endpoints to connect to a private EC2 instance using Session Manager.

---

### VPC Endpoint Architecture

```text
Private EC2
   |
Private Route Table
   |
S3 Gateway Endpoint
   |
Amazon S3
```

For private Session Manager access:

```text
AWS Console
   |
Systems Manager Interface Endpoints
   |
Private EC2
```

---

### Endpoints Created

#### S3 Gateway Endpoint

Used for private access to Amazon S3.

```text
Private EC2 → S3 Gateway Endpoint → Amazon S3
```

The private route table was updated with a route similar to:

```text
pl-xxxxxxxx → vpce-xxxxxxxx
```

The `pl-xxxxxxxx` value represents the AWS-managed S3 prefix list.

The `vpce-xxxxxxxx` value represents the VPC Endpoint.

---

#### Systems Manager Interface Endpoints

Used for private Systems Manager access.

Created endpoints for:

```text
ssm
ssmmessages
ec2messages
```

These allowed the private EC2 instance to communicate with AWS Systems Manager without using NAT Gateway.

---

### IAM Role Used

The private EC2 instance used an IAM role with:

```text
AmazonSSMManagedInstanceCore
```

For S3 testing, I also added S3 permissions such as:

```text
AmazonS3ReadOnlyAccess
```

---

### Commands Used

Inside the private EC2 instance through Session Manager:

```bash
aws --version
aws s3 ls
```

---

### What I Learned

- VPC Endpoints allow private resources to connect to AWS services privately.
- Gateway Endpoints are used for S3 and DynamoDB.
- Interface Endpoints are used for services like Systems Manager, CloudWatch, ECR, Secrets Manager, and others.
- Gateway Endpoints are attached to route tables.
- Interface Endpoints create private network interfaces inside the VPC.
- PrivateLink powers Interface Endpoints.
- VPC Endpoints reduce NAT Gateway dependency.
- Private EC2 instances can access AWS services without public IPs, Bastion Hosts, or NAT Gateway.

---

### Key Takeaway

VPC Endpoints help keep traffic private and reduce dependency on NAT Gateway.

This is closer to how secure production cloud networks are designed.

---

## Day 20: Security Groups vs Network ACLs

### What I Did

I reviewed Security Groups and Network ACLs to understand how traffic is controlled at both the instance level and subnet level.

I also created a test Network ACL, intentionally blocked HTTP traffic on port `80`, observed how the traffic broke, and then fixed it by removing the deny rule.

---

### Security Group Review

#### Public EC2 Security Group

```text
SSH  | TCP | 22 | My IP
HTTP | TCP | 80 | 0.0.0.0/0
```

This allowed SSH only from my IP and HTTP from the internet.

---

#### Private EC2 Security Group

```text
SSH | TCP | 22 | Source: Public EC2 Security Group
```

This allowed SSH into the private EC2 only from the Bastion Host.

---

### Network ACL Review

The default Network ACL allowed all inbound and outbound traffic.

Example inbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

Example outbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

---

### What I Broke Intentionally

I created a test NACL and associated it with the public subnet.

Then I added this inbound deny rule:

```text
90 | HTTP | TCP | 80 | 0.0.0.0/0 | DENY
```

The NACL rules became:

```text
90  | HTTP        | TCP | 80  | 0.0.0.0/0 | DENY
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

Because NACL rules are evaluated from the lowest rule number first, rule `90` blocked HTTP traffic before rule `100` could allow it.

---

### What Happened

Before the deny rule, the Nginx page was accessible.

After adding the deny rule, HTTP stopped working.

Test command:

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

The request failed or timed out.

SSH still worked because I blocked only HTTP port `80`, not SSH port `22`.

---

### How I Fixed It

I removed the deny rule:

```text
90 | HTTP | TCP | 80 | 0.0.0.0/0 | DENY
```

After removing it, the allow-all rule allowed HTTP traffic again:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
```

Then I tested again:

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

The Nginx page worked again.

---

### What I Learned

- Security Groups work at the instance or network interface level.
- Network ACLs work at the subnet level.
- Security Groups are stateful.
- Network ACLs are stateless.
- Security Groups only support allow rules.
- Network ACLs support allow and deny rules.
- NACL rule order matters.
- Lower rule numbers are evaluated first.
- A NACL deny rule can block traffic even if the Security Group allows it.
- NACLs can break traffic if misconfigured.

---

### Security Group vs NACL Comparison

| Feature            | Security Group                   | Network ACL                   |
| ------------------ | -------------------------------- | ----------------------------- |
| Level              | Instance/network interface level | Subnet level                  |
| Stateful           | Yes                              | No                            |
| Rule type          | Allow rules only                 | Allow and deny rules          |
| Rule order matters | No                               | Yes                           |
| Return traffic     | Automatically allowed            | Must be allowed manually      |
| Common use         | Main resource firewall           | Extra subnet-level protection |

---

### Key Takeaway

Security Groups protect individual resources, while Network ACLs protect entire subnets.

In this task, I intentionally broke HTTP access by adding a NACL deny rule for port `80`, then fixed it by removing the deny rule.

This helped me understand how subnet-level rules can block traffic before it reaches an EC2 instance.

---

## Day 21: VPC Flow Logs, CloudWatch Logs, DNS, Route 53 Basics, and Load Balancer Introduction

### What I Did

I enabled VPC Flow Logs and sent the logs to CloudWatch Logs so I could inspect accepted and rejected network traffic.

I also reviewed DNS, Route 53, hosted zones, DNS records, and how production applications are usually routed through load balancers.

---

### VPC Flow Logs Architecture

```text
VPC Network Traffic
   |
VPC Flow Logs
   |
CloudWatch Logs
   |
CloudWatch Logs Insights
```

---

### Flow Log Setup

```text
Resource: VPC
Filter: All
Destination: CloudWatch Logs
Log format: AWS default format
CloudWatch Log Group: /aws/vpc/meeps-week3-flowlogs
IAM Role: meeps-vpc-flowlogs-role
```

I selected `All` traffic so I could capture both:

```text
ACCEPT
REJECT
```

---

### Accepted Traffic Test

I generated accepted traffic by accessing the public EC2 instance through HTTP port `80`.

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

This worked because:

```text
Nginx was running
Security Group allowed HTTP port 80
NACL allowed traffic
Public route table had internet access
```

In Flow Logs, this traffic appeared as:

```text
ACCEPT
```

---

### Rejected Traffic Test

I generated rejected traffic by trying to access port `81`.

```bash
curl http://PUBLIC_EC2_PUBLIC_IP:81
```

This failed because port `81` was not allowed by the Security Group.

In Flow Logs, this traffic appeared as:

```text
REJECT
```

---

### What I Broke Intentionally

I intentionally tried to connect to a blocked port:

```text
TCP port 81
```

This was done to generate rejected traffic and understand how blocked traffic appears in VPC Flow Logs.

The issue was not Nginx, EC2, or the route table.

The issue was:

```text
Port 81 was not allowed by the Security Group
```

---

### How I Fixed It

For this lab, I did not open port `81` because it was only used to test rejected traffic.

To restore normal access, I used the correct allowed port:

```text
Port 80
```

Test command:

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

The request worked successfully.

If this had been a real application that needed port `81`, the correct fix would be to update the Security Group and allow port `81` from the correct trusted source.

---

### CloudWatch Logs Challenge

At first, I had difficulty understanding how to read the raw CloudWatch Log Group records.

The logs contained many fields, and it was not immediately clear which traffic was accepted, which traffic was rejected, which port was involved, or which source IP was trying to connect.

Later, I used CloudWatch Logs Insights, and that made the logs easier to understand.

Logs Insights helped me search for:

```text
ACCEPT
REJECT
Port 80
Port 81
```

This made it much easier to understand how to use VPC Flow Logs for debugging.

---

### CloudWatch Logs Insights Queries Used

To find accepted traffic:

```sql
fields @timestamp, @message
| filter @message like /ACCEPT/
| sort @timestamp desc
| limit 20
```

To find rejected traffic:

```sql
fields @timestamp, @message
| filter @message like /REJECT/
| sort @timestamp desc
| limit 20
```

To find port `80` traffic:

```sql
fields @timestamp, @message
| filter @message like / 80 /
| sort @timestamp desc
| limit 20
```

To find port `81` traffic:

```sql
fields @timestamp, @message
| filter @message like / 81 /
| sort @timestamp desc
| limit 20
```

---

### How to Read a Flow Log Record

Default VPC Flow Log format:

```text
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```

Example:

```text
2 123456789012 eni-abc123 102.89.x.x 10.0.1.20 54321 81 6 1 40 1710000000 1710000060 REJECT OK
```

Meaning:

```text
srcaddr     → Source IP
dstaddr     → Destination IP
srcport     → Source port
dstport     → Destination port
protocol    → Protocol number
action      → ACCEPT or REJECT
log-status  → Log delivery status
```

Important protocol numbers:

```text
6  = TCP
17 = UDP
1  = ICMP
```

---

### DNS and Route 53 Review

I also reviewed DNS and Route 53 basics.

DNS means Domain Name System. It converts human-readable domain names into IP addresses or other DNS targets.

Example:

```text
example.com → 18.130.10.20
```

Amazon Route 53 is AWS’s DNS service. It can manage domain records and route traffic to AWS resources or external services.

---

### Public Hosted Zone vs Private Hosted Zone

A public hosted zone is used for internet-facing DNS records.

Example:

```text
www.myapp.com → public load balancer
```

A private hosted zone is used for internal DNS records that only resolve inside selected VPCs.

Example:

```text
api.internal.local → private load balancer
```

---

### A Record vs CNAME Record

An A record points a domain name to an IPv4 address.

```text
app.example.com → 18.130.10.20
```

A CNAME record points one domain name to another domain name.

```text
www.example.com → example.com
```

---

### Load Balancer Introduction

A load balancer receives traffic from users and forwards it to healthy backend targets.

Targets can include:

```text
EC2 instances
Containers
IP addresses
Lambda functions
```

Production traffic usually follows this pattern:

```text
User
   |
Route 53
   |
Load Balancer
   |
Private EC2 / App Servers
```

This allows backend servers to stay private while the load balancer handles public traffic.

---

## Main Challenges Faced

### 1. Understanding NAT Gateway

At first, it was easy to confuse NAT Gateway with Internet Gateway.

I learned that an Internet Gateway is for public internet access, while NAT Gateway allows private resources to initiate outbound internet access without becoming publicly reachable.

---

### 2. Understanding Bastion Host Access

I had to understand that the private EC2 is not accessed directly from my laptop.

The correct path is:

```text
Laptop → Public EC2 Bastion Host → Private EC2
```

This helped me understand how private infrastructure is accessed securely.

---

### 3. Understanding CloudWatch Flow Logs

At first, the raw CloudWatch Log Group records were difficult to read.

CloudWatch Logs Insights helped me filter for:

```text
ACCEPT
REJECT
Port 80
Port 81
```

This made the logs much easier to understand and showed me how Flow Logs can be used for real debugging.

---

## Screenshots Added

- VPC created.
- Public subnet and private subnet.
- Internet Gateway attached to VPC.
- Public route table with route to Internet Gateway.
- Private route table with route to NAT Gateway.
- NAT Gateway available.
- Elastic IP attached to NAT Gateway.
- Private EC2 with no public IPv4 address.
- Bastion Host SSH access.
- Private EC2 accessed from Bastion Host.
- Session Manager connected to EC2 without SSH.
- IAM role with `AmazonSSMManagedInstanceCore`.
- S3 Gateway Endpoint created.
- Private route table updated with S3 prefix list route.
- VPC Interface Endpoints for Systems Manager.
- Security Group rules for public and private EC2.
- Default NACL rules.
- Test NACL deny rule for HTTP port `80`.
- HTTP traffic broken by NACL rule.
- HTTP traffic restored after removing NACL rule.
- VPC Flow Logs enabled.
- CloudWatch Log Group created.
- CloudWatch Logs showing ACCEPT traffic.
- CloudWatch Logs showing REJECT traffic.
- CloudWatch Logs Insights queries.

---

## Cleanup

To control AWS costs, I deleted temporary resources after completing the labs.

Cleanup included:

```text
Terminated temporary EC2 instances
Deleted NAT Gateway
Released Elastic IP
Deleted VPC Interface Endpoints
Deleted VPC Flow Logs
Deleted CloudWatch Log Group
Deleted test NACL
Removed unused Security Groups
```

I kept only the resources needed for the next task where necessary.

---

## Key Takeaways

- Private servers should not be exposed directly to the internet.
- NAT Gateway allows private resources to access the internet securely.
- Bastion Hosts provide controlled access into private subnets.
- Session Manager is safer than SSH because it removes the need for public SSH access.
- VPC Endpoints allow private access to AWS services without NAT Gateway.
- Security Groups are stateful and work at the resource level.
- Network ACLs are stateless and work at the subnet level.
- NACL deny rules can block traffic even when Security Groups allow it.
- VPC Flow Logs help debug accepted and rejected traffic.
- CloudWatch Logs Insights makes network logs easier to search and understand.
- DNS maps domain names to infrastructure targets.
- Route 53 manages DNS records in AWS.
- Production applications usually route traffic through a load balancer instead of directly exposing EC2 instances.

---

## Final Reflection

Week 3 helped me understand AWS networking beyond just creating a VPC.

I learned how traffic moves through public and private subnets, how private instances access the internet, how engineers securely access private infrastructure, how private resources connect to AWS services, and how to debug network traffic using logs.

The biggest lesson this week was that cloud networking problems are not magic. Most issues come down to route tables, Security Groups, Network ACLs, ports, DNS, or missing network paths.

Understanding how to trace and debug these layers is a core skill for Cloud and Platform Engineers.
