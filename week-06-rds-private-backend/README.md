# Week 6: RDS, PostgreSQL, Backups, and Private Backend Architecture

## Goal

The goal of Week 6 was to understand how production databases are placed privately inside AWS networks and how a backend API securely connects to a private RDS database.

This week focused on building a production-style backend and database architecture using:

- Amazon VPC
- Public and private subnets
- Application Load Balancer
- Private EC2 backend
- FastAPI
- Nginx reverse proxy
- Amazon RDS PostgreSQL
- DB subnet groups
- Security Groups
- Automated backups
- Manual snapshots
- Parameter groups
- Basic secrets handling

## Final Architecture

```text
Internet
  ↓
Application Load Balancer
  ↓
Private EC2 Backend
  ↓
Nginx Reverse Proxy
  ↓
FastAPI Application
  ↓
Private RDS PostgreSQL Database
```

````

## Architecture Explanation

The Application Load Balancer is placed in public subnets so users can access the backend API through the ALB DNS name.

The EC2 backend server is placed in a private subnet and has no public IP address. It is not directly accessible from the internet.

The RDS PostgreSQL database is placed in private DB subnets using a DB subnet group. It has public accessibility disabled and only accepts PostgreSQL traffic from the backend EC2 Security Group.

## Services Used

- **Amazon VPC**: Custom network for the Week 6 architecture.
- **Public Subnets**: Used by the Application Load Balancer.
- **Private App Subnets**: Used by the backend EC2 instance.
- **Private DB Subnets**: Used by the RDS database.
- **Internet Gateway**: Allows public subnets to reach the internet.
- **NAT Gateway**: Allows private EC2 to reach the internet for updates and packages.
- **Application Load Balancer**: Routes public traffic to the private backend.
- **EC2**: Hosts the FastAPI backend application.
- **Nginx**: Reverse proxies traffic from port `80` to FastAPI on `localhost:3000`.
- **FastAPI**: Backend API framework.
- **Amazon RDS PostgreSQL**: Managed relational database.
- **Security Groups**: Controls traffic between ALB, EC2, and RDS.
- **Session Manager**: Secure access to the private EC2 without public SSH.
- **RDS Snapshots**: Used for manual backup and restore testing.
- **Parameter Groups**: Used to inspect and understand database engine settings.

## What I Built

- Created a fresh Week 6 VPC from scratch.
- Created public subnets for the ALB.
- Created private app subnets for the backend EC2.
- Created private DB subnets for RDS.
- Created and configured route tables.
- Created a NAT Gateway for private subnet outbound access.
- Created Security Groups for ALB, backend EC2, and RDS.
- Launched a private EC2 backend server with no public IP.
- Connected to the private EC2 using AWS Systems Manager Session Manager.
- Created a FastAPI backend project named `fastapi-backend-ec2`.
- Pushed the backend code to GitHub.
- Cloned the backend app into the private EC2 instance.
- Configured FastAPI to run on `127.0.0.1:3000`.
- Configured Nginx as a reverse proxy from port `80` to FastAPI.
- Managed the FastAPI app using `systemd`.
- Created an ALB target group with `/health` as the health check endpoint.
- Created a private RDS PostgreSQL database.
- Created a DB subnet group using private DB subnets.
- Connected the FastAPI backend to private RDS using environment variables.
- Created database-backed API endpoints.
- Created a manual RDS snapshot.
- Reviewed automated backups, backup retention, Multi-AZ, and parameter groups.
- Tested the full end-to-end flow through the ALB.

## API Endpoints

| Method | Endpoint   | Purpose                                     |
| ------ | ---------- | ------------------------------------------- |
| GET    | `/health`  | Confirms the backend API is running         |
| GET    | `/db-test` | Confirms FastAPI can connect to private RDS |
| POST   | `/users`   | Creates a user in the PostgreSQL database   |
| GET    | `/users`   | Reads users from the PostgreSQL database    |

## Security Design

- The ALB is public.
- The backend EC2 is private.
- The RDS database is private.
- The backend EC2 has no public IP address.
- The RDS database has `Public accessibility: No`.
- RDS only allows PostgreSQL traffic from the backend EC2 Security Group.
- The backend EC2 only allows HTTP traffic from the ALB Security Group.
- Database credentials are stored using environment variables.
- The real `.env` file is not committed to GitHub.
- A `.env.example` file is used to document required variables safely.

