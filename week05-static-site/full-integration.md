# Day 34: Full Integration, Testing, and Debugging

## What I Learned

- I learned how the full website traffic flow works from domain to S3.
- The end-to-end flow is:
  - User enters the domain
  - Route 53 resolves the domain
  - CloudFront receives the request
  - CloudFront fetches files from the private S3 bucket
  - ACM secures the site with HTTPS
- I confirmed that HTTP traffic should redirect to HTTPS.
- I learned that S3 should remain private and users should only access the website through CloudFront.
- I also learned that CloudFront may serve cached files, so invalidation is needed when updated content does not show immediately.

## What I Broke

- I tested direct access to the S3 bucket/object and confirmed it should not be publicly accessible.
- I also tested how the site behaves when CloudFront caching still shows old content after updating files in S3.
- These checks helped me understand common production issues like:
  - DNS not resolving correctly
  - HTTPS not working
  - CloudFront showing old content
  - S3 returning `AccessDenied`

## How I Fixed It

- I confirmed Route 53 was pointing the domain to the correct CloudFront distribution.
- I confirmed CloudFront had access to the private S3 bucket.
- I verified that S3 public access stayed blocked.
- I used CloudFront invalidation when updated files did not appear immediately.
- I tested both HTTP and HTTPS to confirm the redirect and secure access worked properly.

## Key Takeaway

- Day 34 helped me understand how to test and debug the full static website setup.
- The final working flow is: Route 53 → CloudFront → Private S3, secured with ACM HTTPS.
