The roadmap defines Week 7 as **IAM, Security, Secrets, KMS, CloudTrail, and Audit**, with proof required for IAM roles, least-privilege policies, Secrets Manager/SSM, CloudTrail, Budget, and debugging notes.

````md
# Week 7: IAM, Security, Secrets, KMS, CloudTrail, and Audit

## Goal

Secure the existing Meeps backend infrastructure by removing hardcoded credentials, replacing broad permissions with least-privilege IAM policies, enabling audit logging, and adding cost controls.

This week focused on securing the existing Week 6 architecture:

```text
User
  -> Application Load Balancer
  -> Private EC2 FastAPI Backend
  -> Private RDS Database
```
````

After Week 7, the backend uses secure AWS access patterns:

```text
User
  -> ALB
  -> EC2 FastAPI Backend
       -> IAM Role: meeps-week7-ec2-role
       -> Secrets Manager: meeps/week7/rds
       -> SSM Parameter Store SecureString
       -> S3 Read-Only Prefix Access
       -> Private RDS

CloudTrail
  -> AWS API Audit Logs

AWS Config
  -> Resource Configuration History

GuardDuty
  -> Threat Detection Review

AWS Budgets
  -> Cost Alerting
```

---

## Services Used

- AWS IAM
- IAM Roles
- IAM Policies
- EC2 Instance Profile
- AWS Secrets Manager
- AWS Systems Manager Parameter Store
- AWS KMS
- Amazon S3
- Amazon RDS
- Application Load Balancer
- AWS CloudTrail
- AWS Config
- Amazon GuardDuty
- AWS Budgets
- AWS Systems Manager Session Manager
- FastAPI
- boto3

---

## What I Learned

- Difference between IAM users and IAM roles.
- Why EC2 should use IAM roles instead of long-term AWS access keys.
- How least-privilege IAM policies reduce security risk.
- How to move database credentials from `.env` into AWS Secrets Manager.
- How FastAPI can use `boto3` to read secrets securely.
- How SSM Parameter Store SecureString works with KMS encryption.
- How KMS supports encryption and decryption for AWS-managed secrets.
- How to give EC2 read-only access to a specific S3 bucket prefix.
- How CloudTrail helps audit AWS API activity.
- How AWS Config tracks infrastructure configuration changes.
- How GuardDuty supports threat detection.
- How AWS Budgets helps prevent unexpected billing.
- Why security, auditing, and cost control must be part of cloud infrastructure from the start.

---

## Architecture Summary

The existing FastAPI backend runs on EC2 behind an Application Load Balancer. The database is hosted on private RDS. During Week 7, I secured the backend by attaching an IAM role to EC2, storing database credentials in Secrets Manager, creating least-privilege access to S3, enabling audit logging with CloudTrail, testing AWS Config, reviewing GuardDuty, and creating an AWS Budget.

```text
Internet User
  |
  v
Application Load Balancer
  |
  v
Private EC2 FastAPI Backend
  |
  |-- Reads DB credentials from Secrets Manager
  |-- Reads test SecureString from SSM Parameter Store
  |-- Reads only approved S3 prefix
  |-- Connects to Private RDS
  |
  v
Private RDS Database
```

Audit and operations layer:

```text
CloudTrail -> Tracks AWS API activity
AWS Config -> Tracks configuration changes
GuardDuty -> Reviews threat detection findings
AWS Budgets -> Sends cost threshold alerts
```

---

## Implementation Summary

### Day 43: IAM Foundation and Security Audit

I reviewed the current setup before making changes.

Checked:

- EC2 backend
- RDS database
- S3 bucket
- Application Load Balancer
- Security Groups
- `.env` files
- `systemd` backend service
- AWS access keys on the server
- GitHub repository
- Terminal history
- Deployment scripts

Key checks used:

```bash
printenv | grep AWS
printenv | grep DB
cat .env
sudo systemctl cat fastapi-backend-ec2
history | grep AWS
history | grep DB
```

Security focus:

- Avoid exposing DB passwords.
- Avoid storing AWS keys on EC2.
- Avoid committing `.env` files to GitHub.
- Avoid showing secret values in screenshots.

---

### Day 44: Attach IAM Role to EC2

Created an IAM role for the backend EC2 instance.

```text
Role name: meeps-week7-ec2-role
Trusted entity: EC2
Use case: Backend app permissions
```

Attached the role to the EC2 instance:

