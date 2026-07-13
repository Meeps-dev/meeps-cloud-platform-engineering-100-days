# Day 60: API Gateway and DynamoDB with SAM

## What I Learned

- Used `AWS::Serverless::Api` to create API Gateway with SAM.
- Connected API Gateway routes to a Lambda function.
- Created a DynamoDB table through the SAM template.
- Passed the DynamoDB table name to Lambda using environment variables.
- Applied least-privilege IAM permissions for `GetItem` and `PutItem`.
- Tested:
  - `GET /health`
  - `POST /metadata`
  - `GET /metadata?id=<id>`

## What I Built

- Built the flow:

  `Client/Postman → API Gateway → Lambda → DynamoDB`

- Created API Gateway, Lambda, DynamoDB, IAM permissions, and outputs from one SAM template.

## What Broke / Challenges

- Old Day 59 parameters in `samconfig.toml` conflicted with the updated template.
- The deployment required permission to create a new IAM role.
- Incorrect or missing DynamoDB permissions caused `AccessDeniedException`.
- API errors required checking Lambda logs in CloudWatch.

## How I Fixed It

- Removed the outdated SAM configuration and ran `sam deploy --guided` again.
- Allowed SAM to create IAM resources using `CAPABILITY_IAM`.
- Added only `dynamodb:GetItem` and `dynamodb:PutItem` for the specific table.
- Checked CloudFormation stack events and CloudWatch logs to identify deployment and runtime errors.
- Rebuilt and redeployed the SAM application successfully.

## Key Takeaway

- SAM can define the API, Lambda, database, permissions, and configuration in one repeatable Infrastructure as Code template.
- CloudWatch logs and CloudFormation events are essential for debugging serverless applications.
