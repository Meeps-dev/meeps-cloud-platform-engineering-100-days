# Day 36: RDS and Private Database Architecture

## What I Learned

- Amazon RDS is a managed database service for PostgreSQL/MySQL.
- Production databases should be private, not directly exposed to the internet.
- The correct Week 6 flow is: Internet → ALB → Private EC2 Backend → Private RDS.
- A DB subnet group tells RDS which private subnets to use.
- RDS should use private subnets across at least two Availability Zones.
- Security Groups should control access between layers.
- The ALB should be public, but the backend EC2 and RDS should stay private.
- The RDS Security Group should only allow database traffic from the backend EC2 Security Group.
- NAT Gateway or Session Manager helps private EC2 access updates/tools without exposing it publicly.

## What I Built

- Created a fresh Week 6 VPC from scratch.
- Created public subnets for the ALB.
- Created private app subnets for backend EC2.
- Created private DB subnets for future RDS.
- Created Internet Gateway and public route table.
- Created NAT Gateway for private EC2 outbound access.
- Created separate route tables for public, private app, and private DB layers.
- Created Security Groups for ALB, backend EC2, and RDS.
- Launched private EC2 backend with no public IP.
- Connected to the private EC2 using Session Manager.
- Created an ALB and target group.
- Confirmed the ALB could reach the private backend.
- Prepared the DB subnet group for Day 37 RDS setup.

## What I Broke

- I did not have any Week 5 resources left, so I had to rebuild the full Week 6 architecture from scratch.
- I tested how routing affects private resources by checking private subnet access.
- I also reviewed how wrong Security Group rules can block ALB-to-backend communication.

## How I Fixed It

- Recreated the VPC, subnets, route tables, NAT Gateway, ALB, backend EC2, and Security Groups cleanly.
- Ensured the ALB was placed only in public subnets.
- Ensured the backend EC2 was placed in a private app subnet with no public IP.
- Ensured the private app subnet had outbound internet through the NAT Gateway.
- Ensured the private DB subnets had no direct internet route.
- Configured backend EC2 access using Session Manager instead of public SSH.
- Allowed backend traffic only from the ALB Security Group.

## Key Takeaway

- A production-style backend architecture separates public and private resources.
- The internet should only reach the ALB.
- The backend should stay private.
- The database should stay private and only accept traffic from the backend.
