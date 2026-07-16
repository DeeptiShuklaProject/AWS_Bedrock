# Module 13 - Docker Security & Hardening

## Learning Objectives
* Learn to secure containers, run rootless containers, configure read-only root filesystems, handle secrets, and scan for vulnerabilities.

## Prerequisites
* **Prerequisites**: Module 12

---

## Detailed Explanation
### 1. Rootless Containers
Running the Docker daemon in "Rootless Mode" runs both the daemon and containers as a regular user, mitigating root privilege escalation vulnerabilities.

### 2. Read-Only Filesystems
Prevent hackers from installing malicious software or editing configuration files by mounting the container filesystem as read-only.
* **Command**: `docker run --read-only nginx`
* **Handling temp files**: Use `tmpfs` mounts to allow writing to transient folders like `/tmp` or `/var/run`.

### 3. Secrets Management
Never write passwords, API keys, or SSL keys into Dockerfiles or check them into git.
* **Runtime configurations**: Pass secrets using environment variables during container run (`-e MY_SECRET=xyz`), or use Docker Secrets (Swarm) / Kubernetes Secrets.

### 4. Vulnerability Scanning
Scan container images for known Common Vulnerabilities and Exposures (CVEs).
* **Command**: `docker scout cves <image-name>` or `trivy image <image-name>`

---

## Hands-on Exercise
### Hands-on Exercise: Run a container with read-only root
Start Nginx with a read-only filesystem and check if you can write files:
```bash
docker run --read-only --tmpfs /var/cache/nginx --tmpfs /var/run -d -p 8080:80 nginx
```

## Assignment
Configure Trivy in your terminal and perform a full vulnerability scan on an old Node.js base image.

---

## Quiz

### Q1: Which tool is built into modern Docker CLI to inspect image vulnerabilities?
- trivy
- docker scout
- docker scan
- clair

*Answer*: **docker scout**

### Q2: What flag mounts the container filesystem as read-only?
- --read-only
- -ro
- --immutable
- -d

*Answer*: **--read-only**

---

## Interview Preparation

### Q: Why is hardcoding credentials inside a Dockerfile bad, and how do you fix it?
*Answer*: Hardcoded credentials become baked into the public/private image layers, making them visible to anyone with access to the image. They must be injected at runtime using environment variables, secrets managers, or configuration files.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Running containers with the dangerous `--privileged` flag, which grants root access to all host devices.
* **Troubleshooting**: If read-only mounts crash Nginx, ensure you have allocated writeable `tmpfs` directories to cached folders.

## Best Practices & Tips
* Regularly scan production images for CVE updates and rebuild images using base patches.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker scout cves <image>` | Scan image for vulnerabilities |
| `docker run --read-only` | Prevent writing to root filesystem |
| `docker run --cap-drop=ALL` | Drop all Linux capabilities |

---

## References & Further Reading
* Docker Security Guide (docs.docker.com/engine/security/).
