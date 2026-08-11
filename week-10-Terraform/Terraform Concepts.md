# Day 65: Variables, Outputs, Data Sources and Import

## What I Learned

- Typed variables and validation prevent invalid configuration values.
- Variable precedence determines which value Terraform uses; CLI `-var` has the highest priority.
- Locals reduce repetition and create reusable names and tags.
- Data sources read existing AWS information without creating resources.
- Outputs expose useful information after planning or applying.
- `sensitive = true` hides values in normal CLI output but not in Terraform state.
- `terraform import` connects an existing AWS resource to Terraform state.
- `state list`, `state show` and `state rm` inspect or manage state entries.

## What Broke and How I Fixed It

- The Day 64 bucket returned `404` because it had already been deleted; I confirmed this was expected.
- Terraform initially planned to create the existing import bucket because it was not in state; I fixed this with `terraform import`.
- `terraform state rm` removed the bucket from state but not AWS; I verified it still existed and deleted it safely with the AWS CLI.
- `rg` was unavailable during the secret check; I used macOS `grep` instead.
- A CLI `staging` override changed the planned outputs; running the normal plan again restored the expected `dev` values.
- I kept `terraform.tfvars`, state and saved plans ignored because they may contain sensitive information.

## Final Result

- Added validated variables, locals, AWS data sources and protected outputs.
- Successfully practised variable precedence and resource import.
- Final validation succeeded and the plan showed `No changes`.
- No permanent AWS resources were created.
- Day 65 changes were safely committed, reviewed and merged into `main`.
