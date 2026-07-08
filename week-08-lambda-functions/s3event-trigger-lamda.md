## Day 52: S3 Event Trigger to Lambda

### What I Learned

- S3 event notifications can automatically trigger Lambda when an action happens in a bucket.
- `ObjectCreated` events are triggered when a new file is uploaded to S3.
- Lambda triggers allow AWS services like S3 to invoke a Lambda function automatically.
- The S3 event payload contains useful metadata such as bucket name, object key, object size, upload time, and event name.
- Prefix filtering helps control which files trigger Lambda.
- Using the `uploads/` prefix means only files uploaded inside that folder should invoke the function.
- This is an example of event-driven architecture because Lambda runs only when an upload event happens.

### What I Built

- Created an S3 bucket for file uploads.
- Created an `uploads/` prefix inside the bucket.
- Created a Python Lambda function named `file-processor`.
- Added S3 as a trigger for the Lambda function.
- Configured the trigger to run on `ObjectCreated` events.
- Used the `uploads/` prefix filter so only files in that path trigger Lambda.
- Uploaded a test file into `uploads/`.
- Confirmed that Lambda was triggered automatically.
- Checked CloudWatch Logs to inspect the S3 event payload.

### What I Broke Intentionally

- Uploaded a test file outside the `uploads/` prefix.
- The Lambda function did not trigger because the object did not match the configured prefix filter.

### How I Debugged It

- Checked the S3 object location.
- Confirmed that the Lambda trigger was configured with the `uploads/` prefix.
- Checked CloudWatch Logs to see whether a new invocation happened.
- Compared the file uploaded at the bucket root with the file uploaded inside `uploads/`.

### How I Fixed It

- Uploaded the file into the correct `uploads/` folder.
- Re-tested the upload event.
- Lambda triggered successfully.
- CloudWatch Logs showed the bucket name, object key, object size, upload time, and event name.

### Key Takeaway

S3 can trigger Lambda automatically when files are uploaded. Prefix filtering is important because it controls which uploads trigger the function, and CloudWatch Logs helps confirm and debug the event payload.
