# Day 57: CloudFormation Basics + First S3 Stack

## What I Learned

- CloudFormation is AWS Infrastructure as Code used to create and manage resources from templates.
- A CloudFormation stack is the deployed version of a template.
- YAML indentation is important because wrong spacing can break the template.
- The `Resources` section defines what AWS should create.
- The `Parameters` section makes templates reusable.
- The `Outputs` section shows useful values after deployment.
- Tags help organize resources by project, week, owner, and environment.

## What I Built

- Created my first CloudFormation template: `s3-stack.yaml`.
- Provisioned one S3 bucket using CloudFormation.
- Added bucket tags:
  - `project=meeps`
  - `week=week-9`
  - `environment=dev`
  - `owner=Meepor`
  - `managed-by=cloudformation`
- Added outputs for:
  - S3 bucket name
  - S3 bucket ARN

## What I Broke

- Had to watch out for YAML indentation issues.
- Learned that S3 bucket names must be globally unique if manually defined.
- Saw how small template mistakes can stop stack creation or updates.

## How I Fixed It

- Validated the template before deployment.
- Checked CloudFormation stack events to understand errors.
- Fixed the YAML structure and redeployed the stack.
- Confirmed the stack reached `CREATE_COMPLETE`.

## Key Takeaway

- CloudFormation makes AWS infrastructure repeatable, trackable, and easier to manage compared to manual console clicking.
- Day 57 gave me the foundation for building AWS resources through code before moving deeper into SAM and Terraform.
