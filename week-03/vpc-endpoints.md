## VPC Endpoints

### What I Did

For this task, I created a **VPC Endpoint** to allow resources inside my private subnet to access AWS services privately without depending on the public internet or a NAT Gateway.

The main endpoint I created was an **S3 Gateway Endpoint**. This allowed my private EC2 instance to reach Amazon S3 through the private AWS network instead of routing traffic through a NAT Gateway or Internet Gateway.

I also used **Systems Manager Interface Endpoints** so I could connect to the private EC2 instance using AWS Systems Manager Session Manager without SSH, without a public IP, and without a NAT Gateway.

---

### Architecture

```text
AWS Console
   ↓
Systems Manager Interface Endpoints
   ↓
Private EC2
   ↓
Private Route Table
   ↓
S3 Gateway Endpoint
   ↓
Amazon S3
```

Simplified S3 access flow:

```text
Private EC2
   ↓
Private Route Table
   ↓
S3 Gateway Endpoint
   ↓
Amazon S3
```

---

### Steps I Followed

1. Confirmed that my VPC and private subnet existed.
2. Confirmed that the private subnet was associated with the private route table.
3. Created a security group for the VPC Interface Endpoints.
4. Created a private EC2 security group with no inbound SSH access.
5. Created the required Systems Manager Interface Endpoints:

```text
com.amazonaws.REGION.ssm
com.amazonaws.REGION.ssmmessages
com.amazonaws.REGION.ec2messages
```

6. Created an **S3 Gateway Endpoint**.
7. Attached the S3 Gateway Endpoint to my VPC.
8. Selected the private route table for the S3 Gateway Endpoint.
9. Confirmed that the private route table was updated with an S3 prefix list route.
10. Launched a private EC2 instance with no public IPv4 address.
11. Attached an IAM role to the EC2 instance.
12. Added the required IAM policies for Systems Manager and S3 testing.
13. Connected to the private EC2 instance using Session Manager.
14. Tested S3 access from the private EC2 instance.

---

### Endpoint Types Used

#### S3 Gateway Endpoint

I created an S3 Gateway Endpoint so that resources inside my VPC could access Amazon S3 privately.

The private route table was updated with a route similar to:

```text
Destination: pl-xxxxxxxx
Target: vpce-xxxxxxxx
```

The `pl-xxxxxxxx` value represents the AWS-managed S3 prefix list.

The `vpce-xxxxxxxx` value represents the VPC Endpoint.

---

#### Systems Manager Interface Endpoints

I also created Interface Endpoints for Systems Manager so that my private EC2 instance could be accessed through Session Manager without using NAT Gateway or SSH.

The Interface Endpoints created were:

```text
SSM
SSM Messages
EC2 Messages
```

These endpoints allowed the private EC2 instance to communicate with AWS Systems Manager privately.

---

### IAM Role Used

The private EC2 instance used an IAM role with:

```text
AmazonSSMManagedInstanceCore
```

This allowed the EC2 instance to register with AWS Systems Manager.

For S3 testing, I also attached S3 permission such as:

```text
AmazonS3ReadOnlyAccess
```

This allowed the private EC2 instance to test access to S3 using the AWS CLI.

---

### Security Group Setup

#### Private EC2 Security Group

The private EC2 security group had no inbound SSH rule.

```text
Inbound rules:
None
```

Outbound traffic was allowed so the instance could reach the VPC endpoints.

```text
Outbound rules:
All traffic allowed
```

---

#### VPC Endpoint Security Group

The Interface Endpoint security group allowed HTTPS traffic from the private EC2 security group.

```text
Inbound:
HTTPS | TCP | 443 | Source: Private EC2 Security Group
```

This allowed the private EC2 instance to communicate with the Systems Manager endpoints over port `443`.

---

### Testing

I connected to the private EC2 instance using AWS Systems Manager Session Manager.

Inside the private EC2 instance, I ran:

```bash
aws --version
```

Then I tested S3 access:

```bash
aws s3 ls
```

This confirmed that the private EC2 instance could reach S3 without using:

```text
Public IP
SSH
Bastion Host
NAT Gateway
Internet Gateway route
```

The private EC2 stayed private but still accessed S3 through the VPC Endpoint.

---

### What I Learned

- VPC Endpoints allow private resources to connect to AWS services without going through the public internet.
- S3 Gateway Endpoints are attached to route tables.
- A Gateway Endpoint is commonly used for S3 and DynamoDB.
- Interface Endpoints create private network interfaces inside the VPC.
- Interface Endpoints are used for services like Systems Manager, CloudWatch, ECR, Secrets Manager, and others.
- PrivateLink powers Interface Endpoints.
- A private EC2 instance does not always need NAT Gateway to access AWS services.
- VPC Endpoints can reduce NAT Gateway dependency.
- VPC Endpoints improve security because traffic stays within the AWS private network.
- Session Manager can be used with Interface Endpoints to access private EC2 instances without SSH.

---

### Gateway Endpoint vs Interface Endpoint

| Feature                   | Gateway Endpoint          | Interface Endpoint                          |
| ------------------------- | ------------------------- | ------------------------------------------- |
| Common services           | S3, DynamoDB              | SSM, CloudWatch, ECR, Secrets Manager, etc. |
| How it works              | Adds route to route table | Creates private network interfaces          |
| Uses security group       | No                        | Yes                                         |
| Uses route table          | Yes                       | Not directly like Gateway Endpoint          |
| Powered by PrivateLink    | No                        | Yes                                         |
| Example used in this task | S3 Gateway Endpoint       | SSM Interface Endpoints                     |

---

### Why This Is Important

In a production AWS environment, private servers should not always depend on the public internet to reach AWS services.

Without VPC Endpoints, a private EC2 instance may need this path:

```text
Private EC2
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
AWS Service
```

With VPC Endpoints, the path becomes:

```text
Private EC2
   ↓
VPC Endpoint
   ↓
AWS Service
```

This is more secure because the traffic stays private, and it can reduce NAT Gateway usage.

---

### Key Takeaway

VPC Endpoints allow private AWS resources to access supported AWS services securely without exposing them to the public internet.

For this task, the private EC2 instance had no public IP, no SSH access, and no NAT Gateway, but it could still connect to AWS services using VPC Endpoints.

This is closer to how secure production cloud networks are designed.

---

### Screenshots Added

- S3 Gateway Endpoint created.
- Endpoint type showing `Gateway`.
- VPC selected for the endpoint.
- Private route table selected for the S3 Gateway Endpoint.
- Private route table showing:

```text
pl-xxxxxxxx → vpce-xxxxxxxx
```

- Systems Manager Interface Endpoints created.
- Private EC2 instance with no public IPv4 address.
- Private EC2 security group showing no inbound SSH rule.
- IAM role attached to the private EC2 instance.
- Session Manager connected to the private EC2 instance.
- Terminal output showing:

```bash
aws --version
aws s3 ls
```

---

### Cleanup Note

After completing the task, I terminated the temporary private EC2 instance to avoid unnecessary EC2 charges.

I also deleted the Systems Manager Interface Endpoints after testing because Interface Endpoints can generate cost.

The S3 Gateway Endpoint can also be deleted after the lab to keep the VPC clean.
