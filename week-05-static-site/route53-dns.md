# Day 32: Route 53 and DNS Records

## What I Learned

- DNS translates a domain name into the address of a server or AWS service.
- Route 53 is AWS’s DNS service for managing domain records.
- A hosted zone stores DNS records for a domain.
- Name servers tell the internet where the domain’s DNS is managed.
- An `A` record can point a domain to an IPv4 address or an AWS Alias target.
- A `CNAME` record points one domain name to another domain name.
- An Alias record is useful in AWS because it can point directly to services like CloudFront.
- TTL controls how long DNS records are cached before being refreshed.

## What I Did

- Opened the Route 53 hosted zone for `meepsstore.me`.
- Created an `A` Alias record for `portfolio.meepsstore.me`.
- Pointed the Alias record to my CloudFront distribution:
  - `d1bfd4zq0t05xh.cloudfront.net`
- Confirmed that the record exists inside Route 53.

## What I Broke

- I learned that DNS alone is not enough to make the custom domain fully work.
- Even after pointing Route 53 to CloudFront, the domain may still fail if CloudFront does not have:
  - the alternate domain name added
  - a valid ACM certificate
  - HTTPS configured properly

## How I Fixed It

- I used an `A` Alias record instead of a normal CNAME for the Route 53 setup.
- I pointed the record to the correct CloudFront distribution.
- The next fix is to configure ACM and add the custom domain to CloudFront on Day 33.

## Key Takeaway

- Route 53 connects my domain to CloudFront.
- The DNS flow is: user enters domain → Route 53 resolves it → traffic goes to CloudFront → CloudFront serves files from S3.
