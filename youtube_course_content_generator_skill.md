# Skill: YouTube Course Content Generator

This document defines the strict quality standards, structure, and instructions for generating course materials from educational YouTube playlists.

---

## 📋 Input Parameter Schema

```yaml
Tech_Stack:
  - List of core technologies (e.g. Terraform, AWS, NodeJS)
Destination_Directory: "Target parent folder name"
Playlist_URL: "URL of the YouTube playlist"
Videos:
  - Episode_XX:
      Title: "Video Title"
      URL: "Video URL"
      Tech: "Specific technologies for this episode"
```

---

## 🎖️ Quality Standards & Requirements

### 1. Production-Grade Examples
All code files (e.g. `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`) must meet production standards:
* **Numbered Directories:** Use ordered numeric prefixes (e.g. `01_terraform_introduction`, `02_vs_code_ec2`) for example directories to keep them organized and non-clumsy.
* **Modular Configuration:** Organize resources across separate files (`providers.tf`, `variables.tf`, `main.tf`, `outputs.tf`) rather than clumping everything into a single file.
* **Fully Formatted & Valid:** Must conform strictly to standard formatting guidelines (e.g. `terraform fmt`).
* **Variable Driven:** Do not hardcode secrets, IPs, ARNs, or instance IDs. Use variables with correct types, descriptions, and validations.
* **Security First:** Include appropriate security practices (e.g., ingress rules limited to specific CIDRs, least-privilege IAM policies, encrypted DB resources).
* **Tagging Strategy:** Apply standard tagging structures (e.g., Project, Environment, Owner, ManagedBy) to all resource blocks.
* **State Management:** Demonstrate state locking and remote backend configurations where appropriate.

### 2. High-Value Summaries & Architectural Notes
Summaries are not mere transcripts; they must provide:
* **Deep Conceptual Explanations:** Deep dive into how services work together under the hood.
* **Architectural Visualizations:** Include diagrams or text-based charts describing the target topology (e.g., public/private subnets, NAT flows).
* **Industry Best Practices:** Contrast the video content with industry standards, noting what to do differently in production.
* **Detailed Q&As:** Address common architectural interview questions related to the topic.

### 3. Step-by-Step Lesson Guides (Transcripts)
Transcript files must serve as complete textual walkthroughs containing:
* **Prerequisites & Installation:** Exact commands and links to install required CLI tools.
* **Step-by-Step Instructions:** Execution logs, sample command prompts, and exact CLI commands (e.g., `terraform plan -out=tfplan`, `terraform apply tfplan`).
* **Common Gotchas & Troubleshooting:** List potential errors (e.g., name conflicts, subnet allocation limits) and how to resolve them.

---

## ⚙️ Scaffolding & Execution Pipeline

1. **Root Scaffolding:** Create `Destination_Directory/`.
2. **Directory segregation:** Create `examples/`, `summaries/`, and `transcripts/` subdirectories.
3. **Episode Generation:** For each episode, generate comprehensive code modules under `examples/`, high-quality summary markdown notes under `summaries/`, and detailed guide documents under `transcripts/`.
4. **Course Catalog:** Create `README.md` at the root of `Destination_Directory/` as the primary table of contents.
