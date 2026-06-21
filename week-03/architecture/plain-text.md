# Week 3: AWS Networking Architecture

                           ┌──────────────────────┐
                           │      User / Laptop    │
                           │ SSH, Browser, curl    │
                           └───────────┬──────────┘
                                       │
                                       │ Internet traffic
                                       ↓
                           ┌──────────────────────┐
                           │     Internet Gateway  │
                           │ Public internet entry │
                           └───────────┬──────────┘
                                       │
                                       ↓

┌──────────────────────────────────────────────────────────────────────────────┐
│ VPC: meeps-week3-vpc │
│ CIDR: 10.0.0.0/16 │
│ │
│ ┌────────────────────────────────────┐ ┌──────────────────────────────┐ │
│ │ Public Subnet │ │ Private Subnet │ │
│ │ 10.0.1.0/24 │ │ 10.0.2.0/24 │ │
│ │ │ │ │ │
│ │ Route Table: │ │ Route Table: │ │
│ │ 0.0.0.0/0 → Internet Gateway │ │ 0.0.0.0/0 → NAT Gateway │ │
│ │ │ │ S3 Prefix List → S3 Endpoint│ │
│ │ │ │ │ │
│ │ ┌──────────────────────────────┐ │ │ ┌────────────────────────┐ │ │
│ │ │ Public EC2 / Bastion Host │ │ │ │ Private EC2 │ │ │
│ │ │ Has Public IP │ │ │ │ No Public IP │ │ │
│ │ │ SSH allowed from My IP only │ │ │ │ SSH only from Bastion SG │ │ │
│ │ └──────────────┬───────────────┘ │ │ └────────────┬───────────┘ │ │
│ │ │ │ │ │ │ │
│ │ │ SSH using │ │ │ │ │
│ │ │ private IP │ │ │ │ │
│ │ └──────────────────┼────┼───────────────┘ │ │
│ │ │ │ │ │
│ │ ┌──────────────────────────────┐ │ │ ┌────────────────────────┐ │ │
│ │ │ NAT Gateway │◄─┼────┼──│ Private EC2 outbound │ │ │
│ │ │ Elastic IP attached │ │ │ │ internet traffic │ │ │
│ │ │ Allows outbound internet │ │ │ └────────────────────────┘ │ │
│ │ └──────────────┬───────────────┘ │ │ │ │
│ │ │ │ │ ┌────────────────────────┐ │ │
│ │ ↓ │ │ │ S3 Gateway Endpoint │ │ │
│ │ Internet Gateway │ │ │ Private access to S3 │ │ │
│ │ │ │ └────────────┬───────────┘ │ │
│ │ ┌──────────────────────────────┐ │ │ │ │ │
│ │ │ Application Load Balancer │ │ │ ↓ │ │
│ │ │ Public entry point for apps │ │ │ Amazon S3 │ │
│ │ │ Sends traffic to private apps │──┼────┼──────► Private App Servers │ │
│ │ └──────────────────────────────┘ │ │ │ │
│ └────────────────────────────────────┘ └──────────────────────────────┘ │
│ │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │ VPC Interface Endpoints │ │
│ │ - SSM │ │
│ │ - SSM Messages │ │
│ │ - EC2 Messages │ │
│ │ │ │
│ │ Used by Session Manager to access EC2 without SSH, public IP, or NAT. │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │ VPC Flow Logs │ │
│ │ Captures ACCEPT and REJECT traffic from network interfaces. │ │
│ │ Sent to CloudWatch Logs for debugging. │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────────┐
                           │   CloudWatch Logs     │
                           │ Flow Logs + Insights  │
                           └──────────────────────┘
