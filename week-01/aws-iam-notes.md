# Day 4: AWS Account and IAM Setup

## What I Learned

Today, I learned how to set up an AWS account safely and how IAM controls access inside AWS.

## Topics Covered

- Root account
- IAM user
- IAM group
- IAM role
- IAM policy
- Access key
- Secret key
- MFA
- Least privilege
- AWS CLI setup

## What I Practiced

- Created an AWS account
- Enabled MFA on the root account
- Created an IAM admin user
- Stopped using the root account for daily work
- Installed AWS CLI on my Mac
- Configured AWS CLI locally
- Verified my AWS identity from the terminal

## CLI Commands Used

````bash
aws --version
aws configure
aws sts get-caller-identity
ls ~/.aws
cat ~/.aws/config
cat ~/.aws/credentials
## Key Takeaways

- The root account has full control and should only be used for important account-level tasks.
- MFA adds extra protection to the AWS account.
- IAM users should be used for daily AWS work.
- IAM policies define what a user or role can access.
- Access keys and secret keys are used for CLI access and must be kept private.
- Least privilege means giving only the permissions needed.
- AWS security should be set up properly before deploying any application.

## Why This Matters

A cloud engineer must understand access control before creating infrastructure.
Bad IAM setup can expose servers, databases, billing, and sensitive company data.

## Final Result

AWS CLI was installed and configured successfully, and the account identity was verified using:

```bash
aws sts get-caller-identity
````
