# Day 42: End-to-End Testing, Debugging, and Documentation

## What I Learned

- End-to-end testing confirms the full application flow works.
- The final flow is:

  `Browser/Postman → ALB DNS → Private EC2 Backend → FastAPI → Private RDS → Database response`

- `/health` checks if the backend app is running.
- `/db-test` confirms the backend can connect to the private RDS database.
- `POST /users` tests writing data into the database.
- `GET /users` tests reading data from the database.
- `systemctl` helps check if the backend service is running.
- `journalctl` helps inspect backend logs during debugging.
- `nginx -t` confirms the Nginx reverse proxy config is valid.
- `psql` and `nc` can test private EC2-to-RDS connectivity.
- Security Groups control whether the backend can reach RDS.

## What I Tested

- Tested `GET /health` through the ALB.
- Tested `GET /db-test` through the ALB.
- Tested `POST /users` through the ALB.
- Tested `GET /users` through the ALB.
- Checked the FastAPI service status.
- Checked Nginx status and configuration.
- Tested PostgreSQL connection from private EC2 to RDS.
- Confirmed data was written to and read from the private RDS database.

## What I Broke

- I tested what happens when the backend service is stopped.
- The ALB could not properly reach the application when FastAPI was down.
- I also tested what happens when RDS access is blocked by the Security Group.
- `/health` could still work if the app was running, but `/db-test` and `/users` failed when DB access was broken.

## How I Fixed It

- Restarted the FastAPI backend service using `systemctl`.
- Checked backend logs using `journalctl`.
- Validated Nginx config with `sudo nginx -t`.
- Restarted Nginx where needed.
- Restored the RDS Security Group rule:

  `PostgreSQL 5432 → Source: Backend EC2 Security Group`

- Retested `/health`, `/db-test`, `POST /users`, and `GET /users`.
- Confirmed the ALB target became healthy again.

## Key Takeaway

- The full private backend architecture worked successfully.
- The internet only reached the ALB.
- The backend EC2 stayed private.
- The RDS database stayed private.
- Only the backend EC2 could connect to the database.
- Final working flow:

  `Internet → ALB → Private EC2 → Nginx → FastAPI → Private RDS PostgreSQL`
