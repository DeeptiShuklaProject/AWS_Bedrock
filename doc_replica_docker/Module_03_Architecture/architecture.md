# Module 3 - Docker Architecture & Internals

## Learning Objectives
* Understand the Docker Daemon, Client, Registries, containerd, runc, Namespaces, Control Groups (cgroups), and Union File System.

## Prerequisites
* **Prerequisites**: Module 2

---

## Detailed Explanation
### High-Level Architecture
Docker uses a client-server architecture. The Docker Client talks to the Docker Daemon, which does the heavy lifting of building, running, and distributing containers.

```
+---------------------------------------------------------------+
|                        Docker Host                            |
|                                                               |
|   +----------------+           +--------------------------+   |
|   |  Docker Client | --------> |      Docker Daemon       |   |
|   |  (CLI Command) |  REST API |      (dockerd)           |   |
|   +----------------+           +--------------------------+   |
|                                             |                 |
|                                             v                 |
|                                +--------------------------+   |
|                                |        containerd        |   |
|                                +--------------------------+   |
|                                             |                 |
|                                             v                 |
|                                +--------------------------+   |
|                                |           runc           |   |
|                                +--------------------------+   |
+---------------------------------------------------------------+
```

### Key Components
1. **Docker Client (`docker`)**: The CLI tool used by users to interact with the daemon.
2. **Docker Daemon (`dockerd`)**: A background service that manages Docker objects.
3. **containerd**: An industry-standard container runtime that manages the container lifecycle (start, stop, pause, destroy).
4. **runc**: A lightweight CLI tool for spawning containers according to OCI specifications.
5. **Namespaces**: Provide process-level isolation (PID, NET, IPC, MNT, UTS, USER).
6. **Control Groups (cgroups)**: Resource limiting and accounting (CPU, Memory, Disk I/O).
7. **Union File System (UnionFS)**: Layered file system where layers are stacked together to appear as a single file system.

---

## Hands-on Exercise
### Hands-on Exercise: Inspect system namespaces
List namespaces on your host system:
```bash
lsns
```

## Assignment
Investigate Docker daemon processes on your system using `ps aux | grep docker`.

---

## Quiz

### Q1: Which component is responsible for resource limitation?
- Namespaces
- cgroups
- UnionFS
- runc

*Answer*: **cgroups**

### Q2: What communication protocol is used between the Client and Daemon?
- REST API over UNIX Sockets or HTTP
- GraphQL
- SSH
- gRPC only

*Answer*: **REST API over UNIX Sockets or HTTP**

---

## Interview Preparation

### Q: How does Docker achieve container isolation?
*Answer*: By using Linux kernel features: Namespaces for process/network isolation, and Control Groups (cgroups) for resource allocation and limitations.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Running containers as root inside the container without mapping them to a user namespace.
* **Troubleshooting**: If commands fail with 'Cannot connect to the Docker daemon', verify that the docker service is active (`systemctl status docker`).

## Best Practices & Tips
* Configure dockerd to restrict socket access to authorized users only.

---

## Summary & Cheat Sheet
| Component | Purpose |
|---|---|
| `dockerd` | Daemon managing resources |
| `containerd` | Runtime manager |
| `runc` | Low level OCI runner |

---

## References & Further Reading
* Moby Project (mobyproject.org), OCI runtime-spec.
