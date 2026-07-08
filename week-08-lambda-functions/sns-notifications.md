## Day 55B: SNS Notification Pattern

### What I Learned

- SNS is used for sending notifications to subscribers.
- SNS uses a publish/subscribe model.
- A Lambda function can publish a message to an SNS topic after processing work.
- Subscribers can include email, SMS, Lambda, SQS, or HTTP endpoints.
- SNS pushes messages out to subscribers, while SQS stores messages until they are processed.

### What I Built

- Created an SNS topic.
- Added an email subscription.
- Confirmed the email subscription.
- Allowed Lambda to publish messages to the SNS topic.
- Sent a notification after file processing completed.

### What I Broke

- Tested missing or incorrect SNS publish permission.
- Lambda failed when it tried to publish to SNS.

### How I Debugged It

- Checked CloudWatch Logs for the Lambda error.
- Found an SNS permission issue.
- Reviewed the Lambda execution role policy.
- Confirmed whether `sns:Publish` was allowed on the correct topic ARN.

### How I Fixed It

- Added `sns:Publish` back to the Lambda IAM policy.
- Limited the permission to the specific SNS topic ARN.
- Re-ran the workflow and confirmed the notification was sent.

### Key Takeaway

SNS is best for notification fan-out, but Lambda needs exact `sns:Publish` permission to send messages.
