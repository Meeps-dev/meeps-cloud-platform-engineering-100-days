# Week 5: Static Website Hosting with S3, CloudFront, Route 53, and ACM

## Project Overview

In Week 5, I built and deployed a static portfolio/documentation website on AWS using:

- Amazon S3 for static file storage
- Amazon CloudFront as a CDN
- Amazon Route 53 for DNS
- AWS Certificate Manager for HTTPS
- A private S3 bucket protected behind CloudFront

The goal was to understand how static content, CDN delivery, DNS, and HTTPS work together in a production-style AWS setup.

---

## Architecture

```text
User Browser
    ↓
Route 53 DNS Record
    ↓
CloudFront Distribution
    ↓
Private S3 Bucket
    ↓
Static Website Files
```

---

## AWS Services Used

- **Amazon S3**
  - Used to store static website files such as `index.html`, `error.html`, `style.css`, and assets.

- **Amazon CloudFront**
  - Used as a CDN to deliver the website faster and more securely.

- **Amazon Route 53**
  - Used to manage DNS records and point my custom domain to CloudFront.

- **AWS Certificate Manager**
  - Used to request and validate an SSL/TLS certificate for HTTPS.

- **IAM / Bucket Policy**
  - Used to control access between CloudFront and the private S3 bucket.

---

## Website Details

```text
S3 Bucket: week5-static-site-meeps
CloudFront Domain: d1bfd4zq0t05xh.cloudfront.net
Custom Domain: portfolio.meepsstore.me
```

---

## Project File Structure

```text
week5-static-site/
├── index.html
├── error.html
├── style.css
└── assets/
```

---

## What I Learned

- How S3 stores files as objects inside buckets.
- Difference between object storage and block storage.
- How S3 static website hosting works.
- How bucket policies control access to S3 objects.
- Why public S3 buckets can be risky.
- How to keep S3 private and serve content through CloudFront.
- How CloudFront works as a CDN.
- How CloudFront caching can affect updated content.
- How to use invalidation to clear old cached files.
- How Route 53 manages DNS records.
- Difference between `A`, `CNAME`, and `Alias` records.
- How ACM provides SSL/TLS certificates for HTTPS.
- Why CloudFront certificates must be created in `us-east-1`.
- How DNS validation proves domain ownership.
- How HTTP redirects to HTTPS.

---

## DNS Flow

```text
1. User enters portfolio.meepsstore.me in the browser.
2. Route 53 receives the DNS query.
3. Route 53 uses an A Alias record to point the domain to CloudFront.
4. CloudFront receives the user request.
5. CloudFront checks if the content is already cached.
6. If not cached, CloudFront fetches the files from the private S3 bucket.
7. S3 returns the static files to CloudFront.
8. CloudFront serves the website to the user over HTTPS.
```

---

## Security Setup

- The S3 bucket is private.
- Block Public Access is enabled on the bucket.
- Users cannot access the S3 bucket directly.
- CloudFront is allowed to read files from the S3 bucket.
- The custom domain is secured with an ACM SSL/TLS certificate.
- HTTP traffic redirects to HTTPS.

---

## Implementation Steps

### Day 29: S3 Basics and Static Files

- Created the static website files locally.
- Created the S3 bucket `week5-static-site-meeps`.
- Uploaded:
  - `index.html`
  - `error.html`
  - `style.css`
  - `assets/`

- Confirmed the files existed inside the bucket.
- Kept the bucket private for the final production-style setup.

---

### Day 30: S3 Static Website Hosting and Bucket Policies

- Enabled S3 static website hosting for learning.
- Tested the S3 website endpoint.
- Temporarily added a public-read bucket policy for the lab.
- Confirmed the website could load directly from the S3 website endpoint.
- Removed the public policy after testing.
- Turned Block Public Access back ON.
- Prepared the bucket for private access behind CloudFront.

---

### Day 31: CloudFront CDN

- Created a CloudFront distribution.
- Set the S3 bucket as the CloudFront origin.
- Configured Origin Access Control.
- Set the default root object to `index.html`.
- Set viewer protocol policy to redirect HTTP to HTTPS.
- Allowed `GET` and `HEAD` methods.
- Tested the CloudFront distribution URL.
- Updated `index.html` from Version 1 to Version 2.
- Created a CloudFront invalidation using:

```text
/*
```

- Confirmed CloudFront served the updated version.

---

### Day 32: Route 53 and DNS Records

- Opened the hosted zone for `meepsstore.me`.
- Created an `A` Alias record for:

```text
portfolio.meepsstore.me
```

- Pointed the Alias record to the CloudFront distribution:

```text
d1bfd4zq0t05xh.cloudfront.net
```

- Learned that DNS points the domain to CloudFront, but CloudFront still needs the custom domain and certificate configured.

---

### Day 33: ACM Certificate and HTTPS

- Opened AWS Certificate Manager in `us-east-1`.
- Requested a public certificate for:

```text
portfolio.meepsstore.me
```

