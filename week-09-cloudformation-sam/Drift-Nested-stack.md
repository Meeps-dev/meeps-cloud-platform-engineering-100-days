# Day 63: Drift Detection and Nested Stack Introduction

## What I Learned

- Drift occurs when an AWS resource no longer matches its CloudFormation template.
- Manual console changes can make Infrastructure as Code unreliable.
- CloudFormation drift detection compares deployed resources with the expected template configuration.
- Nested stacks divide large templates into smaller, reusable components.
- Parent stacks pass parameters to child stacks and read child stack outputs.

## What I Built

- Ran drift detection against the existing SAM stack.
- Created a simple nested-stack structure:

  `Root Stack → Storage Nested Stack → S3 Bucket`

- Passed project and environment parameters from the root stack.
- Returned the bucket name and ARN through nested stack outputs.

## What I Broke

- Manually changed an S3 bucket tag in the AWS Console.
- This caused the deployed bucket to differ from the CloudFormation template.
- CloudFormation reported the stack as `DRIFTED` and the bucket as `MODIFIED`.

## Challenges Faced

- Choosing a resource property that CloudFormation could detect as drift.
- Packaging the local child template before deploying the root stack.
- Understanding that nested stacks should be managed through the parent stack.

## How I Fixed It

- Reviewed the expected and actual S3 tag values in the drift results.
- Restored the manual tag to the value defined in the template.
- Ran drift detection again and confirmed the stack returned to `IN_SYNC`.
- Packaged the child template to S3 and deployed it through the root stack.

## Key Takeaway

- AWS resources managed by CloudFormation should not be changed manually.
- Nested stacks make larger infrastructure easier to organize, reuse, and maintain.
