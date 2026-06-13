## NAT Gateway

### What I Did

For this task, I created a NAT Gateway to allow my private EC2 instance to access the internet without exposing it directly to the public internet.

Before creating the NAT Gateway, my private EC2 instance had no public IP address and could not access the internet. This meant commands like `sudo apt update`, `ping google.com`, and `curl ifconfig.me` could not work from the private server.

To solve this, I created a NAT Gateway inside my public subnet and connected it to my private subnet through the private route table.

---

### Steps I Followed

1. Created a custom VPC.
2. Created one public subnet and one private subnet.
3. Created and attached an Internet Gateway to the VPC.
4. Created a public route table and added this route:

```text
0.0.0.0/0 → Internet Gateway
```

5. Created a private route table and associated it with the private subnet.
6. Allocated an Elastic IP address.
7. Created a NAT Gateway inside the public subnet.
8. Attached the Elastic IP to the NAT Gateway.
9. Waited for the NAT Gateway status to become `Available`.
10. Edited the private route table and added this route:

```text
0.0.0.0/0 → NAT Gateway
```

11. Connected to the private EC2 instance through the public EC2/Bastion Host.
12. Tested outbound internet access from the private EC2 instance.

---

### NAT Gateway Architecture

```text
Private EC2
   ↓
Private Route Table
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

---

### What I Learned

- NAT means Network Address Translation.
- A NAT Gateway allows private resources to access the internet securely.
- A NAT Gateway must be placed in a public subnet because it needs access to the Internet Gateway.
- A NAT Gateway needs an Elastic IP so it can communicate with the internet using a public IP address.
- Private subnets do not route directly to the Internet Gateway.
- Instead, the private route table sends internet-bound traffic to the NAT Gateway.
- NAT Gateway allows outbound traffic from private EC2 instances.
- NAT Gateway does not allow the internet to directly connect to private EC2 instances.

---

### Testing

After adding the NAT Gateway route to the private route table, I tested internet access from the private EC2 instance.

Commands used:

```bash
ping google.com
curl ifconfig.me
sudo apt update
```

The test confirmed that the private EC2 instance could now access the internet, even though it still had no public IP address.

---

### Key Takeaway

The NAT Gateway is important in production cloud architecture because it allows private servers to reach the internet for updates, package downloads, API calls, and other outbound traffic without making those servers publicly accessible.

This helps keep backend servers, application servers, and internal systems more secure.

---

### Screenshots Added

- NAT Gateway created and available.
- Elastic IP attached to the NAT Gateway.
- Public subnet where the NAT Gateway was created.
- Private route table with:

```text
0.0.0.0/0 → NAT Gateway
```

- Private EC2 instance showing no public IP.
- Terminal showing successful internet access from private EC2.
- `sudo apt update` working from private EC2.

---

### Cost Note

NAT Gateway is not free. After completing the practice task, I deleted the NAT Gateway and released the Elastic IP to avoid unnecessary AWS billing.
