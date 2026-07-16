# Module 8 - Deep Dive: Storage, Networks & Drivers

## Learning Objectives
* Understand storage drivers, volume mapping, network modes (bridge, host, none, overlay), and custom bridge networks.

## Prerequisites
* **Prerequisites**: Module 7

---

## Detailed Explanation
### 1. Storage Drivers
Docker uses storage drivers to manage the stack layers of images and writeable container filesystems.
Popular storage drivers:
* **Overlay2**: The default and recommended driver for modern Linux distributions. It uses overlay mount techniques to stack filesystems.
* **Btrfs / ZFS**: Copy-on-Write filesystems used for specific enterprise backend requirements.

### 2. Volumes vs Bind Mounts
* **Volumes**: Managed entirely by Docker, stored in a protected path on host (`/var/lib/docker/volumes/`). Recommended for databases.
* **Bind Mounts**: Maps any arbitrary folder on the host system to the container path. Best for local development.

```
+-----------------------------------------------------------+
|                        Docker Host                        |
|                                                           |
|  +--------------------+        +-----------------------+  |
|  |     Container      |        |       Container       |  |
|  |      Volume        |        |      Bind Mount       |  |
|  +---------+----------+        +-----------+-----------+  |
|            |                               |              |
|            v                               v              |
|   /var/lib/docker/volumes/        /users/nishu/workspace/ |
|   (Managed by Docker)             (Any Host Directory)    |
+-----------------------------------------------------------+
```

### 3. Network Modes
* **Bridge (default)**: Creates a private network space on the host. Containers get local IPs and can talk to each other if on the same bridge.
* **Host**: Removes network isolation. Container shares the host's ports directly.
* **None**: Disables networking entirely.
* **Overlay**: Connects multiple Docker daemons together (Swarm mode).

---

## Hands-on Exercise
### Hands-on Exercise: Create a custom bridge network
Create a custom bridge network and connect two containers to it:
```bash
docker network create my-bridge
docker run -d --name web --network my-bridge nginx
docker run -it --name client --network my-bridge alpine ping -c 3 web
```

## Assignment
Create a persistent database container using PostgreSQL and map its data directory to a named volume.

---

## Quiz

### Q1: Which network mode exposes the container ports directly on the host interface?
- bridge
- host
- none
- overlay

*Answer*: **host**

### Q2: Where does Docker store managed volumes on a Linux host?
- /var/lib/docker/volumes/
- /etc/docker/volumes/
- /tmp/volumes/
- /home/docker/

*Answer*: **/var/lib/docker/volumes/**

---

## Interview Preparation

### Q: What is the advantage of using a User-Defined Bridge network over the Default Bridge network?
*Answer*: User-defined bridge networks provide automatic DNS resolution (containers can look up each other by container name) and better isolation, whereas the default bridge requires legacy linking or IP mapping.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Using bind mounts in production environments with absolute host paths that do not exist on the production servers.
* **Troubleshooting**: If containers cannot resolve DNS names, verify the Docker network driver parameters and inspect `/etc/resolv.conf` within the container.

## Best Practices & Tips
* Use named volumes for application database persistence and bind mounts only for codebase sharing in development.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker volume create <name>` | Create a named volume |
| `docker network ls` | List available networks |
| `docker network inspect <net>` | Show subnet details and connected containers |

---

## References & Further Reading
* Docker Networking Guide (docs.docker.com/network/).