## Security Group Rules

### ALB Security Group

```text
Inbound:
HTTP 80 from 0.0.0.0/0
```

### Backend EC2 Security Group

```text
Inbound:
HTTP 80 from ALB Security Group only
```

### RDS Security Group

```text
Inbound:
PostgreSQL 5432 from Backend EC2 Security Group only
```

## Environment Variables

The backend app uses environment variables for database configuration.

```env
APP_ENV=production
APP_PORT=3000

DB_HOST=<rds-endpoint>
DB_PORT=5432
DB_NAME=appdb
DB_USER=<db-user>
DB_PASSWORD=<db-password>
DB_SSLMODE=require
```

The real values were stored on the EC2 instance and not pushed to GitHub.

## What I Learned

- How production databases are placed in private subnets.
- How RDS uses DB subnet groups.
- Why RDS should not be publicly accessible.
- How Security Groups control communication between ALB, EC2, and RDS.
- How a private EC2 backend connects to a private RDS database.
- How to use environment variables for database configuration.
- How to test database connectivity with `psql`.
- How to use Nginx as a reverse proxy for FastAPI.
- How to manage a backend app with `systemd`.
- How ALB health checks work.
- How RDS automated backups and manual snapshots work.
- How snapshot restore creates a new database instead of overwriting the original one.
- How Multi-AZ improves database availability.
- How parameter groups control database engine settings.
- Why static parameter changes may require a reboot.
- Why secrets should not be hardcoded or committed to GitHub.

## Challenges I Faced and Fixed

### 1. Rebuilding Week 6 Resources from Scratch

I did not have the previous Week 5 infrastructure available, so I had to rebuild the full Week 6 architecture from scratch.

**Fix:**

I recreated the full infrastructure manually:

- VPC
- Public subnets
- Private app subnets
- Private DB subnets
- Internet Gateway
- NAT Gateway
- Route tables
- Security Groups
- Private EC2
- ALB
- Target Group
- DB subnet group
- RDS database

This helped me understand the full architecture better instead of depending on old resources.

---

### 2. Session Manager Could Not Connect to Private EC2

I had issues connecting to the private EC2 instance using AWS Systems Manager Session Manager.

The issue came from the private app route table not being connected to the NAT Gateway. Because of that, the private EC2 could not properly reach the required AWS Systems Manager services.

**Fix:**

I updated the private app route table and added:

```text
0.0.0.0/0 → NAT Gateway
```

I also confirmed:

- NAT Gateway was available.
- NAT Gateway was in a public subnet.
- Public subnet had a route to the Internet Gateway.
- EC2 had the correct IAM role for Session Manager.
- EC2 Security Group allowed outbound traffic.

After fixing the route table, Session Manager connected successfully.

---

### 3. Understanding Private RDS Access

When I tried connecting directly to the RDS endpoint from my laptop, the connection failed.

At first, this looked like an issue, but it was the expected result because the RDS database was private.

**Fix:**

No public access was added.

I confirmed:

- RDS had `Public accessibility: No`.
- RDS was inside private DB subnets.
- RDS Security Group did not allow `0.0.0.0/0`.
- Only the backend EC2 Security Group could access PostgreSQL port `5432`.

This proved the database was correctly private.

---

### 4. Backend Could Not Connect to RDS When Security Group Access Was Broken

I tested what happens when the RDS Security Group does not allow traffic from the backend EC2 Security Group.

The FastAPI `/health` endpoint still worked because it does not touch the database, but `/db-test`, `POST /users`, and `GET /users` failed.

**Fix:**

I restored the RDS inbound rule:

```text
PostgreSQL 5432 → Source: Backend EC2 Security Group
```

After that, the backend API connected to RDS successfully again.

---

### 5. ALB Target Health Issues

At a point, the ALB target could become unhealthy if the backend app, Nginx, or health check path was not configured correctly.

**Fix:**

I checked:

```bash
sudo systemctl status fastapi-backend-ec2
sudo systemctl status nginx
sudo nginx -t
curl http://localhost/health
```

I confirmed the ALB target group health check path was:

```text
/health
```

After restarting the backend service and confirming Nginx was working, the target became healthy again.

---

### 6. FastAPI Service Management

When the FastAPI app was not running, the ALB could not return the correct API response.

**Fix:**

I created a `systemd` service for the FastAPI app.

