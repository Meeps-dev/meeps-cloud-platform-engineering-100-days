````md
# Week 8: Serverless File Processing & Notification Workflow

## Project Overview

This project is a production-style serverless workflow built with AWS Lambda, API Gateway, S3, DynamoDB, EventBridge, SQS, SNS, IAM, and CloudWatch Logs.

The goal was to understand how event-driven cloud systems work without managing EC2 servers. The workflow accepts file upload requests through an API, stores the uploaded file in S3, tracks metadata in DynamoDB, queues the processing job through SQS, processes the file with Lambda, and sends notifications through SNS.

---

## Architecture Diagram

![Week 8 Serverless Workflow](./docs/architecture/week8-serverless-file-processing.png)

---

## Architecture Flow

```text
User / Client App
    ↓
API Gateway HTTP API
    ↓
Ingest Lambda
    ↓
Amazon S3 + DynamoDB
    ↓
S3 ObjectCreated Event
    ↓
Amazon EventBridge
    ↓
Amazon SQS
    ↓
Processing Lambda
    ↓
DynamoDB Update + Processed S3 Output
    ↓
Amazon SNS Notification
    ↓
Email / Subscriber Endpoint
```
````

---

## Services Used

- AWS Lambda
- Amazon API Gateway HTTP API
- Amazon S3
- Amazon DynamoDB
- Amazon EventBridge
- Amazon SQS
- Amazon SNS
- AWS IAM
- Amazon CloudWatch Logs
- Lambda Environment Variables

---

## Project Goal

The main goal of this project was to build a serverless file-processing and notification workflow using event-driven AWS services.

This helped me understand:

- How Lambda functions work without managing servers.
- How API Gateway invokes Lambda through HTTP routes.
- How S3 events can trigger downstream processing.
- How EventBridge routes events between AWS services.
- How SQS decouples upload and processing workloads.
- How DLQs capture failed messages.
- How SNS handles notification fan-out.
- How DynamoDB stores file metadata.
- How IAM roles enforce least privilege.
- How CloudWatch Logs helps debug Lambda and event-driven systems.

---

## Resources Created

| Resource Type        | Resource Name                     |
| -------------------- | --------------------------------- |
| S3 Bucket            | `file-upload-<unique-suffix>`     |
| DynamoDB Table       | `meeps-week8-file-metadata`       |
| API Gateway          | `meeps-week8-production-api`      |
| Lambda Function      | `ingest-lambda`                   |
| Lambda Function      | `processing-lambda`               |
| Lambda Function      | `scheduled-summary-lambda`        |
| SQS Queue            | `meeps-week8-processing-queue`    |
| SQS DLQ              | `meeps-week8-processing-dlq`      |
| SNS Topic            | `meeps-week8-file-notifications`  |
| EventBridge Rule     | `meeps-week8-s3-created-to-sqs`   |
| EventBridge Schedule | `meeps-week8-summary-every-5-min` |

---

## Implementation Summary

### 1. API Gateway HTTP API

I created an HTTP API to expose the workflow to users and client applications.

Routes created:

```text
GET  /health
POST /files
GET  /files
GET  /files/{fileId+}
```

The API Gateway routes invoke the `ingest-lambda` function.

---

### 2. Ingest Lambda

The `ingest-lambda` function handles API requests.

It performs the following actions:

- Accepts file upload requests from API Gateway.
- Uploads the file to the S3 `uploads/` prefix.
- Creates an initial metadata record in DynamoDB.
- Returns a job ID and file ID to the client.
- Logs request and processing details to CloudWatch Logs.

Example response:

```json
{
  "message": "File accepted for processing",
  "jobId": "generated-job-id",
  "fileId": "uploads/file-name.txt",
  "status": "uploaded"
}
```

---

### 3. Amazon S3

S3 was used as the private file storage layer.

Folders created:

```text
uploads/
processed/
```

- `uploads/` stores incoming files.
- `processed/` stores processed output or summary files.

S3 was kept private with public access blocked.

---

### 4. DynamoDB Metadata Table

I created a DynamoDB table to store file metadata.

