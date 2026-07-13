# Day 61: S3 Trigger and Event-Driven Workflow

## What I Learned

- Added an S3 `ObjectCreated` trigger through AWS SAM.
- SAM created the required permission for S3 to invoke Lambda.
- Lambda extracted the bucket name, object key, size, and event details.
- Stored uploaded-file metadata in DynamoDB.
- Used CloudWatch Logs to trace the full event flow.
- Restricted `s3:GetObject` access to the `uploads/` prefix only.

## What I Built

- Created the workflow:

  `S3 Upload → Lambda → DynamoDB → CloudWatch Logs`

- Configured the trigger, IAM permissions, bucket, Lambda, and DynamoDB through Infrastructure as Code.

## Challenges

- The stack update failed because the generated S3 bucket name was invalid.
- Using `!Sub >` introduced formatting or whitespace into values used for the bucket name.
- CloudFormation rolled the update back to `UPDATE_ROLLBACK_COMPLETE`.
- The failed bucket resource also produced deletion errors during rollback.

## How I Fixed It

- Replaced folded `!Sub >` values with quoted single-line `!Sub` strings.
- Corrected the bucket name, S3 ARN, environment variable, and API URL values.
- Added parameter validation for lowercase letters, numbers, and hyphens.
- Checked CloudFormation stack events to identify the failed resource.
- Ran `sam validate`, rebuilt without cache, and redeployed the corrected stack.
- Confirmed the stack reached `UPDATE_COMPLETE` and tested the S3 upload flow.

## Key Takeaway

- Resource names and ARNs should use clean single-line values.
- CloudFormation stack events and rollback status are essential for debugging failed IaC deployments.
