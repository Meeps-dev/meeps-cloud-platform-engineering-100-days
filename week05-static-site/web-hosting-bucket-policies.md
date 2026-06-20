# Day 30: S3 Static Website Hosting and Bucket Policies

## What I Learned

- S3 can host static websites using files like `index.html`, `error.html`, and `style.css`.
- Static website hosting gives an S3 website endpoint for testing the site directly from S3.
- Bucket policies control who can access objects inside an S3 bucket.
- Public access allows anyone on the internet to read the files.
- Private access blocks direct public access to the bucket.
- For production, it is safer to keep S3 private and serve the site through CloudFront.
- The S3 website endpoint is useful for learning but does not support HTTPS.
- The S3 REST endpoint is better for the final CloudFront setup.

## What I Broke

- I tried to access the S3 static website while Block Public Access was still enabled.
- The website endpoint returned `AccessDenied` because the bucket was still private.
- I also learned that a public bucket policy will not work properly if Block Public Access is still blocking public access.

## How I Fixed It

- I temporarily turned off Block Public Access for the learning lab.
- I added a temporary public-read bucket policy to allow the website files to load.
- After testing the S3 website endpoint, I removed the public bucket policy.
- I turned Block Public Access back ON to keep the bucket private again.

## Key Takeaway

- Public S3 static hosting is useful for understanding how S3 website hosting works.
- The better production-style setup is private S3 behind CloudFront, where users access the website through CloudFront instead of direct S3.
