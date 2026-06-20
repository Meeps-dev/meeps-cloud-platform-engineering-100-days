# Day 29: S3 Basics and Static Files

## What I Did

- Created an S3 bucket named `week5-static-site-meeps`.
- Created and uploaded the basic static website files:
  - `index.html`
  - `error.html`
  - `style.css`
  - `assets/`
- Confirmed that all files exist inside the S3 bucket.
- Kept the bucket private for a production-style setup.

## What I Learned

- **S3 Buckets**
  - An S3 bucket is a storage container for files in AWS.
  - It can store static website files, images, logs, backups, and documents.

- **Objects**
  - Files uploaded into S3 are called objects.
  - Examples: `index.html`, `error.html`, and `style.css`.

- **Object Keys**
  - An object key is the file name or path inside the bucket.
  - Example: `assets/logo.png`.

- **Regions**
  - S3 buckets are created in a specific AWS Region.
  - The region affects where the files are stored.

- **Object Storage vs Block Storage**
  - S3 is object storage, used for storing files.
  - EBS is block storage, used like a disk attached to an EC2 instance.

- **S3 Folder Structure**
  - S3 does not use real folders like a normal computer.
  - It uses prefixes to make objects appear like folders.

## Key Takeaway

- S3 is useful for storing static website files securely.
- For this project, S3 will store the website files, while CloudFront will later deliver them to users through a CDN.