Table name:

```text
meeps-week8-file-metadata
```

Partition key:

```text
fileId
```

Example item:

```json
{
  "fileId": "uploads/sample.txt",
  "bucket": "file-upload-example",
  "key": "uploads/sample.txt",
  "size": 2048,
  "status": "processed",
  "processedAt": "2026-xx-xxTxx:xx:xxZ"
}
```

---

### 5. EventBridge S3 ObjectCreated Rule

I enabled S3 events to EventBridge.

The EventBridge rule listens for new objects created under:

```text
uploads/
```

When a file is uploaded, EventBridge sends the event to the SQS processing queue.

---

### 6. Amazon SQS Processing Queue

I created an SQS queue to decouple file upload from file processing.

Main queue:

```text
meeps-week8-processing-queue
```

Dead-letter queue:

```text
meeps-week8-processing-dlq
```

Maximum receive count:

```text
3
```

This means failed messages are retried and then moved to the DLQ after repeated failure.

---

### 7. Processing Lambda

The `processing-lambda` function is triggered by SQS.

It performs the following actions:

- Reads the SQS message.
- Extracts the S3 object details.
- Reads the uploaded file from S3.
- Processes the file.
- Writes processed output to the `processed/` S3 prefix.
- Updates the DynamoDB item status to `processed`.
- Publishes a notification to SNS.
- Logs all steps to CloudWatch Logs.

---

### 8. SNS Notification

I created an SNS topic for notifications.

Topic name:

```text
meeps-week8-file-notifications
```

The `processing-lambda` publishes a message after successful file processing.

Notification flow:

```text
Processing Lambda → SNS Topic → Email Subscriber
```

---

### 9. EventBridge Scheduled Lambda

I created a scheduled Lambda to run automatically using EventBridge.

Schedule:

```text
rate(5 minutes)
```

The scheduled Lambda scans DynamoDB and logs a summary of file processing status.

This demonstrated how to run background jobs without EC2 cron servers.

---

## Environment Variables

### Ingest Lambda

```text
TABLE_NAME=meeps-week8-file-metadata
BUCKET_NAME=file-upload-<unique-suffix>
QUEUE_URL=meeps-week8-processing-queue-url
TOPIC_ARN=meeps-week8-file-notifications-topic-arn
PROJECT=meeps
ENVIRONMENT=dev
```

### Processing Lambda

```text
TABLE_NAME=meeps-week8-file-metadata
BUCKET_NAME=file-upload-<unique-suffix>
QUEUE_URL=meeps-week8-processing-queue-url
TOPIC_ARN=meeps-week8-file-notifications-topic-arn
PROJECT=meeps
ENVIRONMENT=dev
```

---

## IAM and Security Decisions

- Used IAM roles instead of access keys.
- Each Lambda function had its own execution role.
- Lambda permissions followed least privilege.
- S3 bucket was private.
- Public access was blocked on the bucket.
- DynamoDB access was limited to the required table.
- SNS publish permission was limited to the required topic.
- SQS permissions were limited to the required queue.
- `AdministratorAccess` was not used for Lambda functions.

---

## IAM Permissions Used

### Ingest Lambda

Required permissions:

```text
s3:PutObject
dynamodb:PutItem
dynamodb:GetItem
dynamodb:Scan
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

### Processing Lambda

Required permissions:

```text
s3:GetObject
s3:PutObject
dynamodb:GetItem
dynamodb:UpdateItem
sns:Publish
sqs:ReceiveMessage
sqs:DeleteMessage
sqs:GetQueueAttributes
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

### Scheduled Summary Lambda

Required permissions:

```text
dynamodb:Scan
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "service": "meeps-week8-api",
  "week": 8
}
```

---

### Upload File

```http
POST /files
```

Example request:

```json
{
  "fileName": "week8-test.txt",
  "content": "Hello from Meeps Week 8 production workflow",
  "contentType": "text/plain"
}
```

Expected response:

```json
{
  "message": "File accepted for processing",
  "jobId": "generated-job-id",
  "fileId": "uploads/generated-file-name.txt",
  "status": "uploaded"
}
```

