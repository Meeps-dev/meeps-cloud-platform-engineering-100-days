## Day 28: Failure Testing, Debugging, and Documentation

### What I Learned

- ALB uses health checks to detect broken targets.
- The health check path `/` checks if the backend server is responding.
- If a target fails health checks, ALB marks it as unhealthy.
- ALB stops sending normal traffic to unhealthy targets.
- Traffic is routed only to healthy targets.
- A stopped or broken Nginx service can make an EC2 target unhealthy.
- Recovery happens when the issue is fixed and the target passes health checks again.
- Restarting Nginx can make the target healthy again.
- CloudWatch ALB metrics help monitor traffic, errors, and target health.

### Basic ALB Metrics Checked

- `HealthyHostCount` shows the number of healthy targets.
- `UnHealthyHostCount` shows the number of unhealthy targets.
- `RequestCount` shows the number of requests handled by the ALB.
- `TargetResponseTime` shows how long targets take to respond.
- `HTTPCode_ELB_5XX_Count` shows errors from the ALB.
- `HTTPCode_Target_5XX_Count` shows errors from the backend targets.

### What I Broke and How I Fixed It

- I stopped Nginx on one private EC2 instance.
- The Target Group detected the failure and marked the instance as unhealthy.
- The ALB stopped routing traffic to the unhealthy target.
- I restarted Nginx on the instance.
- After the health checks passed, the target became healthy again.

### Key Takeaway

ALB health checks help keep applications available by removing broken targets from traffic and adding them back after recovery.
