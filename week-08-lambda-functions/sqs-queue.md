## Day 55C: SQS Queue, Retry Behavior, and DLQ

### What I Learned

- SQS is used to queue messages for background processing.
- Lambda can be triggered automatically by messages in an SQS queue.
- SQS helps decouple file upload from file processing.
- If Lambda fails, the message can be retried.
- Visibility timeout controls how long a message is hidden while being processed.
- A dead-letter queue stores messages that fail too many times.
- Maximum receive count controls how many retries happen before the message goes to the DLQ.
- CloudWatch Logs is important for debugging failed Lambda executions.

### What I Built

- Created a main SQS processing queue.
- Created a dead-letter queue.
- Connected the DLQ to the main queue.
- Configured maximum receive count.
- Added SQS as a trigger for the processing Lambda.
- Tested successful message processing.
- Tested failed message retry behavior.

### What I Broke

- Sent a bad/failing message to the queue.
- Lambda failed while processing the message.
- SQS retried the message.
- After the maximum receive count, the message moved to the DLQ.

### How I Debugged It

- Checked CloudWatch Logs for the Lambda failure.
- Checked the SQS queue for retry behavior.
- Checked the DLQ to confirm the failed message was moved there.
- Reviewed timeout, visibility timeout, and Lambda error logs.

### How I Fixed It

- Fixed the Lambda error or bad message handling.
- Confirmed the correct IAM permissions were attached.
- Re-tested with a valid message.
- Confirmed the message processed successfully and did not move to the DLQ.

### Key Takeaway

SQS makes serverless processing more reliable by adding buffering, retries, and dead-letter queue handling.