Useful commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi-backend-ec2
sudo systemctl restart fastapi-backend-ec2
sudo systemctl status fastapi-backend-ec2
```

This allowed the backend app to run persistently and restart automatically if needed.

---

### 7. Environment Variable and Database Credential Issues

Wrong or missing database environment variables can break the `/db-test` and `/users` endpoints.

**Fix:**

I stored database values on the EC2 instance using an environment file and updated the `systemd` service to load it.

I confirmed these values were correct:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_SSLMODE`

After updating the environment file, I restarted the backend service.

```bash
sudo systemctl restart fastapi-backend-ec2
```

---

### 8. Backup and Restore Cost Awareness

I reviewed the snapshot restore process and learned that restoring a snapshot creates a new temporary RDS instance.

This can create extra cost if left running.

**Fix:**

After testing the restore process and taking screenshots, I deleted the temporary restored database to avoid unnecessary billing.

## Testing and Validation

I tested the full flow using the ALB DNS name.

```text
Browser/Postman
  ↓
ALB DNS
  ↓
Private EC2 Backend
  ↓
FastAPI
  ↓
Private RDS PostgreSQL
  ↓
Database response
```

### Tests Performed

```bash
curl http://<ALB-DNS>/health
curl http://<ALB-DNS>/db-test
curl -X POST http://<ALB-DNS>/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Week 6 Test User"}'
curl http://<ALB-DNS>/users
```

### Backend Service Checks

```bash
sudo systemctl status fastapi-backend-ec2
journalctl -u fastapi-backend-ec2 -n 80 --no-pager
sudo nginx -t
sudo systemctl status nginx
```

### Database Connectivity Checks

```bash
nc -zv <rds-endpoint> 5432
psql -h <rds-endpoint> -U <db-user> -d appdb -p 5432
```

## Backup and Recovery

- Confirmed automated backups were enabled.
- Reviewed the backup retention period.
- Created a manual RDS snapshot.
- Reviewed the restore process.
- Confirmed that restoring a snapshot creates a new RDS database.
- Deleted temporary restore resources after testing.

## Screenshots

The following screenshots should be added to the repository:

- VPC overview
- Public and private subnets
- NAT Gateway
- Private route table with NAT Gateway route
- ALB Security Group
- Backend EC2 Security Group
- RDS Security Group showing PostgreSQL `5432` from backend SG only
- Private EC2 with no public IP
- Session Manager connected to private EC2
- ALB target group healthy
- ALB DNS `/health` response
- ALB DNS `/db-test` response
- `POST /users` response
- `GET /users` response
- RDS private subnet configuration
- DB subnet group
- RDS public accessibility set to `No`
- Automated backups enabled
- Manual RDS snapshot
- Parameter group review

## Repository Structure

```text
week-6-rds-private-backend/
│
├── README.md
├── app/
│   └── fastapi-backend-ec2/
│
├── screenshots/
│   ├── vpc-overview.png
│   ├── subnets.png
│   ├── route-tables.png
│   ├── nat-gateway.png
│   ├── session-manager.png
│   ├── alb-target-healthy.png
│   ├── alb-health-check.png
│   ├── rds-private-access.png
│   ├── db-subnet-group.png
│   ├── rds-security-group.png
│   ├── backend-db-test.png
│   ├── users-api-test.png
│   └── rds-snapshot.png
│
└── notes/
    ├── day-36.md
    ├── day-37.md
    ├── day-38.md
    ├── day-39.md
    ├── day-40.md
    ├── day-41.md
    └── day-42.md
```

## Cost Notes

Resources like NAT Gateway, ALB, EC2, RDS, and RDS snapshots can generate cost.

After completing the lab and taking screenshots, I reviewed and cleaned up unused resources.

Resources to review:

- RDS database
- Manual snapshots
- Temporary restored RDS database
- NAT Gateway
- Elastic IP
- ALB
- EC2 instance
- Unused target groups
- Unused Security Groups

## Final Result

At the end of Week 6, I successfully deployed a FastAPI backend API on a private EC2 instance and connected it securely to a private RDS PostgreSQL database.

The final working architecture was:

```text
Internet → ALB → Private EC2 → Nginx → FastAPI → Private RDS PostgreSQL
```

The database was not exposed to the internet, and only the backend EC2 Security Group could connect to it on PostgreSQL port `5432`.

```

```
````