---

### List Files

```http
GET /files
```

Returns metadata records from DynamoDB.

---

### Get File Metadata

```http
GET /files/{fileId+}
```

Example:

```http
GET /files/uploads/sample.txt
```

Returns metadata for one uploaded file.

---

## Testing

### Test `/health`

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/health
```

### Test file upload

```bash
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/files \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "week8-test.txt",
    "content": "Hello from Meeps Week 8 production workflow",
    "contentType": "text/plain"
  }'
```

### Test list files

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/files
```

---

## What I Broke Intentionally and Fixed

### Day 50: Lambda Timeout

#### What I Broke

- Reduced the Lambda timeout too low.
- Ran a function that took longer than the configured timeout.

#### What Happened

- The Lambda function failed with a timeout error.

#### How I Fixed It

- Increased the timeout value.
- Re-tested the function successfully.
- Confirmed the successful execution in CloudWatch Logs.

---

### Day 51: CloudWatch Logs Permission

#### What I Broke

- Removed `logs:PutLogEvents` from the Lambda execution role.

#### What Happened

- Lambda could run, but new logs were not written correctly to CloudWatch Logs.

#### How I Fixed It

- Added `logs:PutLogEvents` back to the IAM policy.
- Re-ran the function.
- Confirmed logs appeared again in CloudWatch.

---

### Day 52: S3 Prefix Filtering

#### What I Broke

- Uploaded a file outside the configured `uploads/` prefix.

#### What Happened

- Lambda did not trigger because the file did not match the S3/EventBridge prefix rule.

#### How I Fixed It

- Uploaded the file into the correct `uploads/` prefix.
- Confirmed the event triggered the workflow correctly.

---

### Day 53: DynamoDB AccessDenied

#### What I Broke

- Removed `dynamodb:PutItem` from the Lambda execution role.

#### What Happened

- Lambda triggered successfully but failed when writing metadata to DynamoDB.
- CloudWatch Logs showed an `AccessDeniedException`.

#### How I Fixed It

- Added `dynamodb:PutItem` back to the IAM policy.
- Scoped the permission only to the required DynamoDB table.
- Re-tested the workflow and confirmed metadata was stored.

---

### Day 54: API Gateway Route Testing

#### What I Broke

- Tested incorrect or incomplete API routes.
- Also tested file IDs that included nested paths like `uploads/sample.txt`.

#### What Happened

- Some requests did not match the expected API Gateway route.

#### How I Fixed It

- Reviewed API Gateway route configuration.
- Used a greedy route pattern:

```text
GET /files/{fileId+}
```

- Re-tested the endpoint and confirmed DynamoDB metadata was returned.

---

### Day 55A: EventBridge Target Configuration

#### What I Broke

- Tested EventBridge schedule/rule target configuration issues.

#### What Happened

- Lambda did not run as expected until the rule and target were configured correctly.

#### How I Fixed It

- Checked the EventBridge rule status.
- Confirmed the Lambda/SQS target was attached.
- Re-tested and verified execution using CloudWatch Logs.

---

### Day 55B: SNS Publish Permission

#### What I Broke

- Removed or misconfigured `sns:Publish` permission.

#### What Happened

- The processing Lambda failed when trying to publish to SNS.
- CloudWatch Logs showed an SNS permission issue.

#### How I Fixed It

- Added `sns:Publish` back to the Lambda IAM policy.
- Scoped it only to the required SNS topic ARN.
- Re-ran the workflow and confirmed email notification was sent.

---

### Day 55C: SQS Retry and DLQ

#### What I Broke

- Sent a failing message/file to force the processing Lambda to fail.
- Also tested timeout behavior with a slow file-processing case.

#### What Happened

- SQS retried the message.
- After the maximum receive count was reached, the message moved to the DLQ.

#### How I Fixed It

- Reviewed CloudWatch Logs.
- Checked the SQS retry behavior.
- Confirmed the failed message appeared in the DLQ.
- Fixed the Lambda error/permission issue.
- Re-tested with a valid file and confirmed successful processing.

---

## Debugging Tools Used

