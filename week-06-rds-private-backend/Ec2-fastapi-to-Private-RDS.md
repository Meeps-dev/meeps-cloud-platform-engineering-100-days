# Day 39: Connect Backend API to Private RDS

## What I Learned

- The backend API connects to RDS using a database connection string.
- PostgreSQL uses port `5432`.
- The RDS endpoint is used as the database host.
- Database credentials should be stored with environment variables, not hardcoded in code.
- `psql` can be used from the private EC2 to test database connectivity.
- The backend EC2 can connect to RDS privately inside the VPC.
- The RDS Security Group should only allow PostgreSQL traffic from the backend EC2 Security Group.
- The correct flow is:

  `ALB → Private EC2 Backend → Private RDS PostgreSQL`

## What I Built

- Installed PostgreSQL client on the private EC2.
- Tested RDS connection from the private EC2 using `psql`.
- Created a `users` table inside the `appdb` database.
- Updated the FastAPI backend to connect to PostgreSQL.
- Added database-backed API endpoints:
  - `GET /db-test`
  - `POST /users`
  - `GET /users`
- Stored database values using environment variables.
- Confirmed the API could return data from private RDS through the ALB.

## What I Broke

- I tested what happens when the RDS Security Group does not allow traffic from the backend EC2 Security Group.
- The backend could not connect to the database.
- `/health` still worked because it does not touch the database.
- `/db-test`, `POST /users`, and `GET /users` failed because they depend on RDS.
- I also tested how wrong database credentials or environment variables can break the app connection.

## How I Fixed It

- Restored the RDS Security Group rule:

  `PostgreSQL 5432 → Source: Backend EC2 Security Group`

- Checked that the RDS endpoint, database name, username, password, and port were correct.
- Restarted the FastAPI `systemd` service after updating environment variables.
- Checked backend logs using `journalctl`.
- Retested `/db-test`, `POST /users`, and `GET /users` through the ALB.

## Key Takeaway

- The database stayed private and was not exposed to the internet.
- Only the backend EC2 could connect to RDS.
- The final working flow was:

  `Internet → ALB → Private EC2 → FastAPI → Private RDS PostgreSQL`
