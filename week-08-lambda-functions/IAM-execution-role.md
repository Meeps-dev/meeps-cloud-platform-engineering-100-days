## Day 51: IAM Execution Role and Least Privilege

### What I Learned

- A Lambda execution role is an IAM role that gives Lambda permission to access AWS services.
- Lambda does not use my personal IAM user permissions when it runs.
- The trust policy defines who can assume the role.
- For Lambda, the trusted service is `lambda.amazonaws.com`.
- The permission policy defines what the Lambda function is allowed to do.
- For CloudWatch logging, Lambda needs:
  - `logs:CreateLogGroup`
  - `logs:CreateLogStream`
  - `logs:PutLogEvents`
- Least privilege means giving Lambda only the permissions it needs.
- `AdministratorAccess` should not be used because it gives Lambda too much power.
- AWS managed policies are prebuilt by AWS, while custom policies allow tighter control.

### What I Built

- Created a new IAM role named `lambda-execution-role`.
- Added a custom CloudWatch Logs policy to the role.
- Attached the role to my Lambda function.
- Tested the Lambda function successfully.
- Confirmed that Lambda logs were written to CloudWatch Logs.

### What I Broke Intentionally

- Removed the `logs:PutLogEvents` permission from the Lambda role policy.
- Re-ran the Lambda function after removing the permission.
- The Lambda function could still run, but CloudWatch Logs did not receive the new log output correctly.

### How I Debugged It

- Checked the Lambda test result.
- Opened CloudWatch Logs to confirm whether new logs were created.
- Reviewed the IAM policy attached to the Lambda execution role.
- Identified that the missing `logs:PutLogEvents` permission caused the logging issue.

### How I Fixed It

- Added `logs:PutLogEvents` back to the custom IAM policy.
- Saved the updated policy.
- Re-ran the Lambda function.
- Confirmed that new logs appeared again in CloudWatch Logs.
- Fixed the issue without using `AdministratorAccess`.

### Key Takeaway

Lambda needs the correct execution role to work properly. Using least privilege makes the setup more secure, while CloudWatch Logs permissions are essential for debugging Lambda functions.
