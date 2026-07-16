# Module 23 - FAQs & Common Confusions

## Learning Objectives
* Resolve common confusions about Docker, licenses, virtual machines, and databases.

## Prerequisites
* **Prerequisites**: None

---

## Detailed Explanation
### Q: Is Docker free for commercial use?
**A**: Docker Engine is free and open-source. However, **Docker Desktop** requires a paid subscription for commercial use in large organizations (more than 250 employees or $10 million in annual revenue). Alternatives like Podman or Rancher Desktop are free.

### Q: Should I run databases inside Docker?
**A**: Yes, in development and testing. In production, running databases in containers requires careful management of volumes, high availability, backup scripts, and replica failovers. Many enterprise architectures choose managed database services (like AWS RDS) for production data instead.

### Q: Why is my image size so large?
**A**: Every instruction in a Dockerfile adds to the image size. Using a heavy base image (like full `ubuntu` or `node`) or forgetting to clean package manager caches will result in large images. Use multi-stage builds and `alpine` bases to optimize size.

### Q: How do I run GUI applications in Docker?
**A**: Docker is designed for CLI and backend services. To run GUI apps, you must map the host's X11 server socket (`/tmp/.X11-unix`) to the container, which is complex and poses security risks.

---

## Hands-on Exercise
### Hands-on Exercise: Inspect image size metadata
Find the physical disk space utilized by your local base images using `docker image ls`.

## Assignment
Write a comparison overview on the pros and cons of containerized DBs vs Cloud Managed DBs.

---

## Quiz

### Q1: Is Docker Desktop free for companies with >1000 employees?
- No, it requires a paid subscription
- Yes, completely free
- Only on Windows
- Only on Linux

*Answer*: **No, it requires a paid subscription**

### Q2: What is the best alternative to Docker Desktop for commercial environments?
- Podman / Rancher Desktop
- VirtualBox
- VMware
- Ansible

*Answer*: **Podman / Rancher Desktop**

---

## Interview Preparation

### Q: What are the architectural trade-offs of running databases in Docker containers?
*Answer*: Pros: Easy configuration and portability. Cons: Performance overhead, risk of data corruption if volumes aren't managed correctly, and complexity of configuring clustering and failover.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Exposing local database ports publicly without configuring secure database passwords.
* **Troubleshooting**: If your application database fails to start, verify if another instance is already running on the same host port.

## Best Practices & Tips
* Keep databases outside of application containers. Run databases in separate containers linked via networks, or use cloud-managed database services.

---

## Summary & Cheat Sheet
| FAQ Topic | Summary Answer |
|---|---|
| **Desktop License** | Paid for large enterprises |
| **Production DB** | Generally prefer managed cloud services |
| **Optimization** | Use multi-stage builds and alpine bases |

---

## References & Further Reading
* Docker Licensing Terms (docker.com/pricing/faq).
