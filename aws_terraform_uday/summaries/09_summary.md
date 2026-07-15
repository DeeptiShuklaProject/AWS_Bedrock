# Episode 9 Summary: Security Groups Configuration

Security Groups serve as virtual firewalls to control ingress and egress traffic flow.

## Hardening Security Groups
- **Least Privilege:** Never leave port 22 open to the world (`0.0.0.0/0`). Restrict admin ports to office CIDRs or use Session Manager.
- **Egress Limits:** Restrict outbound traffic to specific target endpoints for security compliance.
