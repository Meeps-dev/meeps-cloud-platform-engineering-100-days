                    ┌──────────────────────────────────────┐
                    │              USER BROWSER             │
                    │                                      │
                    │  https://portfolio.meepsstore.me      │
                    └───────────────────┬──────────────────┘
                                        │
                                        │ 1. User enters domain
                                        ▼

┌────────────────────────────────────────────────────────────────────┐
│ ROUTE 53 │
│ │
│ Hosted Zone: meepsstore.me │
│ DNS Record: portfolio.meepsstore.me │
│ Record Type: A Alias │
│ Target: d1bfd4zq0t05xh.cloudfront.net │
└──────────────────────────────┬─────────────────────────────────────┘
│
│ 2. DNS routes request to CloudFront
▼
┌────────────────────────────────────────────────────────────────────┐
│ CLOUDFRONT CDN │
│ │
│ Distribution: week5-cloudfront-distribution-meeps │
│ Default Root Object: index.html │
│ Viewer Protocol Policy: Redirect HTTP to HTTPS │
│ SSL/TLS Certificate: ACM Certificate │
│ Origin Access: CloudFront allowed to read from S3 │
└──────────────────────────────┬─────────────────────────────────────┘
│
│ 3. CloudFront checks cache
│
┌────────────────┴────────────────┐
│ │
▼ ▼
┌──────────────────────────────┐ ┌────────────────────────────────┐
│ CACHE HIT │ │ CACHE MISS │
│ │ │ │
│ CloudFront already has │ │ CloudFront fetches latest │
│ the requested file nearby │ │ file from private S3 bucket │
└──────────────┬───────────────┘ └────────────────┬───────────────┘
│ │
│ ▼
│ ┌──────────────────────────────────┐
│ │ PRIVATE S3 BUCKET │
│ │ │
│ │ Bucket: week5-static-site-meeps │
│ │ Block Public Access: ON │
│ │ Direct public access: blocked │
│ │ │
│ │ Files: │
│ │ - index.html │
│ │ - error.html │
│ │ - style.css │
│ │ - assets/ │
│ └────────────────┬─────────────────┘
│ │
└─────────────────┬───────────────────┘
│
│ 4. Website content returned
▼
┌──────────────────────────────────────┐
│ USER BROWSER │
│ │
│ Static website loads securely │
│ over HTTPS │
└──────────────────────────────────────┘

### HTTPS Certificate Flow

┌──────────────────────────────┐
│ ACM │
│ │
│ Certificate requested in │
│ us-east-1 │
└──────────────┬───────────────┘
│
│ DNS validation record created
▼
┌──────────────────────────────┐
│ ROUTE 53 │
│ │
│ Validation CNAME proves │
│ domain ownership │
└──────────────┬───────────────┘
│
│ Certificate becomes ISSUED
▼
┌──────────────────────────────┐
│ CLOUDFRONT │
│ │
│ ACM certificate attached │
│ to custom domain │
└──────────────┬───────────────┘
│
▼
┌──────────────────────────────┐
│ https://portfolio.meepsstore.me │
│ │
│ Website loads securely │
└──────────────────────────────┘