```text
EC2
  -> Instances
  -> Select backend instance
  -> Actions
  -> Security
  -> Modify IAM role
  -> Attach meeps-week7-ec2-role
```

Verified the role from inside EC2 using SSM Session Manager:

```bash
aws sts get-caller-identity
```

Expected result:

```text
assumed-role/meeps-week7-ec2-role
```

This confirmed that the EC2 instance was using the IAM role instead of long-term AWS access keys.

---

### Day 45: Move DB Credentials to Secrets Manager

Created a Secrets Manager secret for RDS credentials.

```text
Secret name: meeps/week7/rds
```

Secret format:

```json
{
  "DB_HOST": "REDACTED",
  "DB_PORT": "5432",
  "DB_NAME": "REDACTED",
  "DB_USER": "REDACTED",
  "DB_PASSWORD": "REDACTED"
}
```

Created a least-privilege IAM policy allowing the EC2 role to read only this secret:

```json
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue"],
  "Resource": "arn:aws:secretsmanager:eu-west-2:ACCOUNT_ID:secret:meeps/week7/rds-*"
}
```

Updated the FastAPI backend to retrieve credentials from Secrets Manager using `boto3`.

Added only non-secret environment variables to the `systemd` service:

```ini
[Service]
Environment="AWS_REGION=eu-west-2"
Environment="DB_SECRET_ID=meeps/week7/rds"
```

Created one SSM Parameter Store SecureString for practice:

```text
/meeps/week7/test-secure-param
```

Tested:

```bash
sudo systemctl restart fastapi-backend-ec2
sudo systemctl status fastapi-backend-ec2 --no-pager
curl http://localhost:3000/health
curl http://localhost:3000/db-test
```

Result:

```text
FastAPI backend reads RDS credentials from Secrets Manager and connects to private RDS successfully.
```

---

### Day 46: Create Least-Privilege S3 Read Policy

Created an S3 read-only IAM policy.

```text
Policy name: meeps-week7-s3-read-only-policy
```

Allowed EC2 to read only from:

```text
s3-bucket-meeps/week7-read-only/
```

Allowed actions:

```text
s3:ListBucket
s3:GetObject
```

Denied by default:

```text
s3:PutObject
s3:DeleteObject
s3:*
AmazonS3FullAccess
AdministratorAccess
```

Tested the IAM role:

```bash
aws sts get-caller-identity
```

Confirmed:

```text
assumed-role/meeps-week7-ec2-role
```

Tested allowed read:

```bash
aws s3 ls s3://s3-bucket-meeps/week7-read-only/
aws s3 cp s3://s3-bucket-meeps/week7-read-only/index.txt /tmp/index.txt
```

Tested denied write:

```bash
echo "day46 least privilege test" > /tmp/test.txt
aws s3 cp /tmp/test.txt s3://s3-bucket-meeps/week7-read-only/test.txt
```

Expected result:

```text
AccessDenied
```

This proved the EC2 role had read access only and could not write to the bucket.

---

### Day 47: CloudTrail and AWS Config

Created a CloudTrail trail for account-level audit logging.

```text
Trail name: meeps-week7-trail
```

Configured:

- Multi-region trail
- Log file validation
- Private S3 log bucket
- Encryption
- Management events

Generated test AWS activity:

```bash
aws secretsmanager get-secret-value --secret-id meeps/week7/rds --query ARN
aws s3 ls s3://s3-bucket-meeps/week7-read-only/
```

Reviewed CloudTrail Event History for:

- `GetSecretValue`
- `ListBucket`
- `AttachRolePolicy`
- `AccessDenied`
- IAM role activity

Enabled AWS Config for audit practice and reviewed how it tracks configuration changes.

Cost decision:

```text
AWS Config was enabled for Day 47 audit practice and stopped after screenshots for cost control.
```

---

### Day 48: GuardDuty and AWS Budgets

Reviewed GuardDuty as AWS threat detection.

GuardDuty focus:

- Suspicious API activity
- Possible compromised credentials
- Unusual account behavior
- Security findings

Challenge:

```text
GuardDuty was restricted on my current AWS free-plan/free-tier account.
```

Fix:

```text
I proceeded and tested/reviewed GuardDuty using another AWS account where the service was accessible.
```

Created an AWS Budget:

```text
Budget name: meeps-week7-budget
Budget type: Cost budget
Budget amount: $5.00
```

Budget alerts:

```text
Actual cost > 70%
Forecasted cost > 100%
```

Applied tags to Week 7 resources where possible:

```text
project=meeps
week=week-7
owner=kehinde
environment=dev
```

