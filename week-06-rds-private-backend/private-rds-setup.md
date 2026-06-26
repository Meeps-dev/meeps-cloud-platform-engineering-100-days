# Day 37: Private RDS Setup

## What I Learned

- RDS is used to run managed relational databases like PostgreSQL/MySQL.
- A DB subnet group tells RDS which private subnets to use.
- RDS should be placed in private subnets across at least two Availability Zones.
- PostgreSQL uses port `5432`; MySQL uses port `3306`.
- RDS should have `Public accessibility: No`.
- The RDS Security Group should only allow database traffic from the backend EC2 Security Group.
- Direct laptop access to private RDS should fail because the database is not public.
- Correct flow: Internet → ALB → Private EC2 Backend → Private RDS.

## What I Built

- Created a DB subnet group using private DB subnets.
- Created a private PostgreSQL RDS database.
- Set database name to `appdb`.
- Set RDS port to `5432`.
- Enabled automated backups.
- Attached the RDS Security Group.
- Allowed PostgreSQL access only from the backend EC2 Security Group.

## What I Broke

- I tested direct connection from my laptop to the RDS endpoint.
- The connection failed, which confirmed the database was private.
- I also reviewed how wrong Security Group rules can block backend-to-database access.

## How I Fixed It

- Confirmed RDS had `Public accessibility: No`.
- Confirmed RDS was using the private DB subnet group.
- Removed any public database access rule.
- Allowed inbound PostgreSQL `5432` only from the backend EC2 Security Group.
- Verified that private EC2 is the correct access point to the database.

## Key Takeaway

- A production database should not be exposed to the internet.
- Only the backend application should connect to RDS.
- Security Groups are the main control for allowing backend-to-database access.
