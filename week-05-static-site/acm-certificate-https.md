# Day 33: ACM Certificate and HTTPS

## What I Learned

- ACM is used to request and manage SSL/TLS certificates in AWS.
- SSL/TLS certificates allow websites to use HTTPS securely.
- HTTPS encrypts traffic between the user’s browser and the website.
- For CloudFront, the ACM certificate must be created in `us-east-1`.
- DNS validation proves that I own or control the domain.
- ACM provides a CNAME validation record that must be added to Route 53.
- Once validation is complete, the certificate status changes to `Issued`.
- CloudFront needs both:
  - an Alternate Domain Name
  - a matching ACM certificate

## What I Broke

- The custom domain could not fully work with HTTPS until the ACM certificate was validated and attached to CloudFront.
- I also learned that if the certificate is created in the wrong region, it will not appear inside CloudFront.

## How I Fixed It

- I requested a public ACM certificate in `us-east-1`.
- I added the DNS validation CNAME record in Route 53.
- I waited until the certificate status changed to `Issued`.
- I added my custom domain as an Alternate Domain Name in CloudFront.
- I attached the issued ACM certificate to the CloudFront distribution.
- I waited for CloudFront to redeploy before testing the HTTPS domain.

## Key Takeaway

- Route 53 points the domain to CloudFront, but ACM is what enables HTTPS.
- The full secure flow is: user visits custom domain → Route 53 resolves DNS → CloudFront serves the site → ACM secures the connection with HTTPS.
