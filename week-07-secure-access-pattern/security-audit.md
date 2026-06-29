# Day 43: IAM Foundation and Current Security Audit

## Goal

Audit my existing Week 6 cloud setup before replacing hardcoded credentials and broad permissions with secure AWS access patterns.

## Resources Checked

- EC2 backend
- RDS database
- S3 bucket
- Application Load Balancer
- Security Groups
- .env files
- systemd backend service
- AWS CLI credentials
- Terminal history
- GitHub repository

## Findings

### EC2 Backend

- EC2 instance found: Yes
- IAM role attached: Yes/No
- Public IP attached: Yes/No
- Backend Security Group reviewed: Yes

### RDS Database

- Public access disabled: Yes/No
- DB Security Group allows traffic only from backend SG: Yes/No
- DB credentials currently hardcoded: Yes/No

### S3 Bucket

- Block Public Access enabled: Yes/No
- Bucket policy reviewed: Yes
- Encryption enabled: Yes/No

### ALB

- ALB routes traffic to backend: Yes/No
- Target group healthy: Yes/No
- ALB Security Group reviewed: Yes

### Secrets Audit

- .env file found: Yes/No
- DB password found in .env: Yes/No
- AWS access keys found on EC2: Yes/No
- Secrets found in systemd service: Yes/No
- Secrets found in terminal history: Yes/No
- Secrets found in GitHub repo: Yes/No

## Security Risks Found

- Hardcoded DB credentials need to be moved to Secrets Manager or SSM.
- EC2 should use an IAM role instead of access keys.
- S3 permissions need to follow least privilege.
- Security Groups should allow only required traffic.

## Next Action

On Day 44, I will create and attach an IAM role to the EC2 backend so the instance can securely access AWS services without long-term access keys.
