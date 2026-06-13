## Day 21: VPC Flow Logs, CloudWatch Logs, DNS, Route 53 Basics, and Load Balancer Introduction

### What I Did

For Day 21, I focused on observability and production-style traffic routing.

The main practical task was enabling **VPC Flow Logs** for my VPC and sending the logs to **Amazon CloudWatch Logs**. This allowed me to inspect network traffic and understand which traffic was accepted and which traffic was rejected.

I also reviewed the basics of DNS, Route 53, hosted zones, DNS records, and how traffic is usually routed to applications through a load balancer in production environments.

---

### Main Goal

The goal of this task was to understand how cloud engineers debug network traffic instead of guessing.

When something is not reachable in AWS, the issue may come from:

Security Groups
Network ACLs
Route Tables
Public IP / Private IP setup
Subnet associations
Missing Internet Gateway
Missing NAT Gateway
Blocked ports
DNS misconfiguration

VPC Flow Logs help show what is actually happening at the network level.

---

### Architecture

User / Laptop
↓
Public EC2
↓
VPC Network Interface
↓
VPC Flow Logs
↓
CloudWatch Logs
↓
CloudWatch Logs Insights

For production routing:

User
↓
Domain Name
↓
Route 53
↓
Load Balancer
↓
Private EC2 / App Servers

---

### Steps I Followed

1. Confirmed that my VPC existed.
2. Confirmed that my public EC2 instance was running.
3. Confirmed that the public EC2 had a public IPv4 address.
4. Confirmed that Nginx was running on the public EC2.
5. Created a CloudWatch Log Group for VPC Flow Logs.
6. Created an IAM role for VPC Flow Logs.
7. Added permissions that allowed VPC Flow Logs to publish to CloudWatch Logs.
8. Enabled Flow Logs on my VPC.
9. Selected `All` traffic so I could capture both accepted and rejected traffic.
10. Sent the logs to CloudWatch Logs.
11. Generated accepted traffic by accessing the public EC2 on HTTP port `80`.
12. Generated rejected traffic by trying to access a blocked port.
13. Opened CloudWatch Logs to inspect the log streams.
14. Used CloudWatch Logs Insights to search and understand the flow log records properly.
15. Reviewed DNS, Route 53, hosted zones, A records, CNAME records, and load balancer basics.

---

### VPC Flow Logs Setup

I enabled Flow Logs on my VPC.

Flow log settings:

Resource: VPC
Filter: All
Destination: CloudWatch Logs
Log format: AWS default format
CloudWatch Log Group: /aws/vpc/meeps-week3-flowlogs
IAM Role: meeps-vpc-flowlogs-role

I selected `All` traffic because I wanted to capture:

ACCEPT traffic
REJECT traffic

This helped me compare working traffic with blocked traffic.

---

### CloudWatch Log Group

I created a CloudWatch Log Group to store the VPC Flow Logs.

Log group used:

/aws/vpc/meeps-week3-flowlogs

I used CloudWatch Logs to view the raw traffic logs generated from the VPC.

---

### IAM Role Used

I created an IAM role that allowed VPC Flow Logs to write logs into CloudWatch Logs.

IAM role name:

meeps-vpc-flowlogs-role

The role allowed actions such as:

logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
logs:DescribeLogGroups
logs:DescribeLogStreams

This permission was required so VPC Flow Logs could publish network traffic records to CloudWatch.

---

### Accepted Traffic Test

To generate accepted traffic, I accessed the public EC2 instance through HTTP.

Command used:

curl http://PUBLIC_EC2_PUBLIC_IP

I also tested through the browser:

http://PUBLIC_EC2_PUBLIC_IP

This worked because:

Nginx was running
Public EC2 had a public IP
Security Group allowed HTTP port 80
Public subnet had a route to the Internet Gateway
NACL allowed the traffic

In the Flow Logs, this traffic appeared as:

ACCEPT

