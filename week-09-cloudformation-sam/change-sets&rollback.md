# Day 62: Change Sets, Stack Updates, and Rollback Testing

## What I Learned

- Created and reviewed CloudFormation change sets before updating infrastructure.
- Used `describe-change-set` to inspect planned resource changes.
- Learned how CloudFormation handles failed updates and automatic rollback.
- Used stack events and `StatusReason` to identify deployment failures.
- Added DynamoDB TTL, a Lambda environment variable, a new API route, tags, and outputs.

## What I Built

- Added a `/deployment` API endpoint.
- Added DynamoDB TTL using the `expiresAt` attribute.
- Added a deployment-version environment variable.
- Created, reviewed, and executed CloudFormation change sets.

## What I Broke

- Created an intentionally failing stack update to test rollback.
- Generated stale or missing SAM packaged templates.
- Used an incorrect `CodeUri` path, causing Lambda code to be skipped during build.
- Misconfigured YAML indentation in the `Outputs` section.
- Deployed old Lambda code, causing `/deployment` to return `Route not found`.

## Challenges Faced

- Change sets repeatedly returned `FAILED`.
- CloudFormation reported that `null` values were not allowed in the template.
- The SAM package command could not find the Lambda artifact.
- Some packaged files were deleted manually and had to be regenerated.
- Debugging required checking source files, built files, packaged templates, and stack events separately.

## How I Fixed It

- Corrected `CodeUri` to point to the actual Lambda source directory.
- Fixed the YAML indentation and ensured every output had a valid `Value`.
- Deleted stale `.aws-sam` build artifacts and rebuilt without cache.
- Regenerated the packaged SAM template from the latest source.
- Added a unique deployment-version parameter to force a valid stack change.
- Checked `StatusReason` before trying to execute failed change sets.
- Confirmed the stack returned to `UPDATE_COMPLETE`.

## Key Takeaway

- A safe CloudFormation workflow is:

  `Edit → Validate → Build → Verify → Package → Review Change Set → Execute → Monitor Events`
