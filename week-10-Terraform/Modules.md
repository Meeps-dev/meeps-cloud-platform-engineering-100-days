# Day 67 — VPC, Subnets, Routes and Security Modules

## What I Learned

- Child modules use variables as inputs and outputs to share resource information.
- Terraform modules are isolated and cannot directly access another module’s resources.
- Resource references automatically create dependency relationships.
- Security groups can securely pass traffic between ALB, application and database tiers.
- Saved plans and final `No changes` checks make infrastructure changes safer.
- Optional NAT Gateways help balance private-subnet connectivity and cost.

## What I Built

- A VPC with DNS support across two Availability Zones.
- Two public ALB, two private application and two private database subnets.
- Internet Gateway, isolated route tables and all subnet associations.
- Optional NAT Gateway controlled by a variable and disabled for cost control.
- ALB, application and RDS security-group modules with least-privilege rules.
- Reusable VPC and security module inputs and outputs.

## What Broke

- The root module passed arguments that the child module had not declared.
- Root variables used by the VPC module were initially missing.
- The VPC module referenced an Availability Zones data source declared only in the root module.
- Terraform commands were mistakenly run from child-module directories.
- Six AWS subnets and their route-table associations became missing while stale addresses remained in state.
- Git detected an extra blank line at the end of `variables.tf`.

## How I Fixed It

- Matched the root and child-module variable contracts.
- Declared the required Availability Zones data source inside the VPC module.
- Ran Terraform commands from the `envs/dev` root module.
- Verified the missing resources in both Terraform state and AWS before taking action.
- Backed up remote state and reviewed a saved recovery plan.
- Safely recreated six subnets and six associations without duplicating resources.
- Removed the extra blank line and reran formatting checks.
- Finished with successful validation and a final `No changes` plan.