Tagged resources:

- EC2
- RDS
- S3 bucket
- IAM role
- Secrets Manager secret
- CloudTrail S3 log bucket
- KMS key if applicable
- VPC endpoints if applicable

---

## Challenges Faced and How I Fixed Them

### 1. SSM Session Manager Instead of SSH

**Challenge**

I was connected to the EC2 instance using SSM Session Manager instead of SSH, so I needed to confirm how to inspect files, services, and environment variables correctly.

**Fix**

I treated the SSM session as a normal EC2 shell and used:

```bash
sudo -i
whoami
systemctl cat fastapi-backend-ec2
```

This allowed me to inspect the backend service, `.env` files, and application directory safely.

---

### 2. Backend Was FastAPI, Not Node.js

**Challenge**

The initial secret-loading plan needed adjustment because my backend uses FastAPI, not Node.js.

**Fix**

I used Python `boto3` instead of the Node.js AWS SDK.

FastAPI now retrieves secrets from Secrets Manager using:

```text
boto3 -> secretsmanager:GetSecretValue -> meeps/week7/rds
```

---

### 3. systemd Environment Override Confusion

**Challenge**

I needed to confirm whether adding `AWS_REGION` and `DB_SECRET_ID` to the `systemd` override file was correct.

**Fix**

I added only non-secret values to the service override:

```ini
[Service]
Environment="AWS_REGION=eu-west-2"
Environment="DB_SECRET_ID=meeps/week7/rds"
```

I did not put DB passwords inside systemd.

---

### 4. Existing EnvironmentFile Could Still Contain Old Secrets

**Challenge**

The backend service still referenced an environment file:

```text
EnvironmentFile=/etc/fastapi-backend-ec2.env
```

This meant old DB credentials could still exist there.

**Fix**

I checked the file using redacted commands and planned to remove DB credentials only after confirming the backend worked with Secrets Manager.

---

### 5. S3 Command Format Error

**Challenge**

While testing S3 access, I initially used the wrong S3 path format by adding an extra space before the object path.

Example issue:

```bash
aws s3 ls s3://s3-bucket-meeps /index.html/
```

**Fix**

I corrected the command format:

```bash
aws s3 ls s3://s3-bucket-meeps/week7-read-only/
```

---

### 6. Tried to Download an Object That Did Not Exist

**Challenge**

I tried to download:

```text
sample.txt
```

but the object did not exist in the prefix.

**Fix**

I listed the prefix first, confirmed the actual file was:

```text
index.txt
```

Then downloaded the correct object:

```bash
aws s3 cp s3://s3-bucket-meeps/week7-read-only/index.txt /tmp/index.txt
```

---

### 7. S3 Upload Failed With AccessDenied

**Challenge**

Uploading to the S3 prefix failed with:

```text
AccessDenied
```

**Fix**

I did not “fix” this by adding write permission because the failure was expected.

The role was intentionally read-only, so the denied upload proved least privilege was working.

---

### 8. Listing the Full S3 Bucket Failed

**Challenge**

Listing the full bucket failed with `AccessDenied`.

**Fix**

This was also expected because the policy only allowed listing the approved prefix.

The correct allowed command was:

```bash
aws s3 ls s3://s3-bucket-meeps/week7-read-only/
```

---

### 9. CloudTrail Events Did Not Appear Immediately

**Challenge**

Some CloudTrail events did not show instantly after generating activity.

**Fix**

I waited a few minutes and searched Event History again.

I also focused on management events such as:

```text
GetSecretValue
AttachRolePolicy
AccessDenied
```

---

### 10. S3 Object-Level Events Were Limited

**Challenge**

S3 object-level activity did not fully appear in CloudTrail Event History because full S3 data events were not enabled.

**Fix**

I documented that S3 data events can add cost and skipped broad S3 data event logging for cost control.

---

### 11. AWS Config Cost Concern

**Challenge**

AWS Config is useful, but it can add cost when left running.

**Fix**

I enabled AWS Config for Day 47 audit practice, captured screenshots, and stopped it afterward for cost control.

---

### 12. GuardDuty Account Access Limitation

**Challenge**

My current AWS account was on a free-plan/free-tier setup and GuardDuty access was restricted.

**Fix**

I proceeded and figured out GuardDuty using another AWS account where the service was accessible.

I documented the limitation and continued with the AWS Budget and tagging tasks.

---

## Security Decisions

