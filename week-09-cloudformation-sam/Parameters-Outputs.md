# Day 58: Parameters, Outputs, IAM Role, and Intrinsic Functions

## What I Learned

- Used `!Ref` to reference parameters and resource names.
- Used `!GetAtt` to retrieve resource ARNs.
- Used `!Sub` and `!Join` to build dynamic names and strings.
- Created a Lambda execution role through CloudFormation.
- Applied least-privilege IAM permissions instead of `AdministratorAccess`.
- Updated an existing CloudFormation stack safely.

## What I Built

- Created `iam-lambda-role.yaml`.
- Provisioned:
  - Lambda execution IAM role
  - CloudWatch Logs permissions
  - S3 object read permission
  - DynamoDB `GetItem` and `PutItem` permissions
  - DynamoDB table and CloudWatch log group
- Added outputs for resource names and ARNs.

## What I Broke

- Tested an incorrect or missing IAM permission.
- Encountered stack update issues when IAM acknowledgement or template configuration was incorrect.
- Confirmed that overly restricted permissions can cause `AccessDenied` errors.

## How I Fixed It

- Checked CloudFormation stack events for the failed resource.
- Added the required IAM capability acknowledgement.
- Corrected the IAM actions and resource ARNs.
- Redeployed the template and confirmed the stack reached `UPDATE_COMPLETE`.

## Key Takeaway

- IAM roles should grant only the exact actions required on specific AWS resources.
- CloudFormation intrinsic functions make templates reusable and prevent hardcoded resource values.
