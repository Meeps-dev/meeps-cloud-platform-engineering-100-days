# Day 59: Deploy Lambda Using AWS SAM

## What I Learned

- AWS SAM simplifies serverless deployments built on CloudFormation.
- Used `AWS::Serverless::Function` to define a Lambda function.
- Configured the Lambda handler, runtime, memory, timeout, IAM role, and environment variables.
- Used `sam validate`, `sam build`, and `sam deploy --guided`.
- Learned that the local Python version must match the Lambda runtime in the SAM template.

## What I Built

- Created a file processor Lambda application.
- Added a SAM `template.yaml`.
- Configured the function to:
  - Receive an event
  - Log the event to CloudWatch
  - Return a clean JSON response
- Reused the IAM role, S3 bucket, DynamoDB table, and log group created earlier.

## Challenges / What Broke

- `sam validate` initially failed because the SAM CLI was not installed.
- `sam build` failed because Python 3.13 was not available in my system PATH.
- `sam build --use-container` failed because Docker or Finch was not installed and running.

## How I Fixed It

- Installed the AWS SAM CLI and confirmed it using `sam --version`.
- Installed Python 3.13 to match the runtime in `template.yaml`.
- Updated the terminal PATH so SAM could detect Python 3.13.
- Removed the failed `.aws-sam` build directory and rebuilt the project.
- Used local Python instead of the container build method.

## Key Takeaway

- SAM requires its CLI and the matching runtime to be installed locally unless a container runtime is used.
- Validation and build errors should be resolved before deploying the application to AWS.
