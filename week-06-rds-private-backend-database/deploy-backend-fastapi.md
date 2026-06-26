# Day 38: Deploy Backend API on Private EC2

## What I Learned

- A backend API can run on a private EC2 instance with no public IP.
- Users should not access the backend EC2 directly.
- Public traffic should enter through the ALB.
- Nginx can be used as a reverse proxy from port `80` to the FastAPI app on `localhost:3000`.
- A `/health` endpoint is used by the ALB to check if the backend is healthy.
- Environment variables help manage app configuration without hardcoding values.
- `systemd` helps keep the FastAPI app running after the terminal closes.
- Session Manager allows secure access to private EC2 without opening SSH.

## What I Built

- Created a FastAPI backend project called `fastapi-backend-ec2`.
- Added basic API routes:
  - `GET /health`
  - `GET /db-test`
  - `POST /users`
  - `GET /users`
- Pushed the backend app to GitHub.
- Cloned the GitHub repo into the private EC2 instance.
- Installed Python, Git, FastAPI dependencies, and Nginx on EC2.
- Ran FastAPI on `127.0.0.1:3000`.
- Configured Nginx to forward traffic from port `80` to FastAPI.
- Created a `systemd` service to manage the FastAPI app.
- Connected the ALB target group health check to `/health`.
- Confirmed the ALB could reach the private backend API.

## What I Broke / Challenges I Faced

- I had issues connecting to the private EC2 using Session Manager.
- The issue was caused by the private route table not having a route to the NAT Gateway.
- Because of that, the private EC2 could not properly reach the required AWS Systems Manager services.
- I also tested how stopping the FastAPI service affects the backend health check.
- When the backend app was not running, Nginx/ALB could not serve the API correctly.

## How I Fixed It

- I updated the private app subnet route table.
- Added the correct route:

  `0.0.0.0/0 → NAT Gateway`

- Confirmed the NAT Gateway was in a public subnet with internet access.
- Confirmed the private EC2 had the correct IAM role for Session Manager.
- Reconnected to the private EC2 successfully using Session Manager.
- Restarted the FastAPI `systemd` service.
- Restarted and tested Nginx.
- Confirmed the ALB target became healthy again.

## Key Takeaway

- Private EC2 instances need proper outbound access for tools like Session Manager and package installation.
- The private backend should not be exposed directly to the internet.
- The correct flow is:

  `Internet → ALB → Private EC2 → Nginx → FastAPI`
