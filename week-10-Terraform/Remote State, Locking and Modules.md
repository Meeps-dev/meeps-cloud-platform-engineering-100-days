# Day 66 — Remote State, Locking and Modules

## What I Learned

- Local state is unsafe for teamwork because it cannot be shared or locked reliably.
- An S3 backend provides centralized, durable Terraform state.
- use_lockfile = true enables native S3 state locking.
- Backend infrastructure must be created separately before state can be migrated.
- terraform init -migrate-state moves existing local state to S3.
- Root modules configure backends and providers; child modules contain reusable infrastructure code.
- S3 versioning helps recover previous state versions.

## What I Built

- Created a separate bootstrap configuration for the state bucket.
- Enabled S3 versioning, AES256 encryption and full public-access blocking.
- Migrated the development state to:
- week-10/dev/terraform.tfstate
- Created module skeletons for VPC, security, ALB, compute, RDS and application S3.
- Confirmed child modules contain no backend or provider configurations.
- What Broke and How I Fixed It
- An incomplete quoted cd command opened the dquote> prompt.
- Cancelled it with Ctrl+C and reran the complete command.
- The initial backup check did not pass because a backup was missing or empty.
- Recreated both backups separately, secured them with chmod 600 and verified them.
- A second Terraform operation failed with a state-lock error.
- This was expected; I stopped the first operation and confirmed the lock was released safely.

## Final Result

- Remote state is encrypted, versioned and privately stored in S3.
- Simultaneous state modifications are blocked.
- No state, plan or secret variable files are tracked by Git.
- Terraform validation passed and the final plan showed no changes.
