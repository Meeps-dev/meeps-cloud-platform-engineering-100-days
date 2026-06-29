# Day 44: Attach IAM Role to EC2 Instead of Using Access Keys

## Goal

Attach an IAM role to the backend EC2 instance so the server can use temporary AWS credentials instead of long-term access keys.

## What I Did

- Created IAM role `meeps-week7-ec2-role`
- Set trusted entity to EC2
- Attached the role to the backend EC2 instance
- Removed AWS access keys from the shell, `.env`, systemd, and AWS credential files where present
- Confirmed role identity using `aws sts get-caller-identity`
- Verified the private EC2 can reach AWS services through the existing NAT Gateway

## Result

The EC2 backend now uses an IAM instance profile instead of static AWS access keys.

## Security Decision

I did not attach `AdministratorAccess`. I kept the role minimal and will add exact Secrets Manager/SSM and S3 permissions in the next tasks.

## Cost Note

The NAT Gateway is still present because the private EC2 needs outbound access for this lab. I will review and remove it when it is no longer actively needed.
