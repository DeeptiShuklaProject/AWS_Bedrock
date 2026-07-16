# Module 4 - Prerequisites

## Learning Objectives
* Learn the essential concepts required before working with Docker: Linux CLI, Networking basics, and YAML formatting.

## Prerequisites
* **Prerequisites**: None

---

## Detailed Explanation
### 1. The Linux Command Line
Docker runs natively on Linux. Familiarity with basic Linux CLI operations is crucial:
* `ls`, `cd`, `pwd`, `mkdir`, `rm`
* File permissions: `chmod`, `chown`
* Process management: `ps`, `kill`, `top`
* Text editors: `nano`, `vim`

### 2. Networking Basics
You need to understand:
* **IP Address**: Unique identifier for devices on a network.
* **Port**: Numerical endpoint used by applications to receive network traffic (e.g., HTTP is on port 80).
* **DNS (Domain Name System)**: Maps domain names to IP addresses.
* **Localhost (127.0.0.1)**: Points to your local computer.

### 3. YAML (YAML Ain't Markup Language)
YAML is a human-readable data serialization standard used heavily by Docker Compose and Kubernetes.
Key rules:
* Case sensitive
* Indentation matters (use spaces, not tabs!)
* Key-value pairs: `name: John`
* Lists: prefixed by a hyphen `-`

```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
```

---

## Hands-on Exercise
### Hands-on Exercise: Write a YAML configuration
Create a YAML file named `test.yaml` containing settings for a simulated app stack and validate it.

## Assignment
Write a bash script that starts a script, prints environmental variables, and exits.

---

## Quiz

### Q1: Which character represents a list item in YAML?
- -
- #
- *
- &

*Answer*: **-**

### Q2: What port is typically used for HTTPS?
- 80
- 443
- 8080
- 22

*Answer*: **443**

---

## Interview Preparation

### Q: Why is Linux shell knowledge critical for Docker?
*Answer*: Docker is based on Linux kernel primitives (namespaces, cgroups). Most containers run Linux environments internally, meaning basic file manipulation, process handling, and shell configuration are required.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Using tabs instead of spaces in YAML files, which causes parsing errors.
* **Troubleshooting**: Use a YAML validator (like yaml-lint) to verify indentation if configuration loads fail.

## Best Practices & Tips
* Always specify YAML keys in lowercase and keep indentation to 2 spaces.

---

## Summary & Cheat Sheet
| Concept | Key Command/Feature |
|---|---|
| Indentation | Spaces only (typically 2) |
| Comments | Prefixed with `#` |

---

## References & Further Reading
* YAML Spec (yaml.org).
