## Day 22: Understand Load Balancing

### What I Learned

- A Load Balancer distributes traffic across multiple servers.
- It helps prevent one server from being overloaded.
- It improves availability because traffic can be sent to healthy servers if one server fails.
- Backend servers should not be exposed directly to the internet.
- Keeping backend servers private reduces security risks.
- Users should access the application through the Load Balancer, not directly through EC2 public IPs.
- An Application Load Balancer handles HTTP and HTTPS traffic.
- ALB works well for websites, APIs, and web applications.
- ALB forwards traffic to backend servers through a Target Group.
- ALB uses health checks to know which servers are healthy.
- ALB works at Layer 7, while NLB works at Layer 4.
- NLB is better for TCP/UDP and very high-performance network traffic.
- In a VPC, the ALB is placed in public subnets.
- The backend EC2 instances are placed in private subnets.
- The private EC2 Security Group should allow traffic only from the ALB Security Group.

### Simple Traffic Flow

Internet → Application Load Balancer → Target Group → Private EC2 Web Servers

### Key Takeaway

A Load Balancer acts as the public entry point for an application, while the backend servers stay private and protected inside the VPC.
