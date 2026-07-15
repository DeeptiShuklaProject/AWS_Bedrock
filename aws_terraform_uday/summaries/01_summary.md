# Episode 1 Summary: Terraform Introduction & S3 Provisioning

This lab introduces Infrastructure as Code (IaC) using Terraform. It establishes the foundations of configuration, planning, and applying resources.

## Architectural Notes
S3 buckets in production must always be locked down. Our template configures:
- **Server-Side Encryption (SSE-S3):** All objects encrypted at rest using AES256.
- **Public Access Block:** Strict protection blocking all public ACLs and bucket policies to avoid data leaks.

## Q&A & Interview Prep
* **Q: Why use Terraform over AWS CloudFormation?**
  * **A:** Terraform is cloud-agnostic, uses HashiCorp Configuration Language (HCL) which is highly readable, supports a rich provider ecosystem, and has a strong community.
