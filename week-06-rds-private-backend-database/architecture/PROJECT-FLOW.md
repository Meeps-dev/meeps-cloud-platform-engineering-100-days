                    WEEK 6 AWS BACKEND + PRIVATE RDS ARCHITECTURE
                    ----------------------------------------------


                                 USER / BROWSER / POSTMAN
                                           |
                                           |
                                           |  HTTP :80
                                           v
                              +-------------------------+
                              |  APPLICATION LOAD       |
                              |  BALANCER               |
                              |  Public Subnets         |
                              |  Port: 80               |
                              +-------------------------+
                                           |
                                           |
                                           |  HTTP :80
                                           |  Source: ALB Security Group
                                           v
                    +------------------------------------------------+
                    |              PRIVATE EC2 BACKEND               |
                    |              Private App Subnet                 |
                    |              No Public IP                       |
                    |                                                |
                    |   +----------------------------------------+   |
                    |   | NGINX Reverse Proxy                    |   |
                    |   | Listens on port 80                     |   |
                    |   +----------------------------------------+   |
                    |                    |                           |
                    |                    | forwards to                |
                    |                    v                           |
                    |   +----------------------------------------+   |
                    |   | FastAPI Backend App                    |   |
                    |   | Runs on 127.0.0.1:3000                 |   |
                    |   |                                        |   |
                    |   | Endpoints:                             |   |
                    |   | GET  /health                           |   |
                    |   | GET  /db-test                          |   |
                    |   | POST /users                            |   |
                    |   | GET  /users                            |   |
                    |   +----------------------------------------+   |
                    +------------------------------------------------+
                                           |
                                           |
                                           |  PostgreSQL :5432
                                           |  Source: Backend EC2 Security Group
                                           v
                              +-----------------------------+
                              |     PRIVATE RDS DATABASE    |
                              |     PostgreSQL              |
                              |     DB Name: appdb          |
                              |     Port: 5432              |
                              |     Public Access: No       |
                              |     Private DB Subnets      |
                              +-----------------------------+
