## Day 23: Prepare Multi-AZ Network

### What I Learned

- Multi-AZ means spreading resources across more than one Availability Zone.
- Multi-AZ design improves availability if one AZ has issues.
- Public subnets are used for resources that need internet access, like ALB and NAT Gateway.
- Private subnets are used for backend servers that should not be directly exposed to the internet.
- An Internet Gateway allows public subnets to reach the internet.
- A NAT Gateway allows private instances to access the internet for updates and package installation.
- Public route tables use `0.0.0.0/0 → Internet Gateway`.
- Private route tables use `0.0.0.0/0 → NAT Gateway`.
- ALB needs public subnets in at least two Availability Zones.
- Private EC2 instances should sit behind the ALB for better security.
- Users should access the application through the ALB, not directly through EC2.
- Systems Manager Session Manager can be used instead of a Bastion Host.
- Using Session Manager reduces the need for inbound SSH access.

### Network Setup Created

- Created a new Week 4 VPC.
- Created 2 public subnets across different Availability Zones.
- Created 2 private subnets across different Availability Zones.
- Created and attached an Internet Gateway.
- Created a public route table for internet access.
- Created a NAT Gateway for private subnet outbound access.
- Created a private route table pointing to the NAT Gateway.
- Prepared Security Groups for the ALB and private EC2 instances.
- Created an IAM role for EC2 access through Systems Manager.

### Key Takeaway

A proper Multi-AZ network separates public and private resources. The ALB stays public, while backend EC2 instances stay private and are accessed securely through the ALB and Systems Manager.
