## Day 26: Create Application Load Balancer

### What I Learned

- An Application Load Balancer acts as the public entry point for web traffic.
- The ALB is placed in public subnets so users can reach it from the internet.
- Backend EC2 instances remain in private subnets for better security.
- The ALB uses a listener to receive traffic on a specific port.
- For this project, the listener was configured on HTTP port `80`.
- The listener forwards traffic to the Target Group.
- The Target Group then forwards traffic to healthy private EC2 web servers.
- The ALB DNS name can be used to test the application in a browser.
- If the Target Group has no healthy targets, the ALB may return an error like `503`.
- Security Groups must allow the ALB to reach the private EC2 instances on port `80`.

### Practical Work Completed

- Created an internet-facing Application Load Balancer.
- Attached the ALB to two public subnets across different Availability Zones.
- Attached the ALB Security Group.
- Configured an HTTP listener on port `80`.
- Forwarded listener traffic to the Target Group.
- Waited for the private EC2 targets to become healthy.
- Tested the ALB DNS name in the browser.
- Confirmed traffic reached the private EC2 Nginx web servers through the ALB.

### Key Takeaway

The ALB receives public web traffic and safely forwards it to healthy private EC2 instances through the Target Group.
