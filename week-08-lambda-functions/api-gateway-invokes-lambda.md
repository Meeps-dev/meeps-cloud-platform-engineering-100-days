## Day 54: API Gateway HTTP API Invoking Lambda

### What I Learned

- API Gateway HTTP API can expose a Lambda function through a public URL.
- Lambda proxy integration forwards HTTP request details to Lambda.
- Routes control which endpoint triggers the Lambda function.
- I used routes such as `GET /health`, `GET /files`, and `GET /files/{fileId}`.
- The invoke URL is the public endpoint used to test the API.
- API Gateway needs permission to invoke Lambda.
- CloudWatch Logs helps confirm that API requests reached the Lambda function.
- Lambda can read metadata from DynamoDB and return it through an API response.

### What I Built

- Created a new Lambda function named `api-handler`.
- Connected the Lambda function to API Gateway HTTP API.
- Created a `/health` route that returns a simple status response.
- Created a `/files` route that reads stored metadata from DynamoDB.
- Created a `/files/{fileId}` route to fetch metadata for a specific file.
- Tested the API using the browser, Postman, or curl.
- Confirmed that Lambda execution logs appeared in CloudWatch.

### What I Broke / Tested

- Tested an incorrect or incomplete API route.
- The request did not return the expected response.
- Also confirmed that file IDs with paths like `uploads/sample.txt` need careful route handling.

### How I Debugged It

- Checked the API Gateway route configuration.
- Verified that the Lambda integration was attached to the correct routes.
- Checked the Lambda execution role permissions.
- Reviewed CloudWatch Logs to confirm whether the Lambda function was invoked.
- Compared the requested path with the route defined in API Gateway.

### How I Fixed It

- Corrected the API Gateway route configuration.
- Confirmed that API Gateway had permission to invoke Lambda.
- Ensured the Lambda function had DynamoDB read permissions.
- Re-tested `/health` and confirmed the correct status response.
- Re-tested `/files` and confirmed that DynamoDB metadata was returned.

### Key Takeaway

API Gateway allows Lambda to act like a real backend API. Correct routes, Lambda permissions, DynamoDB read access, and CloudWatch Logs are important for testing and debugging serverless APIs.
