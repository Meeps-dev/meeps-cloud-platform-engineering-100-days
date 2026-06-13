## Bastion Host and Secure Private EC2 Access

### What I Did

For this task, I used my public EC2 instance as a Bastion Host to securely access my private EC2 instance.

The private EC2 instance was placed inside a private subnet and had no public IPv4 address. This means it could not be accessed directly from the internet. Instead of exposing the private server publicly, I connected to it through the public EC2 instance located in the public subnet.

This setup helped me understand how engineers securely access private servers in a cloud environment.

---

### Architecture

```text
Your Laptop
   ↓ SSH
Public EC2 / Bastion Host
   ↓ SSH
Private EC2
```

---

### Steps I Followed

1. Confirmed that the public EC2 instance was running inside the public subnet.
2. Confirmed that the private EC2 instance was running inside the private subnet.
3. Confirmed that the public EC2 instance had a public IPv4 address.
4. Confirmed that the private EC2 instance had no public IPv4 address.
5. Updated the public EC2 Security Group to allow SSH only from my IP address:

```text
SSH | TCP | 22 | My IP
```

6. Updated the private EC2 Security Group to allow SSH only from the public EC2 Security Group:

```text
SSH | TCP | 22 | Source: Public EC2 Security Group
```

7. Connected from my laptop into the public EC2 instance using SSH.
8. From the public EC2 instance, connected into the private EC2 instance using its private IP address.
9. Confirmed that I was inside the private EC2 instance.
10. Removed the private key from the public EC2 instance after testing.

---

### Commands Used

From my laptop, I connected to the public EC2 instance:

```bash
ssh -i my-key.pem ubuntu@PUBLIC_EC2_PUBLIC_IP
```

Then I copied the key to the public EC2 instance for this learning lab:

```bash
scp -i my-key.pem my-key.pem ubuntu@PUBLIC_EC2_PUBLIC_IP:/home/ubuntu/
```

Inside the public EC2 instance, I fixed the key permission:

```bash
chmod 400 my-key.pem
```

Then I connected to the private EC2 instance using its private IP address:

```bash
ssh -i my-key.pem ubuntu@PRIVATE_EC2_PRIVATE_IP
```

To confirm I was inside the private EC2 instance, I ran:

```bash
hostname
hostname -I
ip addr
```

After testing, I deleted the key from the public EC2 instance:

```bash
rm my-key.pem
```

---

### What I Learned

- A Bastion Host is a public server used as a controlled entry point into private servers.
- The public EC2 instance sits in the public subnet and has a public IP address.
- The private EC2 instance sits in the private subnet and has no public IP address.
- Private servers should not be exposed directly to the internet.
- The private EC2 can still be accessed securely through the Bastion Host.
- The private EC2 Security Group should not allow SSH from `0.0.0.0/0`.
- The private EC2 should only allow SSH from the Bastion Host Security Group.
- The Bastion Host should only allow SSH from a trusted IP address.
- This reduces the attack surface of the private server.
- In production, copying private keys to a Bastion Host is not recommended.
- A better production approach is to use SSH agent forwarding, EC2 Instance Connect, or AWS Systems Manager Session Manager.

---

### Security Group Setup

#### Public EC2 Security Group

```text
Inbound:
SSH | TCP | 22 | My IP
```

This means only my own IP address can SSH into the Bastion Host.

#### Private EC2 Security Group

```text
Inbound:
SSH | TCP | 22 | Public EC2 Security Group
```

This means only the Bastion Host can SSH into the private EC2 instance.

---

### Why This Is Important

Directly exposing private servers to the internet is dangerous because attackers can scan public IP addresses and attempt to break into open services like SSH.

By using a Bastion Host, the private server remains hidden inside the private subnet. It does not need a public IP address, and it does not accept direct traffic from the internet.

This is closer to how real production cloud environments are designed.

---

### Key Takeaway

A Bastion Host provides a secure path into private infrastructure.

Instead of exposing private EC2 instances directly to the internet, access is controlled through one public entry point. This keeps private servers more secure while still allowing engineers to manage them when needed.

---

### Screenshots Added

- Public EC2 instance running in the public subnet.
- Private EC2 instance running in the private subnet.
- Private EC2 showing no public IPv4 address.
- Public EC2 Security Group allowing SSH from my IP only.
- Private EC2 Security Group allowing SSH from the public EC2 Security Group only.
- Terminal showing successful SSH from laptop to public EC2.
- Terminal showing successful SSH from public EC2 to private EC2.
- Terminal showing private EC2 private IP address.
- Terminal showing key deleted from the public EC2 after testing.

---

### Cost and Cleanup Note

After completing this practice, I can terminate the EC2 instances and delete unused networking resources to avoid unnecessary AWS billing.

If the NAT Gateway is still running, it should also be deleted after testing because it can generate charges.