- Used DNS validation.
- Created the ACM validation CNAME record in Route 53.
- Waited for the certificate status to become `Issued`.
- Added `portfolio.meepsstore.me` as an alternate domain name in CloudFront.
- Attached the ACM certificate to the CloudFront distribution.
- Waited for CloudFront deployment to complete.

---

### Day 34: Full Integration, Testing, and Debugging

- Tested the full flow from domain to CloudFront to S3.
- Confirmed the site works through CloudFront.
- Confirmed HTTP redirects to HTTPS.
- Confirmed direct S3 access is blocked.
- Tested CloudFront caching behavior.
- Used invalidation when old content was still being served.
- Practiced troubleshooting DNS, CloudFront, S3 access, and HTTPS issues.

---

## Challenges I Faced

### Challenge 1: CloudFront Root URL Did Not Load Correctly

At one point, my CloudFront distribution did not load the homepage correctly because I had not set `index.html` as the default root object.

#### Fix

I edited the CloudFront distribution and set:

```text
Default root object: index.html
```

After CloudFront redeployed, the root CloudFront URL loaded the website correctly.

---

### Challenge 2: S3 Website Endpoint Returned AccessDenied

While testing S3 static website hosting, the website endpoint returned `AccessDenied`.

#### Cause

Block Public Access was still enabled, so the public bucket policy could not expose the files.

#### Fix

For the learning lab only, I temporarily disabled Block Public Access and added a public-read bucket policy.

After testing, I removed the public bucket policy and turned Block Public Access back ON.

---

### Challenge 3: CloudFront Showed Old Content After Updating S3

After updating `index.html`, CloudFront still showed the old version.

#### Cause

CloudFront cached the previous version of the file.

#### Fix

I created a CloudFront invalidation using:

```text
/*
```

After the invalidation completed, CloudFront served the updated version.

---

### Challenge 4: DNS Alone Was Not Enough

After creating the Route 53 Alias record, I learned that DNS alone does not fully make a custom domain work with CloudFront.

#### Cause

CloudFront also needs:

- An alternate domain name
- A matching ACM certificate
- HTTPS configuration

#### Fix

I requested an ACM certificate, validated it with Route 53, added the custom domain to CloudFront, and attached the certificate.

---

## What I Intentionally Broke and Fixed

I intentionally broke parts of the setup to understand real troubleshooting scenarios.

### 1. Removed or missed `index.html`

#### Result

The website could not load the correct homepage.

#### Fix

Uploaded `index.html` again and set it as the CloudFront default root object.

---

### 2. Tried to use a public bucket policy while Block Public Access was ON

#### Result

S3 returned `AccessDenied`.

#### Fix

For the lab, I temporarily disabled Block Public Access.
For the final setup, I restored private access and used CloudFront instead.

---

### 3. Updated S3 content but CloudFront still showed old content

#### Result

The browser still displayed the cached version.

#### Fix

Created a CloudFront invalidation for:

```text
/*
```

---

### 4. Tested direct S3 access

#### Result

Direct access to S3 was blocked.

#### Fix

No fix was needed because this was the expected secure behavior.
Users should access the site through CloudFront only.

---

### 5. Tested incomplete custom domain setup

#### Result

The domain could point to CloudFront but still fail until CloudFront had the correct custom domain and certificate.

#### Fix

Added the alternate domain name to CloudFront and attached the issued ACM certificate.

---

## Screenshots

Add screenshots below:

```text
screenshots/
├── s3-bucket-files.png
├── s3-block-public-access.png
├── s3-static-website-hosting.png
├── cloudfront-distribution.png
├── cloudfront-origin-oac.png
├── cloudfront-default-root-object.png
├── cloudfront-invalidation.png
├── route53-alias-record.png
├── acm-certificate-issued.png
└── https-browser-test.png
```

---

## Final Testing Checklist

- [x] S3 bucket created
- [x] Static website files uploaded
- [x] S3 static website hosting tested
- [x] Bucket policy tested
- [x] Bucket locked back down
- [x] CloudFront distribution created
- [x] S3 bucket connected as CloudFront origin
- [x] Origin Access Control configured
- [x] Default root object set to `index.html`
- [x] HTTP to HTTPS redirect configured
- [x] CloudFront invalidation tested
- [x] Route 53 Alias record created
- [x] ACM certificate requested
- [x] DNS validation completed
- [x] Certificate attached to CloudFront
- [x] Custom domain connected to CloudFront
- [x] HTTPS tested
- [x] Direct S3 access blocked

---

## Key Takeaway

This week helped me understand how static websites are deployed securely on AWS.

The final architecture is:

```text
Route 53
→ CloudFront
→ Private S3 Bucket
```

Route 53 handles DNS, CloudFront delivers and caches the content, S3 stores the static files, and ACM secures the website with HTTPS.

The most important lesson from Week 5 was that production-style hosting is not just about making a website load. It is about making it secure, reliable, correctly routed, and easy to debug.

```

```
