# Day 64 — Terraform Foundations and Provider Configuration

## What I Learned

- Terraform manages infrastructure through declarative Infrastructure as Code.
- HCL describes the desired infrastructure state.
- Providers connect Terraform to platforms such as AWS.
- Resources define infrastructure Terraform should create and manage.
- Terraform state maps configuration to real infrastructure.
- `.terraform.lock.hcl` keeps provider versions consistent.

## Practical Work

- Installed Terraform `1.15.8` on macOS.
- Confirmed my AWS identity and region.
- Configured AWS Provider `~> 6.55`.
- Added variables and default AWS tags.
- Created and verified an S3 test bucket.
- Practised `init`, `fmt`, `validate`, `plan`, `show`, `apply`, `state list`, and `output`.
- Confirmed idempotency with a no-change plan.
- Generated and reviewed a destroy plan.

## What Broke and How I Fixed It

- `terraform` was initially unavailable, so I installed it with Homebrew.
- Git returned `pathspec` errors because I ran root-relative commands from the `dev` directory.
- I fixed this by returning to the repository root:

  `cd "$(git rev-parse --show-toplevel)"`

- Terraform state and generated files appeared locally, so I confirmed they were excluded using `.gitignore`.
- I committed `.terraform.lock.hcl` but kept state, plan files, credentials, and `.terraform/` out of Git.

## Result

- Terraform initialized and validated successfully.
- AWS infrastructure was created and verified.
- Local state was inspected safely without manual editing.
- The project was committed without exposing generated or sensitive files.
