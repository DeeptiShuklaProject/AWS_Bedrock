# Episode 2 Summary: VS Code and AWS CLI Integration

This lab configures the local developer workstation using VS Code, HashiCorp Terraform extensions, and AWS CLI credentials profiles.

## Developer Best Practices
- **VS Code Extension:** Install the official HashiCorp Terraform extension for auto-formatting, syntax highlighting, and schema validation.
- **AWS CLI Profiles:** Avoid embedding hardcoded credentials. Use `shared_credentials_files` or IAM Roles/SSO profiles.
