## Security Groups vs Network ACLs

### What I Did

For this task, I reviewed how Security Groups and Network ACLs control traffic inside an AWS VPC.

I confirmed that my public EC2 instance was protected by a Security Group that only allowed SSH from my own IP address. I also confirmed that my private EC2 instance only allowed SSH from the public EC2 Security Group.

After reviewing Security Groups, I opened the Network ACLs section in the VPC dashboard, studied the default NACL rules, created a test NACL, intentionally blocked HTTP traffic on port `80`, observed how the application traffic broke, and then restored the correct rule.

This helped me understand the difference between instance-level security and subnet-level security.

---

### Architecture

```text
Your Laptop
   ↓ SSH
Public EC2 / Bastion Host
   ↓ SSH
Private EC2
```

For the NACL test:

```text
Browser / curl
   ↓ HTTP port 80
Public Subnet
   ↓
Public EC2 running Nginx
```

---

### Security Group Review

#### Public EC2 Security Group

The public EC2 instance was in the public subnet and had a public IPv4 address.

Its Security Group allowed:

```text
SSH  | TCP | 22 | My IP
HTTP | TCP | 80 | 0.0.0.0/0
```

The important security rule was:

```text
SSH | TCP | 22 | My IP
```

This means only my own IP address could SSH into the public EC2 instance.

I made sure SSH was not open to:

```text
0.0.0.0/0
```

because that would allow the whole internet to attempt SSH access.

---

#### Private EC2 Security Group

The private EC2 instance was in the private subnet and had no public IPv4 address.

Its Security Group allowed:

```text
SSH | TCP | 22 | Source: Public EC2 Security Group
```

This means the private EC2 could only be accessed from the public EC2/Bastion Host.

The private EC2 did not allow SSH from:

```text
0.0.0.0/0
```

and did not allow direct SSH from my laptop.

---

### Network ACL Review

I opened the Network ACLs section in the VPC dashboard and reviewed the default NACL.

The default NACL allowed all inbound and outbound traffic.

Example default inbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

Example default outbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

The `*` rule is the final default deny rule. If traffic does not match an allow rule, it is denied.

---

### Test NACL Created

I created a separate test Network ACL instead of modifying the default NACL directly.

Test NACL name:

```text
meeps-test-public-nacl
```

I associated this test NACL with the public subnet.

Before blocking anything, I added allow-all rules so traffic would continue working.

Inbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
```

Outbound rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
```

After associating the test NACL with the public subnet, I confirmed that SSH and HTTP were still working.

---

### What We Broke Intentionally

To understand how NACLs can block traffic, I intentionally blocked HTTP traffic on port `80`.

I added this inbound deny rule to the test NACL:

```text
90 | HTTP | TCP | 80 | 0.0.0.0/0 | DENY
```

This rule was added before the allow-all rule:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
```

So the NACL looked like this:

```text
90  | HTTP        | TCP | 80  | 0.0.0.0/0 | DENY
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
*   | All traffic | All | All | 0.0.0.0/0 | DENY
```

Because NACL rules are processed from the lowest rule number first, rule `90` blocked HTTP traffic before rule `100` could allow it.

---

### What Happened After Blocking Port 80

Before the deny rule, the Nginx page on the public EC2 was accessible through the browser.

After adding the deny rule for HTTP port `80`, the Nginx page stopped loading.

When I tested with:

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

the request failed or timed out.

This proved that even though the Security Group allowed HTTP traffic, the Network ACL blocked it at the subnet level before it could reach the EC2 instance.

SSH still worked because I only blocked HTTP port `80`, not SSH port `22`.

---

### How I Fixed It

To restore HTTP access, I removed the deny rule from the test NACL:

```text
90 | HTTP | TCP | 80 | 0.0.0.0/0 | DENY
```

After deleting that rule, the allow-all rule started allowing HTTP traffic again:

```text
100 | All traffic | All | All | 0.0.0.0/0 | ALLOW
```

Then I tested the public EC2 again:

```bash
curl http://PUBLIC_EC2_PUBLIC_IP
```

The Nginx page worked again.

This confirmed that the issue was caused by the NACL deny rule, not the EC2 instance, not Nginx, and not the Security Group.

---

### What I Learned

- Security Groups work at the instance or network interface level.
- Network ACLs work at the subnet level.
- Security Groups are stateful.
- Network ACLs are stateless.
- Security Groups only support allow rules.
- Network ACLs support both allow and deny rules.
- NACL rule order matters.
- Lower rule numbers are evaluated first.
- A deny rule in a NACL can block traffic even if the Security Group allows it.
- NACLs can break traffic if return traffic or ephemeral ports are not allowed.
- Security Groups are usually the main firewall used for EC2-level access.
- NACLs are useful for extra subnet-level control.

---

### Security Group vs NACL Comparison

| Feature               | Security Group                   | Network ACL                   |
| --------------------- | -------------------------------- | ----------------------------- |
| Level                 | Instance/network interface level | Subnet level                  |
| Stateful              | Yes                              | No                            |
| Rule type             | Allow rules only                 | Allow and deny rules          |
| Rule order matters    | No                               | Yes                           |
| Return traffic        | Automatically allowed            | Must be allowed manually      |
| Common use            | Main resource firewall           | Extra subnet-level protection |
| Risk if misconfigured | Can expose or block a resource   | Can break an entire subnet    |

---

### Stateful vs Stateless

Security Groups are stateful.

This means if inbound traffic is allowed, the response traffic is automatically allowed back.

Network ACLs are stateless.

This means both inbound and outbound traffic must be explicitly allowed. If one direction is blocked, the connection can fail.

This is why NACLs require more care, especially with ephemeral ports.

---

### Ephemeral Ports

Ephemeral ports are temporary high-numbered ports used for return traffic.

For example, when a client connects to a web server on port `80` or `443`, the response traffic may return through an ephemeral port.

Because NACLs are stateless, return traffic must also be allowed. If ephemeral ports are blocked, traffic may fail even when the main application port is allowed.

---

### Key Takeaway

Security Groups and Network ACLs both control traffic, but they work at different levels.

Security Groups protect individual resources like EC2 instances.

Network ACLs protect entire subnets.

In this task, I intentionally broke HTTP access by adding a NACL deny rule for port `80`. Then I fixed it by removing the deny rule. This showed that NACLs can override Security Group access and block traffic before it reaches the EC2 instance.

---

### Screenshots Added

- Public EC2 Security Group allowing SSH from my IP only.
- Public EC2 Security Group allowing HTTP on port `80`.
- Private EC2 Security Group allowing SSH only from the public EC2 Security Group.
- Default NACL inbound rules.
- Default NACL outbound rules.
- Test NACL created.
- Test NACL associated with the public subnet.
- Nginx/HTTP working before the deny rule.
- NACL deny rule blocking HTTP port `80`.
- HTTP request failing after the deny rule.
- SSH still working after HTTP was blocked.
- HTTP working again after removing the deny rule.
- Public subnet restored to the original/default NACL.

---

### Cleanup Note

After completing the test, I removed the HTTP deny rule and restored the correct NACL configuration.

I also reassociated the public subnet back to the original/default NACL and deleted the test NACL to keep the VPC clean.

```

```