This showed that the traffic was allowed.

---

### Rejected Traffic Test

To generate rejected traffic, I tried to access a port that was not allowed by the Security Group.

Example:

curl http://PUBLIC_EC2_PUBLIC_IP:81

or:

nc -vz PUBLIC_EC2_PUBLIC_IP 81

This failed because port `81` was not open in the public EC2 Security Group.

The public EC2 Security Group allowed:

SSH | TCP | 22
HTTP | TCP | 80

But it did not allow:

TCP | 81

So the traffic was rejected.

In the Flow Logs, this appeared as:

REJECT

---

### What I Broke Intentionally

For this task, I intentionally tested traffic to a blocked port.

The broken test was:

Trying to reach the public EC2 on port 81

That traffic failed because the Security Group did not allow port `81`.

This was intentional. The purpose was to generate rejected traffic so I could see how VPC Flow Logs records blocked network traffic.

The issue was not with Nginx, the EC2 instance, or the route table.

The issue was simply:

Port 81 was not allowed by the Security Group

---

### How We Fixed It

In this case, I did not need to open port `81` permanently because the goal was only to test rejected traffic.

To restore normal access, I used the correct allowed port:

Port 80

Then I tested again:

curl http://PUBLIC_EC2_PUBLIC_IP

The request worked successfully.

So the fix was:

Use the correct allowed port: 80

If this had been a real application that needed port `81`, the proper fix would be to update the Security Group and allow port `81` from the correct trusted source.

But for this lab, I left port `81` blocked because unnecessary ports should not be opened.

---

### CloudWatch Logs Challenge I Faced

At first, I had difficulty understanding how to read the raw CloudWatch Log Group records.

The logs contained many fields, and it was not immediately clear which traffic was accepted, which traffic was rejected, which port was involved, or which source IP was trying to connect.

The raw logs looked difficult to read because they were displayed as long records.

Later, I used **CloudWatch Logs Insights**, and that made the logs easier to understand.

Logs Insights helped me search for:

ACCEPT
REJECT
Port 80
Port 81

This helped me understand how to read VPC Flow Logs properly when debugging network issues.

---

### CloudWatch Logs Insights Queries Used

To find accepted traffic:

```sql
fields @timestamp, @message
| filter @message like /ACCEPT/
| sort @timestamp desc
| limit 20


To find rejected traffic:


fields @timestamp, @message
| filter @message like /REJECT/
| sort @timestamp desc
| limit 20
```

To search for traffic involving port `80`:

```sql
fields @timestamp, @message
| filter @message like / 80 /
| sort @timestamp desc
| limit 20


To search for traffic involving port `81`:


fields @timestamp, @message
| filter @message like / 81 /
| sort @timestamp desc
| limit 20


---

### How to Read a Flow Log Record

A default VPC Flow Log record looks like this:


version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status


Example:

2 123456789012 eni-abc123 102.89.x.x 10.0.1.20 54321 81 6 1 40 1710000000 1710000060 REJECT OK
```

Meaning:

2 → Flow log version
123456789012 → AWS account ID
eni-abc123 → Network interface ID
102.89.x.x → Source IP address
10.0.1.20 → Destination IP address
54321 → Source port
81 → Destination port
6 → Protocol number
1 → Number of packets
40 → Number of bytes
REJECT → Traffic was rejected
OK → Log status

Important protocol numbers:

6 = TCP
17 = UDP
1 = ICMP

