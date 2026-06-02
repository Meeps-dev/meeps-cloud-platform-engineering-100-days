# Day 5: EC2 Fundamentals

## What I Learned

Today, I learned how to launch and connect to an AWS EC2 instance. I also installed Nginx and served a basic web page from a cloud server.

## Topics Covered

- EC2 instance
- Ubuntu AMI
- Instance type
- Key pair
- Security group
- SSH
- Public IP
- Private IP
- User data
- Elastic IP
- Nginx web server

## What I Practiced

- Launched an Ubuntu EC2 instance
- Created a `.pem` key pair
- Secured the key file using `chmod 400`
- Allowed SSH access on port `22`
- Connected to the server from my Mac using SSH
- Installed Nginx on the EC2 instance
- Opened HTTP access on port `80`
- Visited the EC2 public IP in my browser
- Replaced the default Nginx page with a custom HTML page

## Commands Used

```bash
cd ~/Downloads
chmod 400 meeps-day-5-key.pem
ssh -i meeps-day-5-key.pem ubuntu@YOUR_PUBLIC_IP

sudo apt update
sudo apt upgrade -y
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
curl localhost

echo "<h1>Meeps Day 5 EC2 Nginx Lab</h1><p>My first AWS EC2 web server is running.</p>" | sudo tee /var/www/html/index.html

exit
```

## Key Takeaways

- EC2 is a virtual server used to run applications in the cloud.
- An AMI is the operating system template used to create the server.
- An instance type defines the server size, CPU, memory, and cost.
- A key pair is used to securely connect to the server.
- SSH allows remote access from my Mac to the EC2 instance.
- A security group works like a firewall for the EC2 server.
- Port `22` is used for SSH access.
- Port `80` is used for HTTP browser access.
- The public IP allows access from the internet.
- The private IP is used inside the AWS private network.
- Nginx can serve web pages from the EC2 instance.

## Why This Matters

This is my first real cloud deployment step.
I did not just create a server, I connected to it, configured it, installed software, opened network access, and served a working web page from AWS.

## Final Result

I successfully launched an EC2 instance, connected through SSH, installed Nginx, and confirmed the web server was accessible from the browser using the EC2 public IP.