- Used IAM role instead of AWS access keys on EC2.
- Removed dependency on hardcoded DB credentials.
- Stored RDS credentials in Secrets Manager.
- Used SSM Parameter Store SecureString for practice.
- Gave EC2 permission to read only the required secret.
- Created S3 read-only access for only one bucket prefix.
- Did not use `AdministratorAccess`.
- Did not use `AmazonS3FullAccess`.
- Did not use `s3:*`.
- Did not make the S3 bucket public.
- Kept CloudTrail log bucket private.
- Avoided exposing real secret values in screenshots or GitHub.
- Used AWS Budgets for cost control.

---

## Cost Decisions

- Created a monthly AWS Budget named `meeps-week7-budget`.
- Set the budget amount to `$5.00`.
- Added alerts for:
  - Actual cost above `70%`
  - Forecasted cost above `100%`

- Stopped AWS Config after screenshots for cost control.
- Avoided broad S3 data event logging to reduce unnecessary cost.
- Reviewed GuardDuty carefully because account plan and billing limitations applied.
- Continued using cost-aware tagging across Week 7 resources.

---

## Screenshots / GitHub Proof

Add screenshots for:

- IAM role: `meeps-week7-ec2-role`
- EC2 instance showing attached IAM role
- `aws sts get-caller-identity` showing assumed role
- Secrets Manager secret: `meeps/week7/rds`
- SSM SecureString parameter
- Least-privilege S3 read policy
- Successful S3 read/list test
- Failed S3 write test with `AccessDenied`
- CloudTrail trail: `meeps-week7-trail`
- CloudTrail Event History
- AWS Config setup/resource timeline
- AWS Config stopped for cost control
- GuardDuty review/findings/settings
- AWS Budget: `meeps-week7-budget`
- Budget alerts
- Resource tags

---

## Commands Used

```bash
# Verify EC2 role identity
aws sts get-caller-identity

# Check systemd service
sudo systemctl cat fastapi-backend-ec2
sudo systemctl status fastapi-backend-ec2 --no-pager

# Restart backend
sudo systemctl daemon-reload
sudo systemctl restart fastapi-backend-ec2

# Test backend locally
curl http://localhost:3000/health
curl http://localhost:3000/db-test

# Test Secrets Manager access safely
aws secretsmanager get-secret-value \
  --secret-id meeps/week7/rds \
  --query ARN \
  --output text \
  --region eu-west-2

# Test S3 read access
aws s3 ls s3://s3-bucket-meeps/week7-read-only/

# Download allowed object
aws s3 cp s3://s3-bucket-meeps/week7-read-only/index.txt /tmp/index.txt

# Test denied S3 write access
echo "day46 least privilege test" > /tmp/test.txt
aws s3 cp /tmp/test.txt s3://s3-bucket-meeps/week7-read-only/test.txt

# Search for CloudTrail events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=GetSecretValue \
  --region eu-west-2 \
  --max-results 5
```

---

## Final Outcome

By the end of Week 7:

- EC2 uses an IAM role instead of access keys.
- FastAPI retrieves DB credentials from Secrets Manager.
- DB credentials are no longer hardcoded in `.env`.
- SSM SecureString was created for practice.
- S3 access is limited to read-only access on one prefix.
- S3 write access fails with `AccessDenied` as expected.
- CloudTrail is enabled for audit visibility.
- AWS Config was tested and stopped for cost control.
- GuardDuty was reviewed using an accessible AWS account.
- AWS Budget was created with alerts.
- Week 7 resources were tagged for organization and cost tracking.

---

## What I Would Improve in Production

- Use IAM Identity Center for human access instead of long-term IAM users.
- Add automatic Secrets Manager rotation for RDS credentials.
- Use customer-managed KMS keys where stronger key control is required.
- Enable selected CloudTrail data events only for critical buckets.
- Send CloudTrail logs to a centralized security account.
- Keep AWS Config enabled with carefully selected rules in production.
- Add GuardDuty across all production accounts and regions.
- Use AWS Organizations and Service Control Policies for stronger guardrails.
- Use VPC endpoints for Secrets Manager, SSM, and S3 to reduce dependency on NAT Gateway.
- Automate IAM, Secrets Manager, CloudTrail, and budgets later with Infrastructure as Code.

---

## Key Takeaway

Week 7 moved the Meeps platform from a basic working backend setup to a more secure, auditable, and cost-aware cloud environment. The most important lesson was that production cloud engineering is not just about making services work; it is about making them work securely, with least privilege, audit visibility, and cost control.

```

```
