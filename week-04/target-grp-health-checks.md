## Day 25: Target Groups and Health Checks

### What I Learned

- A Target Group is where backend servers are registered.
- The ALB forwards traffic to the Target Group.
- For this project, my targets are two private EC2 web servers.
- Targets can be registered by selecting the EC2 instances inside the correct VPC.
- Health checks help the ALB know if a server is working.
- The health check path `/` checks if Nginx responds successfully.
- A `200 OK` response means the server is reachable and working.
- A healthy target can receive traffic from the ALB.
- An unhealthy target will not receive normal traffic.
- If Nginx is stopped or port 80 is blocked, the target may become unhealthy.
- If the Target Group is not yet attached to an ALB listener, the target may show as `unused`.

### Practical Work Completed

- Created a Target Group for the private web servers.
- Selected target type as `Instances`.
- Used protocol `HTTP` and port `80`.
- Configured the health check path as `/`.
- Set expected success code as `200`.
- Registered both private EC2 instances.
- Confirmed both servers were listed in the Target Group.

### Key Takeaway

Target Groups connect the ALB to backend servers, while health checks make sure only working servers receive traffic.
