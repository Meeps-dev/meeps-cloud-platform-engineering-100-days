# Day 46: Create Least-Privilege S3 Read Policy

## What I Learned

- Learned how to give EC2 access to S3 using an IAM role instead of public bucket access.
- Learned that least privilege means granting only the exact S3 actions needed.
- Understood that `s3:ListBucket` applies to the bucket itself.
- Understood that `s3:GetObject` applies to objects inside a specific prefix.
- Learned that write access requires `s3:PutObject`, which was intentionally not allowed.
- Learned that KMS may require `kms:Decrypt` if S3 objects are encrypted with a customer-managed KMS key.
- Confirmed that my EC2 instance was using the IAM role `meeps-week7-ec2-role`.

## What I Did

- Created a least-privilege S3 read-only policy.
- Attached the policy to `meeps-week7-ec2-role`.
- Allowed EC2 to list and read only from the selected S3 prefix:
  - `s3-bucket-meeps/week7-read-only/`
- Tested the IAM identity using:
  - `aws sts get-caller-identity`
- Confirmed the role showed as:
  - `assumed-role/meeps-week7-ec2-role`
- Tested reading from the allowed prefix.
- Successfully downloaded `index.txt` from the allowed S3 prefix.
- Tested uploading a file to the same prefix.
- Confirmed the upload failed with `AccessDenied`.

## What I Broke / Issue Faced

- I initially used the wrong S3 command format by adding an extra space before the object path.
- I also tried to download `sample.txt`, but that object did not exist in the prefix.
- Listing the full bucket failed with `AccessDenied` because the policy only allowed listing the approved prefix.
- Uploading `test.txt` failed with `AccessDenied` because the role did not have `s3:PutObject`.

## How I Fixed It

- Corrected the S3 path format.
- Listed the allowed prefix to confirm the actual object name.
- Downloaded the correct file: `index.txt`.
- Kept the `AccessDenied` upload result as proof that write access was blocked.
- Did not fix the upload failure because it was expected behavior under least privilege.

## Security Decision

- I did not use `s3:*`.
- I did not use `AmazonS3FullAccess`.
- I did not use `AdministratorAccess`.
- I did not make the S3 bucket public.
- I allowed only read access to the required bucket prefix.

## Result

The EC2 role can read from the approved S3 prefix, but cannot write to it or list the entire bucket. This confirms that least-privilege S3 access is working correctly.

## Key Takeaway

Least privilege means giving the EC2 backend only the access it needs. Read access worked, while write and broader bucket access failed as expected.