- Lambda test console
- API Gateway route testing
- CloudWatch Logs
- DynamoDB table item explorer
- S3 object view
- SQS queue metrics
- DLQ message polling
- EventBridge rule monitoring
- SNS subscription confirmation
- IAM policy review

---

## CloudWatch Logs Checked

Log groups used:

```text
/aws/lambda/ingest-lambda
/aws/lambda/processing-lambda
/aws/lambda/scheduled-summary-lambda
```

CloudWatch helped confirm:

- Lambda invocation
- API request payloads
- S3 object metadata
- DynamoDB writes and updates
- SNS publish success/failure
- SQS retry failures
- Timeout errors
- IAM `AccessDeniedException` errors

---

## Final Workflow Validation

The project was considered successful after confirming:

- API Gateway invoked `ingest-lambda`.
- Uploaded files were stored in S3 under `uploads/`.
- Initial metadata was created in DynamoDB.
- S3 ObjectCreated events were sent to EventBridge.
- EventBridge routed matching events to SQS.
- SQS triggered `processing-lambda`.
- Processing Lambda read the file from S3.
- Processed output was written to `processed/`.
- DynamoDB metadata was updated to `processed`.
- SNS sent a notification to the confirmed email subscriber.
- Failed messages retried and moved to the DLQ.
- CloudWatch Logs showed successful and failed executions.

---

## Lambda vs EC2: What I Learned

### Lambda Is Better For

- Event-driven workloads
- File processing
- Scheduled tasks
- Lightweight APIs
- Background jobs
- Queue-based processing
- Workloads with unpredictable traffic
- Serverless systems where I do not want to manage servers

### EC2 Is Better For

- Long-running applications
- Apps that need full operating system control
- Persistent background processes
- Heavy compute workloads
- Workloads that exceed Lambda timeout limits
- Applications requiring custom server-level configuration

---

## Cost and Cleanup Notes

To avoid unnecessary AWS charges:

- Disabled the EventBridge schedule after testing.
- Deleted test files from S3 if no longer needed.
- Deleted unused SQS messages and DLQ test messages.
- Confirmed no unnecessary Lambda loops were running.
- Kept the S3 bucket private.
- Reviewed resources created for Week 8.
- Used AWS Budget alerts from the previous security week.
- Avoided NAT Gateway, EC2, ALB, RDS, and EKS for this serverless project.

---

## Screenshots to Include

- Architecture diagram
- API Gateway routes
- API Gateway invoke URL test
- `ingest-lambda` configuration
- `processing-lambda` configuration
- Lambda environment variables
- IAM least-privilege policy
- S3 bucket with `uploads/` and `processed/`
- DynamoDB table item
- EventBridge rule
- EventBridge schedule
- SQS main queue
- SQS DLQ
- SNS topic and confirmed subscription
- CloudWatch successful logs
- CloudWatch `AccessDeniedException`
- DLQ message after failed retries
- Final successful workflow test

---

## Production Improvements

If this were moved closer to a real production system, I would add:

- Authentication and authorization on API Gateway.
- Request validation for file uploads.
- API throttling and usage limits.
- CloudWatch alarms for Lambda errors.
- CloudWatch alarms for DLQ messages.
- Structured JSON logging.
- AWS X-Ray tracing.
- S3 lifecycle rules.
- DynamoDB backup/PITR.
- Infrastructure as Code using CloudFormation/SAM or Terraform.
- CI/CD deployment with GitHub Actions.
- Secrets Manager or SSM Parameter Store for sensitive configuration.
- Idempotency handling for duplicate S3/SQS events.

---

## Key Takeaway

This project showed how to build a production-style serverless workflow using AWS managed services. API Gateway handled entry, Lambda handled compute, S3 stored files, DynamoDB stored metadata, EventBridge routed events, SQS added buffering and retries, SNS handled notifications, IAM secured access, and CloudWatch provided observability.

The biggest lesson was that serverless systems are powerful, but production reliability depends on correct IAM permissions, logging, retries, DLQs, event filtering, timeout settings, and clear debugging practices.

```

```
