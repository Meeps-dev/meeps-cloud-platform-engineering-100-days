## Day 68: Terraform ALB and Private EC2

## What I Learned

- Built reusable Terraform modules for an Application Load Balancer and EC2 backend.
- Deployed an ALB across two public subnets.
- Registered a private EC2 instance with an ALB target group.
- Configured port 8080 and the /health endpoint for health checks.
- Used EC2 user data and systemd to run a Python backend automatically.
- Secured EC2 with no public IP, encrypted EBS and required IMDSv2.
- Allowed backend traffic only from the ALB security group.
- Deployed without a NAT Gateway by using the preinstalled Python runtime.

## What Broke

- The initial root configuration did not expose the required ALB and EC2 outputs.
- The first Git push failed because my system could not resolve github.com.

## How I Fixed It

- Added outputs for the ALB DNS, target group ARN, EC2 ID and private IP.
- Regenerated and reviewed the saved Terraform plan before applying.
- Resolved the temporary DNS/network issue and retried the Git push.
- Verified the target was healthy, /health returned HTTP 200, and terraform plan reported No changes.

## Final Traffic Flow

Internet → ALB :80 → Private EC2 :8080 → /health
