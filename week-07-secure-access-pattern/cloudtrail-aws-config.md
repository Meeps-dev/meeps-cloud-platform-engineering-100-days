# Day 47: CloudTrail and AWS Config Basics

## What I Learned

- Learned that **CloudTrail** records AWS API activity.
- Learned that CloudTrail answers: who did what, when, from where, and on which resource.
- Learned that **AWS Config** tracks how AWS resource configurations change over time.
- Understood that CloudTrail shows **who made the change**, while AWS Config shows **what changed**.
- Learned that S3 object-level events may need CloudTrail data events, which can add cost.
- Learned that AWS Config can also add cost if too many resources are recorded.

## What I Did

- Created a CloudTrail trail named `meeps-week7-trail`.
- Enabled multi-region logging.
- Enabled log file validation.
- Used a private S3 bucket for CloudTrail logs.
- Enabled management events for audit logging.
- Generated test activity using:
  - Secrets Manager
  - S3 read access
  - S3 denied write access
- Searched CloudTrail Event History for events like:
  - `GetSecretValue`
  - `ListBucket`
  - `AttachRolePolicy`
  - `AccessDenied`
- Enabled AWS Config for Day 47 audit practice.
- Captured screenshots of AWS Config setup/resource timeline.
- Stopped AWS Config after screenshots for cost control.

## What I Broke / Issue Faced

- Some events did not appear immediately in CloudTrail because logs can take a few minutes to show.
- S3 object-level activity was limited because full S3 data events were not enabled.
- AWS Config was useful, but I had to be careful because it can increase cost if left running.

## How I Fixed It

- Waited a few minutes and searched CloudTrail Event History again.
- Focused on management events like `GetSecretValue` and IAM policy activity.
- Documented that S3 data events were skipped/limited for cost control.
- Enabled AWS Config only for audit practice and stopped it after taking screenshots.

## Security Decision

- CloudTrail was enabled to provide account-level audit visibility.
- CloudTrail log bucket was kept private.
- Log file validation was enabled to help verify log integrity.
- I avoided enabling broad S3 data events to reduce unnecessary cost.
- AWS Config was stopped after documentation to control billing.

## Cost Note

- AWS Config was enabled for Day 47 audit practice and stopped after screenshots for cost control.
- I documented the difference between CloudTrail and AWS Config instead of leaving extra monitoring resources running unnecessarily.

## Key Takeaway

CloudTrail helps me audit AWS actions, while AWS Config helps me understand resource configuration changes. Both are important for security, debugging, compliance, and production-style cloud operations.
