# Day 45: Move DB Credentials to Secrets Manager

## What I Learned

- Learned the difference between **AWS Secrets Manager** and **SSM Parameter Store**.
- Used **Secrets Manager** for RDS database credentials because it is better for sensitive secrets.
- Learned that **SSM Parameter Store SecureString** can also store encrypted values using KMS.
- Learned that EC2 can read secrets securely using an **IAM role**, not hardcoded AWS access keys.
- Learned that FastAPI can use `boto3` to fetch secrets from AWS Secrets Manager.
- Learned that only non-secret values like `AWS_REGION` and `DB_SECRET_ID` should be added to `systemd`.
- Confirmed that real DB passwords should not be stored in `.env`, GitHub, screenshots, or service files.

## What I Did

- Created a Secrets Manager secret for my RDS credentials.
- Used the secret name: `meeps/week7/rds`.
- Added a least-privilege IAM policy to allow EC2 to read only that secret.
- Updated my FastAPI backend to load database credentials from Secrets Manager.
- Added non-secret environment variables to the `fastapi-backend-ec2` systemd service:
  - `AWS_REGION`
  - `DB_SECRET_ID`
- Created one SSM SecureString parameter for practice:
  - `/meeps/week7/test-secure-param`
- Tested the backend locally and through the ALB.

## What I Broke / Issue Faced

- I initially needed to clarify how to do the setup because I was connected through **SSM Session Manager**, not SSH.
- I also had to adjust the implementation because my backend uses **FastAPI**, not Node.js.
- I noticed that the service still referenced an `EnvironmentFile`, meaning old DB values could still exist there.
- The backend could fail if `AWS_REGION` or `DB_SECRET_ID` is missing from the systemd service.

## How I Fixed It

- Used the SSM session like a normal EC2 shell and switched to root with `sudo -i` when needed.
- Used `boto3` in FastAPI to retrieve the secret from Secrets Manager.
- Added only safe, non-secret values to the systemd override file.
- Kept real DB credentials inside Secrets Manager only.
- Checked the old environment file safely using redacted commands before removing any DB secrets.
- Restarted the backend service and tested the API endpoints again.

## Security Decision

- I did not use `AdministratorAccess`.
- I gave the EC2 role only `secretsmanager:GetSecretValue` for the exact RDS secret.
- I avoided exposing DB passwords in screenshots, GitHub, terminal output, or documentation.
- I kept `.env` only for non-sensitive config after the Secrets Manager setup worked.

## Key Takeaway

Secrets should not live inside application files or server config. A secure backend should use an IAM role to retrieve credentials from Secrets Manager, then connect to private RDS safely.
