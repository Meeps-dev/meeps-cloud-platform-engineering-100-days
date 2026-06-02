# Day 3: Networking Basics

## What I Learned

Today, I learned the basic networking concepts that cloud engineers need to understand before working deeply with AWS infrastructure.

## Topics Covered

- What happens when a user opens a website
- How DNS converts domain names into IP addresses
- Why applications use ports
- Why HTTPS is important for secure communication
- How firewalls control allowed and blocked traffic
- How load balancers distribute traffic across servers
- Why companies use private networks to protect internal systems

## Key Takeaways

- DNS helps browsers find the correct server behind a domain name.
- Ports allow different services to run on the same server.
- HTTPS protects user data by encrypting communication.
- Firewalls protect servers by controlling incoming and outgoing traffic.
- Load balancers improve reliability by spreading traffic across multiple servers.
- Private networks keep sensitive systems like databases away from the public internet.

## Practical Task Completed

I documented what happens when a user visits my backend API from their browser.

Flow:

```text
User → Browser → DNS → Internet → Load Balancer → Server → Application → Database → Response
```

## Why This Matters

Networking is a core foundation of cloud engineering. Before deploying applications to AWS, I need to understand how requests move from users to servers, how traffic is routed, and how systems are protected in production.

# What Happens When a User Visits My Backend API?

## Simple Flow

```text
User
  ↓
Browser
  ↓
DNS
  ↓
Internet
  ↓
Load Balancer
  ↓
Server
  ↓
Application
  ↓
Database
  ↓
Response
  ↓
Browser
  ↓
User
```

## Diagram

```text
+--------+      +---------+      +------+      +----------+
|  User  | ---> | Browser | ---> | DNS  | ---> | Internet |
+--------+      +---------+      +------+      +----------+
                                      ↓
                              +---------------+
                              | Load Balancer |
                              +---------------+
                                      ↓
                              +---------------+
                              |    Server     |
                              +---------------+
                                      ↓
                              +---------------+
                              | Application   |
                              +---------------+
                                      ↓
                              +---------------+
                              |   Database    |
                              +---------------+
                                      ↓
                              +---------------+
                              |   Response    |
                              +---------------+
                                      ↓
                              +---------+
                              | Browser |
                              +---------+
```

## Explanation

- The user enters the API URL in the browser.
- The browser checks DNS to find the server IP address.
- The request travels through the internet.
- The load balancer receives the request first.
- The load balancer forwards the request to a healthy server.
- The server sends the request to the backend application.
- The application processes the request.
- The application may read from or write to the database.
- The database returns the needed data.
- The application sends a response back to the browser.
- The user sees the result.
