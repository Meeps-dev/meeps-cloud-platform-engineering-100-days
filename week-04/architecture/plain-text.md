                           INTERNET USERS
                                |
                                |
                                v
                        INTERNET GATEWAY
                                |
                                |
                                v
        =====================================================
        |                    WEEK 4 VPC                     |
        |                                                   |
        |  =====================     =====================  |
        |  |   PUBLIC SUBNET A  |     |   PUBLIC SUBNET B  | |
        |  |        AZ A        |     |        AZ B        | |
        |  |                    |     |                    | |
        |  |   ALB Node / ENI   |     |   ALB Node / ENI   | |
        |  =====================     =====================  |
        |              \                     /              |
        |               \                   /               |
        |                v                 v                |
        |        APPLICATION LOAD BALANCER                  |
        |                Listener: HTTP :80                  |
        |                SG: Allow HTTP from Internet        |
        |                         |                         |
        |                         v                         |
        |                  TARGET GROUP                     |
        |              Health Check Path: /                 |
        |              Expected Response: 200 OK            |
        |                    /              \               |
        |                   /                \              |
        |                  v                  v             |
        |  =====================     =====================  |
        |  |  PRIVATE SUBNET A |     |  PRIVATE SUBNET B |  |
        |  |       AZ A        |     |       AZ B        |  |
        |  |                   |     |                   |  |
        |  | Private EC2 Web 1 |     | Private EC2 Web 2 |  |
        |  | Nginx Port: 80   |     | Nginx Port: 80   |  |
        |  | No Public IP     |     | No Public IP     |  |
        |  =====================     =====================  |
        |                                                   |
        =====================================================
