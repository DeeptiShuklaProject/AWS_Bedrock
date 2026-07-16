# Module 1 - Introduction to Docker

## Learning Objectives
* Understand the history, evolution, problems solved, benefits, limitations, alternatives, market demand, and future roadmap of containerization.

## Prerequisites
* **Prerequisites**: None

---

## Detailed Explanation
### What is Docker?
Docker is an open-source platform that automates the deployment, scaling, and management of applications by using containerization. It packages an application and all its dependencies (libraries, configuration files, system tools) into a standardized unit called a **container**.

### Why was Docker created?
Before Docker, developers and system administrators faced the classic problem: *"It works on my machine!"* 

This occurred due to differences in:
1. Operating system versions
2. System libraries and dependencies
3. Environment configurations
4. Available resources (CPU/Memory)

Docker solved this by packaging the application and its entire environment together, ensuring it runs identically on any environment: development, staging, or production.

### History & Evolution
* **2013**: Docker was launched as an open-source project by Solomon Hykes during PyCon 2013. Initially, it used Linux Containers (LXC) as the default execution driver.
* **2014**: Docker released version 1.0 and introduced `libcontainer` to replace LXC, making it independent of specific platform tools.
* **2015-Present**: Docker became the industry standard. The Open Container Initiative (OCI) was formed to establish industry standards for container formats and runtimes.

### Real-World Problems Solved
* **Dependency Hell**: No more conflicting libraries between applications.
* **Slow Deployments**: Virtual machines take minutes to boot; Docker containers start in milliseconds.
* **Resource Inefficiency**: Virtual machines require dedicated guest OS allocations, wasting memory. Containers share the host kernel, utilizing minimal resources.

### Alternatives
* **Podman**: A daemonless container engine by Red Hat.
* **LXC/LXD**: System-level containerization.
* **containerd/CRI-O**: Low-level container runtimes.

### Visual Diagram: VM vs Container
```
+---------------------------+     +---------------------------+
|      Virtual Machines     |     |          Containers       |
+---------------------------+     +---------------------------+
|  App A  |  App B  | App C |     |  App A  |  App B  | App C |
+---------+---------+-------+     +---------+---------+-------+
| Guest OS| Guest OS|GuestOS|     | Libs/Bin| Libs/Bin|Libs/Bin|
+---------+---------+-------+     +---------+---------+-------+
|  Hypervisor (e.g. ESXi)  |     |      Docker Daemon        |
+---------------------------+     +---------------------------+
|         Host OS           |     |         Host OS           |
+---------------------------+     +---------------------------+
|      Physical Server      |     |      Physical Server      |
+---------------------------+     +---------------------------+
```

---

## Hands-on Exercise
### Hands-on Exercise: Verify Docker Installation
Run the following commands to check your Docker version and verify that the daemon is active:
```bash
docker --version
docker info
```

## Assignment
Write a short essay comparing a shipping container analogy to Docker containers.

---

## Quiz

### Q1: Who founded the Docker project?
- Solomon Hykes
- Linus Torvalds
- Steve Jobs
- Guido van Rossum

*Answer*: **Solomon Hykes**

### Q2: What is the primary benefit of containerization over VMs?
- Containers include a guest OS
- Containers share the host OS kernel and are lightweight
- Containers are slower but safer
- Containers only run on Windows

*Answer*: **Containers share the host OS kernel and are lightweight**

---

## Interview Preparation

### Q: What is the 'It works on my machine' problem, and how does Docker solve it?
*Answer*: It occurs due to differences in OS and dependencies. Docker solves it by packaging the app and all its dependencies into an immutable container image that runs identically everywhere.

### Q: Compare Virtual Machines and Docker Containers.
*Answer*: VMs virtualize hardware, requiring a full guest OS, which is heavy and slow. Containers virtualize the OS kernel, sharing it among apps, making them lightweight and starting in milliseconds.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Trying to run virtual machines inside Docker containers, or expecting Docker to replace full OS virtualization requirements.
* **Troubleshooting**: If Docker isn't starting, check if virtualization (VT-x/AMD-V) is enabled in your system's BIOS/UEFI.

## Best Practices & Tips
* Keep your containers single-purpose. Run only one main process per container.

---

## Summary & Cheat Sheet
| Command | Description |
|---|---|
| `docker --version` | Shows the Docker version |
| `docker info` | Displays system-wide information |

---

## References & Further Reading
* Docker Documentation (docs.docker.com), OCI Standards (opencontainers.org).
