## Day 55A: EventBridge Scheduled Lambda

### What I Learned

- EventBridge can trigger Lambda automatically on a schedule.
- `rate()` expressions are useful for repeated intervals like `rate(5 minutes)`.
- `cron()` expressions are better for fixed times and advanced schedules.
- Scheduled Lambda jobs remove the need for EC2-based cron servers.
- CloudWatch Logs confirms whether the scheduled Lambda actually ran.

### What I Built

- Created an EventBridge schedule/rule.
- Connected the schedule to a Lambda function.
- Configured the Lambda to run automatically.
- Checked CloudWatch Logs to confirm scheduled execution.

### What I Broke

- Tested a schedule/target configuration issue where Lambda did not run as expected.
- This showed that EventBridge needs the correct Lambda target and invocation permission.

### How I Debugged It

- Checked the EventBridge schedule/rule status.
- Confirmed the Lambda target was attached.
- Checked CloudWatch Logs for new Lambda invocations.
- Verified that the schedule was enabled.

### How I Fixed It

- Corrected the EventBridge target configuration.
- Ensured the schedule was enabled.
- Re-tested and confirmed Lambda logs appeared in CloudWatch.

### Key Takeaway

EventBridge is useful for running background jobs automatically without managing servers.
