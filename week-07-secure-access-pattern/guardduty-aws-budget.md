# Day 48: GuardDuty and AWS Budgets

## What I Learned

- Learned that **GuardDuty** is used for AWS threat detection.
- Learned that GuardDuty helps detect suspicious activity, compromised credentials, and unusual AWS API behavior.
- Learned that **AWS Budgets** helps control cloud spending and prevent billing surprises.
- Learned that budget alerts can notify me when actual or forecasted cost reaches a set threshold.
- Learned that consistent resource tagging helps with organization, tracking, and cost visibility.
- This follows the Week 7 roadmap requirement to enable GuardDuty if acceptable and create a budget alert. :contentReference[oaicite:0]{index=0}

## What I Did

- Reviewed GuardDuty and checked how it works.
- Created an AWS Budget named `meeps-week7-budget`.
- Set the budget amount to `$5.00`.
- Added budget alerts:
  - Actual cost greater than `70%`
  - Forecasted cost greater than `100%`
- Checked that the budget health status was healthy.
- Applied Week 7 tags to resources where possible:
  - `project=meeps`
  - `week=week-7`
  - `owner=kehinde`
  - `environment=dev`

## What I Broke / Issue Faced

- I initially could not access GuardDuty properly on my current AWS free-tier/free-plan account.
- The account showed a setup/access limitation, so GuardDuty was restricted.
- This blocked me from completing GuardDuty directly on that account.

## How I Fixed It

- I proceeded carefully and tested GuardDuty on another AWS account where the service was accessible.
- I reviewed GuardDuty findings, settings, and monitoring behavior from that account.
- I continued the cost-control part by creating the AWS Budget successfully.
- I documented the account limitation instead of forcing an unsafe billing/account upgrade.

## Security Decision

- I did not ignore GuardDuty; I found a safe way to understand it using another AWS account.
- I avoided unnecessary account upgrades just to force service access.
- I kept cost control active by creating a low AWS budget.
- I used tags to make Week 7 resources easier to identify and manage.

## Cost Note

- Created `meeps-week7-budget` with a `$5.00` monthly budget.
- Added alerts for actual and forecasted cost.
- This helps prevent unexpected AWS billing while continuing the lab work.

## Key Takeaway

GuardDuty improves security visibility, while AWS Budgets protects against billing surprises. Even when a service is restricted on one account, the correct engineering decision is to document the limitation, find a safe test path, and continue with cost controls.