```

---

### What I Learned About VPC Flow Logs

* VPC Flow Logs capture network traffic metadata.
* Flow Logs can show accepted and rejected traffic.
* `ACCEPT` means the traffic was allowed.
* `REJECT` means the traffic was blocked.
* Flow Logs help debug Security Group and NACL issues.
* Flow Logs do not show the full request body or application data.
* Flow Logs are useful for checking source IP, destination IP, port, protocol, and action.
* Flow Logs are not always instant, so logs may take a few minutes to appear.
* CloudWatch Logs stores the logs.
* CloudWatch Logs Insights makes the logs easier to search and understand.

---

### DNS Basics

I also reviewed DNS basics.

DNS means:


Domain Name System


DNS converts human-readable names into IP addresses or other DNS names.

Example:


example.com → 18.130.10.20


Without DNS, users would need to remember IP addresses instead of domain names.

---

### Route 53 Basics

Amazon Route 53 is AWS’s DNS service.

Route 53 can be used to:


Register domains
Create DNS records
Route traffic to AWS resources
Route traffic to external resources
Create public hosted zones
Create private hosted zones


In production, Route 53 is commonly used to point a domain name to a load balancer, CloudFront distribution, or another target.

---

### Public Hosted Zone vs Private Hosted Zone

A public hosted zone is used for DNS records that should resolve publicly on the internet.

Example:


www.myapp.com → public load balancer


A private hosted zone is used for internal DNS records that should only resolve inside selected VPCs.

Example:


api.internal.local → private load balancer


---

### A Record vs CNAME Record

An A record points a domain name to an IPv4 address.

Example:


app.example.com → 18.130.10.20


A CNAME record points one domain name to another domain name.

Example:


www.example.com → example.com


In production, it is common to point DNS to a load balancer instead of directly to one EC2 instance.

---

### Domain Name to Server Routing

A normal production traffic flow can look like this:


User enters domain name
   ↓
DNS resolves the domain
   ↓
Route 53 returns the target
   ↓
Traffic goes to the load balancer
   ↓
Load balancer forwards traffic to healthy backend servers


Example:


user visits app.example.com
   ↓
Route 53
   ↓
Application Load Balancer
   ↓
Private EC2 instances


---

### Load Balancer Introduction

A load balancer receives traffic from users and forwards it to healthy backend targets.

Targets can include:


EC2 instances
Containers
IP addresses
Lambda functions


A load balancer helps with:


High availability
Health checks
Traffic distribution
Scaling
Keeping backend servers private


Instead of exposing backend servers directly to the internet, users connect to the load balancer, and the load balancer forwards traffic to the application servers.

---

### Key Takeaways

* VPC Flow Logs help debug network traffic.
* CloudWatch Logs stores the traffic logs.
* CloudWatch Logs Insights makes the logs easier to search.
* Accepted traffic appears as `ACCEPT`.
* Blocked traffic appears as `REJECT`.
* Testing a blocked port helped me understand how rejected traffic appears in logs.
* DNS converts names into targets.
* Route 53 manages DNS records in AWS.
* Public hosted zones are for internet-facing DNS records.
* Private hosted zones are for internal VPC DNS records.
* A records point to IPv4 addresses.
* CNAME records point to another domain name.
* Production apps usually use load balancers instead of exposing EC2 instances directly.

---

### Screenshots Added

* VPC selected for Flow Logs.
* Flow Log created on the VPC.
* Flow Log filter set to `All`.
* Flow Log destination set to CloudWatch Logs.
* CloudWatch Log Group created.
* IAM role used by VPC Flow Logs.
* Nginx page working on public EC2.
* Accepted HTTP traffic test.
* Rejected port `81` traffic test.
* CloudWatch Log Stream showing flow log records.
* CloudWatch Logs Insights query for `ACCEPT`.
* CloudWatch Logs Insights query for `REJECT`.
* CloudWatch Logs Insights query for port `80`.
* CloudWatch Logs Insights query for port `81`.

---

### Cleanup Note

After completing the task and taking screenshots, I cleaned up the temporary resources to avoid unnecessary billing.

Cleanup completed:


Deleted VPC Flow Log
Deleted CloudWatch Log Group
Terminated temporary EC2 instance
Deleted unused test resources


The key lesson from this cleanup is that observability tools are useful, but unused logs and temporary compute resources should be removed after practice to control AWS costs.

```
