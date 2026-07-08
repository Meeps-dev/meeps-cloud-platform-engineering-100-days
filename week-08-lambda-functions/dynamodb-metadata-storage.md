## Day 53: DynamoDB Metadata Storage

### What I Learned

- DynamoDB is a serverless NoSQL database that works well with Lambda.
- A DynamoDB table stores data as items.
- The partition key uniquely identifies each item in the table.
- I used `fileId` as the partition key for uploaded file metadata.
- Lambda environment variables help avoid hardcoding values like table name and project name.
- Lambda needs IAM permissions before it can write to or read from DynamoDB.
- `PutItem` is used to write new metadata into DynamoDB.
- `GetItem` is used to read a specific item from DynamoDB.
- CloudWatch Logs helps debug DynamoDB access and Lambda execution issues.

### What I Built

- Created a DynamoDB table named `meeps-week8-file-metadata`.
- Set `fileId` as the partition key with type `String`.
- Added environment variables to the `file-processor` Lambda:
  - `TABLE_NAME=meeps-week8-file-metadata`
  - `ENVIRONMENT=dev`
  - `PROJECT=meeps`
- Updated the Lambda function to write S3 file metadata into DynamoDB.
- Uploaded a new file to the S3 `uploads/` folder.
- Confirmed that the file metadata appeared in DynamoDB.
- Checked CloudWatch Logs to verify successful processing.

### What I Broke Intentionally

- Removed the `dynamodb:PutItem` permission from the Lambda IAM policy.
- Uploaded another file to S3 to trigger the Lambda function.
- Lambda was triggered, but it failed when trying to write to DynamoDB.

### How I Debugged It

- Checked CloudWatch Logs for the failed Lambda execution.
- Found an `AccessDeniedException` error.
- Confirmed that the Lambda execution role was missing `dynamodb:PutItem`.
- Verified that the issue was caused by IAM permissions, not the Lambda code.

### How I Fixed It

- Added `dynamodb:PutItem` back to the Lambda IAM policy.
- Kept the permission limited to the `meeps-week8-file-metadata` table.
- Re-uploaded a test file to S3.
- Confirmed that Lambda processed the file successfully.
- Verified that the metadata was written into DynamoDB again.

### Key Takeaway

Lambda needs exact IAM permissions to interact with DynamoDB. Removing `dynamodb:PutItem` caused an `AccessDeniedException`, and the correct fix was to restore only the required table-level permission without using `AdministratorAccess`.
