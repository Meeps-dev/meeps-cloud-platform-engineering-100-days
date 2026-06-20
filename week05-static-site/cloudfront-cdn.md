# Day 31: CloudFront CDN

## What I Learned

- CloudFront is a CDN that delivers website files faster by caching them closer to users.
- A CloudFront distribution is the setup that connects users to the website content.
- The origin is where CloudFront gets the files from. In this project, my origin is an S3 bucket.
- The default root object tells CloudFront which file to load first.
- For a static website, the default root object should be `index.html`.
- Viewer protocol policy controls how users access the site.
- I used `Redirect HTTP to HTTPS` so HTTP requests are redirected securely.
- CloudFront can cache old files, so invalidation is needed when updated files do not show immediately.

## What I Broke

- I did not set `index.html` as the default root object in CloudFront at first.
- Because of this, the CloudFront root URL did not load the homepage correctly.

## How I Fixed It

- I edited the CloudFront distribution settings.
- I set the default root object to `index.html`.
- After the distribution updated, the CloudFront URL loaded the homepage correctly.
- I also updated `index.html` to Version 2 and confirmed the site was delivered through CloudFront.

## Key Takeaway

- CloudFront should be configured properly with an S3 origin, a default root object, HTTPS redirect, and cache invalidation when needed.
- The secure setup is: users access CloudFront, while S3 stays private behind it.
