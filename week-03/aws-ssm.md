## AWS Systems Manager Session Manager

### What I Did

For this task, I used AWS Systems Manager Session Manager to connect to an EC2 instance without using SSH.

Instead of opening port `22`, using an SSH key, or connecting through a Bastion Host, I connected to the EC2 instance directly from the AWS Console using Session Manager.

This helped me understand a safer and more modern way to access cloud servers.

---

### Architecture

```text id="lvpyqn"
AWS Console
   ↓
Systems Manager Session Manager
   ↓
EC2 Instance
```

---

### Steps I Followed

1. Created an IAM role for EC2.
2. Attached the AWS managed policy:

```text id="ewoz07"
AmazonSSMManagedInstanceCore
```

3. Launched a temporary EC2 instance.
4. Attached the IAM role to the EC2 instance.
5. Used a security group with no inbound SSH rule.
6. Confirmed the instance had outbound internet access.
7. Opened AWS Systems Manager.
8. Checked that the EC2 instance appeared under managed nodes.
9. Started a Session Manager session from the AWS Console.
10. Ran basic Linux commands inside the browser terminal.
11. Terminated the EC2 instance after taking screenshots.

---

### Commands Used

Inside the Session Manager browser terminal, I ran:

```bash id="lxf1j1"
whoami
```

```bash id="b3wx8t"
hostname
```

```bash id="cdv696"
ip addr
```

These commands confirmed that I had shell access to the EC2 instance without using SSH.

---

### What I Learned

- AWS Systems Manager is used to manage and access AWS resources like EC2 instances.
- Session Manager allows shell access into EC2 from the AWS Console or CLI.
- Session Manager does not require SSH keys.
- Session Manager does not require port `22` to be open.
- Session Manager does not require the EC2 instance to allow inbound traffic.
- Access is controlled through IAM permissions.
- The EC2 instance needs an IAM role with `AmazonSSMManagedInstanceCore`.
- The EC2 instance also needs SSM Agent running.
- The EC2 instance must be able to reach AWS Systems Manager services.
- For public EC2 instances, this can happen through internet access.
- For private EC2 instances, this can happen through NAT Gateway or VPC Interface Endpoints.

---

### Security Group Setup

For this task, I used a security group with no inbound rules:

```text id="pk2ub8"
Inbound rules:
None
```

Outbound traffic was left as default:

```text id="r77pxu"
Outbound rules:
All traffic → 0.0.0.0/0
```

This proves that Session Manager does not need inbound SSH access.

---

### Why Session Manager Is Safer Than SSH

Session Manager is safer than normal SSH because:

- No SSH key needs to be shared.
- No inbound SSH port needs to be opened.
- No public SSH access is required.
- IAM controls who can connect.
- Access can be logged and audited.
- It reduces the need for Bastion Hosts.
- It reduces the attack surface of the EC2 instance.

---

### Key Difference From Bastion Host

With a Bastion Host, the access flow is:

```text id="qgbfet"
Laptop
   ↓ SSH
Public EC2 Bastion Host
   ↓ SSH
Private EC2
```

With Session Manager, the access flow is:

```text id="nahmsy"
AWS Console / AWS CLI
   ↓
Systems Manager
   ↓
EC2 Instance
```

Session Manager removes the need to expose a public server just for access.

---

### Key Takeaway

AWS Systems Manager Session Manager is a modern and safer way to access EC2 instances.

It allows engineers to manage servers without opening SSH, without using key pairs, and without relying on a Bastion Host. This makes server access more secure, easier to audit, and closer to how many production cloud environments are managed.

---

### Screenshots Added

- IAM role created for EC2.
- `AmazonSSMManagedInstanceCore` policy attached to the IAM role.
- EC2 instance launched with the IAM role attached.
- EC2 security group showing no inbound SSH rule.
- Systems Manager managed nodes showing the EC2 instance.
- Session Manager start session page.
- Browser terminal connected to the EC2 instance.
- Terminal output showing `whoami`, `hostname`, and `ip addr`.

---

### Cleanup Note

After completing the task, I terminated the temporary EC2 instance to avoid unnecessary AWS billing.

I kept the IAM role because IAM roles do not generate cost by themselves and can be reused for future Session Manager labs.
