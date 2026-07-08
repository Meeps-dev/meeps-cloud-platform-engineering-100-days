## Day 50: Lambda Basics and Manual Function Setup

### What I Learned

- AWS Lambda is a serverless compute service that runs code only when triggered by an event.
- A Lambda function does not require managing EC2 servers, operating systems, or manual scaling.
- The Lambda runtime defines the language environment. For this task, I used Python.
- The handler function is the entry point Lambda runs when the function is invoked.
- The event object contains the input data passed into the Lambda function.
- The response object is what the Lambda function returns after execution.
- Lambda memory can be increased or reduced depending on workload needs.
- Timeout controls how long a Lambda function can run before AWS stops it.
- Lambda needs an IAM execution role to write logs and access other AWS services.
- CloudWatch Logs helps track Lambda execution, errors, duration, memory usage, and debugging details.

### What I Built

- Created my first Lambda function manually.
- Used a Python handler that returned:

{
"message": "Meeps Week 8 Lambda is working"
}

- Tested the function using the Lambda console test event.
- Verified the output from the Lambda test result.
- Checked CloudWatch Logs to confirm the function invocation.
- Changed memory settings to understand how Lambda resource allocation works.
- Changed timeout settings to understand how short timeouts can break execution.

### What I Broke Intentionally

- I reduced the Lambda timeout setting too low.
- I tested the function with a delay that took longer than the configured timeout.
- This caused the Lambda function to fail with a timeout error.

### How I Debugged It

- I checked the Lambda test result in the console.
- I opened the CloudWatch log stream for the function.
- I reviewed the `START`, `END`, and `REPORT` logs.
- I checked the error message showing that the function timed out.
- I compared the configured timeout with the function execution time.

### How I Fixed It

- I increased the Lambda timeout value to allow enough execution time.
- I re-ran the test event after updating the timeout.
- The function executed successfully and returned the expected response.
- I confirmed the successful execution in CloudWatch Logs.

### Key Takeaway

Lambda is useful for running small event-driven workloads without managing servers, but correct timeout, memory, IAM role, and CloudWatch logging setup are important for stable execution and debugging.
