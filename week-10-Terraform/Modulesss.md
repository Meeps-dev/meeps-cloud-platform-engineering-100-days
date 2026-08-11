# Day 69 — Private RDS and Application S3 with Terraform

## Objective

Build reusable Terraform modules for a private PostgreSQL database and a secure application S3 bucket, connect them to the development environment, and verify their security controls.

## Resources Built

### Amazon RDS

- PostgreSQL 16 database using `db.t3.micro`
- RDS subnet group spanning two private database subnets
- Storage encryption enabled
- Public accessibility disabled
- One-day automated backup retention
- TCP port 5432 allowed only from the application security group
- Master credentials generated and managed by Amazon RDS through AWS Secrets Manager
- Automatic secret rotation enabled

### Amazon S3

- Private application bucket with a globally unique name
- All four S3 Block Public Access controls enabled
- ACLs disabled with `BucketOwnerEnforced`
- Object versioning enabled
- SSE-S3 encryption using AES256
- Bucket ARN and name exposed through Terraform outputs

## Verification Results

- Terraform applied exactly 7 resources.
- Apply result: `7 added, 0 changed, 0 destroyed`
- RDS status: `available`
- RDS publicly accessible: `false`
- RDS storage encrypted: `true`
- RDS master secret status: `active`
- Database subnets have no default internet route.
- No public IPv4 or IPv6 RDS ingress exists.
- S3 public-access blocks: enabled
- S3 versioning: enabled
- S3 encryption: AES256
- S3 ownership: BucketOwnerEnforced
- Final Terraform plan reported no infrastructure changes.

## What I Learned

- An RDS subnet group should span private subnets in at least two Availability Zones.
- Security-group references provide safer service-to-service access than public CIDR rules.
- RDS can generate and rotate its master password through Secrets Manager without storing a plaintext password in Terraform configuration.
- A private RDS database needs neither a public IP nor an internet default route.
- S3 is not deployed inside a subnet; access is secured using authorization, ownership controls, encryption, and Block Public Access.
- Saved Terraform plans allow the exact reviewed infrastructure changes to be applied.
- A post-apply plan is an effective way to confirm that deployed infrastructure matches the configuration.

## What Broke and How I Fixed It

### Terraform was run from the repository root

Terraform returned `No configuration files` because the command was executed outside `infra/terraform/envs/dev`.

**Fix:** I changed into the development environment before running Terraform commands and regenerated the saved plan.

### Remote state access timed out

Terraform temporarily timed out while reading the remote S3 state.

**Fix:** I verified the AWS account and state bucket, restored a stable network connection, retained state locking, and retried successfully.

### A stale saved-plan file caused confusion

The failed plan command left an older file visible in `/tmp`.

**Fix:** I regenerated the plan from the correct directory, inspected its seven resource addresses, and applied only the reviewed plan.

### Systems Manager connectivity test was unavailable

The backend instance returned an SSM status of `None`, and Run Command returned `InvalidInstanceId`.

**Fix:** I treated the live EC2-to-RDS TCP test as skipped instead of weakening database security. The database path was verified through security groups, private subnet routing, and Terraform state. SSM connectivity can later be enabled through NAT or the required VPC interface endpoints.

## Final Result

Day 69 successfully provisioned an encrypted private PostgreSQL database and a secure application S3 bucket using reusable Terraform modules. The final Terraform plan reported no drift.
