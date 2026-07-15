# Episode 4 Summary: AWS NAT Gateway & Private Subnets

Securing database and backend application instances by deploying them in isolated private subnets.

## Architectural Design
- **Private Subnet:** Instances here do not have public IPv4 addresses and cannot be accessed from the public internet.
- **NAT Gateway:** Deployed in the public subnet. Allows private subnet instances to initiate outbound connections (e.g. package downloads/security patches) while blocking inbound traffic.
