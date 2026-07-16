import os
import json

# Target folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Course modules structure and definitions
modules = [
    {
        "num": 1,
        "name": "Introduction",
        "file": "introduction.md",
        "title": "Module 1 - Introduction to Docker",
        "objectives": "Understand the history, evolution, problems solved, benefits, limitations, alternatives, market demand, and future roadmap of containerization.",
        "prereqs": "None",
        "explanation": """### What is Docker?
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
```""",
        "diagram": """VMs vs Containers Architecture Diagram (shown above)""",
        "exercises": """### Hands-on Exercise: Verify Docker Installation
Run the following commands to check your Docker version and verify that the daemon is active:
```bash
docker --version
docker info
```""",
        "assignment": "Write a short essay comparing a shipping container analogy to Docker containers.",
        "quiz": [
            {"q": "Who founded the Docker project?", "options": ["Solomon Hykes", "Linus Torvalds", "Steve Jobs", "Guido van Rossum"], "a": "Solomon Hykes"},
            {"q": "What is the primary benefit of containerization over VMs?", "options": ["Containers include a guest OS", "Containers share the host OS kernel and are lightweight", "Containers are slower but safer", "Containers only run on Windows"], "a": "Containers share the host OS kernel and are lightweight"}
        ],
        "interview": [
            {"q": "What is the 'It works on my machine' problem, and how does Docker solve it?", "a": "It occurs due to differences in OS and dependencies. Docker solves it by packaging the app and all its dependencies into an immutable container image that runs identically everywhere."},
            {"q": "Compare Virtual Machines and Docker Containers.", "a": "VMs virtualize hardware, requiring a full guest OS, which is heavy and slow. Containers virtualize the OS kernel, sharing it among apps, making them lightweight and starting in milliseconds."}
        ],
        "mistakes": "Trying to run virtual machines inside Docker containers, or expecting Docker to replace full OS virtualization requirements.",
        "troubleshooting": "If Docker isn't starting, check if virtualization (VT-x/AMD-V) is enabled in your system's BIOS/UEFI.",
        "best_practices": "Keep your containers single-purpose. Run only one main process per container.",
        "cheat_sheet": "| Command | Description |\n|---|---|\n| `docker --version` | Shows the Docker version |\n| `docker info` | Displays system-wide information |",
        "references": "Docker Documentation (docs.docker.com), OCI Standards (opencontainers.org)."
    },
    {
        "num": 2,
        "name": "Fundamentals",
        "file": "fundamentals.md",
        "title": "Module 2 - Docker Fundamentals",
        "objectives": "Learn the core concepts of Docker: Images, Containers, Registries, and the difference between Images and Containers.",
        "prereqs": "Module 1",
        "explanation": """### The Core Concepts
1. **Docker Image**: A read-only template containing instructions for creating a Docker container. Think of it as a class in OOP, or a blueprint.
2. **Docker Container**: A runnable instance of a Docker image. Think of it as an object/instance in OOP.
3. **Docker Registry**: A storage and distribution system for Docker images (e.g., Docker Hub, Amazon ECR).

### Analogy: Baking a Cake
* **Recipe**: The Dockerfile
* **Cake Mix / Blueprint**: The Docker Image
* **The Baked Cake**: The Docker Container
* **Baking Recipe Book Store**: The Docker Registry

### How They Work Together
```
+---------------+     Build     +--------------+     Run     +-------------------+
|  Dockerfile   | ------------> | Docker Image | ----------> |  Docker Container |
+---------------+               +--------------+             +-------------------+
                                       |
                                       | Push / Pull
                                       v
                               +----------------+
                               | Docker Registry|
                               +----------------+
```""",
        "diagram": "The Docker Lifecycle Diagram (shown above)",
        "exercises": """### Hands-on Exercise: Run your first container
Run the classic hello-world container:
```bash
docker run hello-world
```""",
        "assignment": "Pull the 'ubuntu' image and run an interactive shell inside it.",
        "quiz": [
            {"q": "What is a Docker image?", "options": ["A running application instance", "A read-only blueprint template", "A database engine", "A virtual machine monitor"], "a": "A read-only blueprint template"},
            {"q": "Which command runs a container from an image?", "options": ["docker build", "docker push", "docker run", "docker create"], "a": "docker run"}
        ],
        "interview": [
            {"q": "What is the difference between an Image and a Container?", "a": "An image is a read-only blueprint template. A container is a running, writable instance instantiated from that image."}
        ],
        "mistakes": "Modifying a container's filesystem and expecting those changes to persist inside the image automatically.",
        "troubleshooting": "If an image fails to pull, check your internet connection and ensure your registry DNS is resolvable.",
        "best_practices": "Always version your images. Avoid using the 'latest' tag in production environments.",
        "cheat_sheet": "| Command | Description |\n|---|---|\n| `docker run <image>` | Runs a container from an image |\n| `docker images` | Lists all local images |",
        "references": "Docker Image Specification (github.com/moby/moby)."
    },
    {
        "num": 3,
        "name": "Architecture",
        "file": "architecture.md",
        "title": "Module 3 - Docker Architecture & Internals",
        "objectives": "Understand the Docker Daemon, Client, Registries, containerd, runc, Namespaces, Control Groups (cgroups), and Union File System.",
        "prereqs": "Module 2",
        "explanation": """### High-Level Architecture
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
7. **Union File System (UnionFS)**: Layered file system where layers are stacked together to appear as a single file system.""",
        "diagram": "Client-Server Architecture Flow (shown above)",
        "exercises": """### Hands-on Exercise: Inspect system namespaces
List namespaces on your host system:
```bash
lsns
```""",
        "assignment": "Investigate Docker daemon processes on your system using `ps aux | grep docker`.",
        "quiz": [
            {"q": "Which component is responsible for resource limitation?", "options": ["Namespaces", "cgroups", "UnionFS", "runc"], "a": "cgroups"},
            {"q": "What communication protocol is used between the Client and Daemon?", "options": ["REST API over UNIX Sockets or HTTP", "GraphQL", "SSH", "gRPC only"], "a": "REST API over UNIX Sockets or HTTP"}
        ],
        "interview": [
            {"q": "How does Docker achieve container isolation?", "a": "By using Linux kernel features: Namespaces for process/network isolation, and Control Groups (cgroups) for resource allocation and limitations."}
        ],
        "mistakes": "Running containers as root inside the container without mapping them to a user namespace.",
        "troubleshooting": "If commands fail with 'Cannot connect to the Docker daemon', verify that the docker service is active (`systemctl status docker`).",
        "best_practices": "Configure dockerd to restrict socket access to authorized users only.",
        "cheat_sheet": "| Component | Purpose |\n|---|---|\n| `dockerd` | Daemon managing resources |\n| `containerd` | Runtime manager |\n| `runc` | Low level OCI runner |",
        "references": "Moby Project (mobyproject.org), OCI runtime-spec."
    },
    {
        "num": 4,
        "name": "Prerequisites",
        "file": "prerequisites.md",
        "title": "Module 4 - Prerequisites",
        "objectives": "Learn the essential concepts required before working with Docker: Linux CLI, Networking basics, and YAML formatting.",
        "prereqs": "None",
        "explanation": """### 1. The Linux Command Line
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
```""",
        "diagram": "YAML Structure Tree",
        "exercises": """### Hands-on Exercise: Write a YAML configuration
Create a YAML file named `test.yaml` containing settings for a simulated app stack and validate it.""",
        "assignment": "Write a bash script that starts a script, prints environmental variables, and exits.",
        "quiz": [
            {"q": "Which character represents a list item in YAML?", "options": ["-", "#", "*", "&"], "a": "-"},
            {"q": "What port is typically used for HTTPS?", "options": ["80", "443", "8080", "22"], "a": "443"}
        ],
        "interview": [
            {"q": "Why is Linux shell knowledge critical for Docker?", "a": "Docker is based on Linux kernel primitives (namespaces, cgroups). Most containers run Linux environments internally, meaning basic file manipulation, process handling, and shell configuration are required."}
        ],
        "mistakes": "Using tabs instead of spaces in YAML files, which causes parsing errors.",
        "troubleshooting": "Use a YAML validator (like yaml-lint) to verify indentation if configuration loads fail.",
        "best_practices": "Always specify YAML keys in lowercase and keep indentation to 2 spaces.",
        "cheat_sheet": "| Concept | Key Command/Feature |\n|---|---|\n| Indentation | Spaces only (typically 2) |\n| Comments | Prefixed with `#` |",
        "references": "YAML Spec (yaml.org)."
    },
    {
        "num": 5,
        "name": "Environment Setup",
        "file": "setup.md",
        "title": "Module 5 - Environment Setup",
        "objectives": "Install Docker Desktop, verify the installation, configure environment variables, and verify configuration status.",
        "prereqs": "Module 4",
        "explanation": """### Hardware & Software Requirements
* **Windows**: Windows 10/11 64-bit with WSL 2 enabled, VT-x/AMD-V virtualization enabled in BIOS.
* **macOS**: Apple Silicon (M1/M2/M3) or Intel processor, macOS 11+.
* **Linux**: Ubuntu/Debian/CentOS/RHEL, 64-bit kernel with systemd support.

### Installing Docker Desktop (Windows/macOS)
1. Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
2. Run installer and check "Use WSL 2 instead of Hyper-V" (on Windows).
3. Restart computer.
4. Launch Docker Desktop and accept the subscription service agreement.

### Installing Docker Engine (Ubuntu Linux CLI)
```bash
# Update package database
sudo apt-get update

# Install certificates and cURL
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```""",
        "diagram": "Docker Desktop vs WSL 2 Architecture Block",
        "exercises": """### Hands-on Exercise: Run verification check
Execute the diagnostic script to ensure Docker is running correctly:
```bash
docker run --rm hello-world
```""",
        "assignment": "Add your local user to the 'docker' group on Linux to run docker commands without sudo.",
        "quiz": [
            {"q": "Which backend virtualizer does Windows recommend for Docker Desktop?", "options": ["WSL 2", "VirtualBox", "VMware Workstation", "Hyper-V legacy only"], "a": "WSL 2"},
            {"q": "Which command checks system information for Docker?", "options": ["docker info", "docker status", "docker diagnostic", "docker print"], "a": "docker info"}
        ],
        "interview": [
            {"q": "Why do we add a user to the 'docker' group in Linux?", "a": "The Docker daemon binds to a UNIX socket owned by root. By adding the user to the docker group, we grant access to run docker commands without typing 'sudo'."}
        ],
        "mistakes": "Forgetting to enable hardware virtualization in BIOS before launching WSL 2 or Docker Desktop.",
        "troubleshooting": "If Docker Desktop hangs on startup, restart the WSL 2 subsystem by running `wsl --shutdown` in PowerShell.",
        "best_practices": "Set memory and CPU limits inside Docker Desktop settings to avoid freezing your host system during heavy builds.",
        "cheat_sheet": "| Command | Purpose |\n|---|---|\n| `docker info` | Inspect engine logs/status |\n| `docker version` | Output version details |",
        "references": "Docker Installation Guide (docs.docker.com/engine/install/)."
    },
    {
        "num": 6,
        "name": "Configuration",
        "file": "configuration.md",
        "title": "Module 6 - Configuration & daemon.json",
        "objectives": "Configure the Docker Daemon using daemon.json, set up environment variables, and manage configuration profiles.",
        "prereqs": "Module 5",
        "explanation": """### The daemon.json File
The Docker daemon can be configured globally using a JSON file called `daemon.json`. 
* **Location (Linux)**: `/etc/docker/daemon.json`
* **Location (Windows)**: `C:\\ProgramData\\docker\\config\\daemon.json`

### Example Configuration:
```json
{
  "debug": true,
  "metrics-addr": "127.0.0.1:9323",
  "experimental": false,
  "insecure-registries": [],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Environmental Configuration
Docker CLI can be configured using environment variables:
* `DOCKER_HOST`: Connection string for a remote daemon (e.g. `tcp://192.168.1.50:2376`).
* `DOCKER_TLS_VERIFY`: Enable TLS authentication for remote daemons.
* `DOCKER_CERT_PATH`: Directory containing security certificates.""",
        "diagram": "Docker Daemon Configuration Routing",
        "exercises": """### Hands-on Exercise: Configure log rotation
Create or modify your local `/etc/docker/daemon.json` to include log-driver size limits to prevent hard drive exhaustion.""",
        "assignment": "Configure the Docker CLI to connect to a remote Docker instance running on a virtual machine.",
        "quiz": [
            {"q": "Where is the default location for daemon.json in Linux?", "options": ["/etc/docker/daemon.json", "/var/lib/docker/daemon.json", "/usr/bin/daemon.json", "/etc/daemon.json"], "a": "/etc/docker/daemon.json"},
            {"q": "Which env variable points Docker CLI to a remote daemon socket?", "options": ["DOCKER_HOST", "DOCKER_DAEMON", "DOCKER_REMOTE", "DOCKER_SOCKET"], "a": "DOCKER_HOST"}
        ],
        "interview": [
            {"q": "How can you restrict container logs from filling up the entire server disk?", "a": "By configuring log rotation limits inside `daemon.json` under the 'log-opts' key, setting 'max-size' (e.g., '10m') and 'max-file' limit parameters."}
        ],
        "mistakes": "Typing malformed JSON (missing commas or unclosed brackets) in `daemon.json`, which prevents the daemon from starting.",
        "troubleshooting": "Run `journalctl -u docker` to view daemon startup logs if dockerd fails to reload after modifying config files.",
        "best_practices": "Always validate the JSON configuration before restarting the Docker service.",
        "cheat_sheet": "| Settings Key | Value | Description |\n|---|---|---|\n| `debug` | `true/false` | Toggles debug mode logs |\n| `log-driver` | `\"json-file\"` | Sets default logs format |",
        "references": "Docker Daemon Reference (docs.docker.com/engine/reference/commandline/dockerd)."
    },
    {
        "num": 7,
        "name": "Core Concepts",
        "file": "core_concepts.md",
        "title": "Module 7 - Core Concepts",
        "objectives": "Learn to manage the lifecycle of Docker containers, understand container states, image layers, and key CLI utilities.",
        "prereqs": "Module 6",
        "explanation": """### Container Lifecycle States
A container transitions through several states in its lifecycle:

```
                  +-----------+
                  |  Created  |
                  +-----------+
                        |
                        v   Start / Run
                  +-----------+
      +---------> |  Running  | <---------+
      |           +-----------+           |
      |                 |                 |
      | Restart         | Stop / Kill     | Pause
      |                 v                 |
      |           +-----------+           |
      +---------- |  Stopped  |           |
                  +-----------+           |
                        |                 v
                        |           +-----------+
                        |           |  Paused   |
                        |           +-----------+
                        v   Remove        | Unpause
                  +-----------+           |
                  | Destroyed | <---------+
                  +-----------+
```

### Important Commands
* **`docker run`**: Create and start a container. Combining `docker create` and `docker start`.
* **`docker stop`**: Send SIGTERM to allow graceful shutdown, followed by SIGKILL if container doesn't exit.
* **`docker kill`**: Send SIGKILL immediately to terminate processes.
* **`docker ps`**: List running containers (`-a` to list all).
* **`docker rm`**: Remove stopped containers.
* **`docker rmi`**: Delete local images.

### Understanding Image Layers
Docker images are built in layers. Every command in a Dockerfile (e.g., `RUN`, `COPY`, `ADD`) creates a new layer. Layers are read-only.
When a container is started, a thin **Writable Layer** (container layer) is added on top of the stack. All changes (writing files, deleting files) are written to this writable layer.""",
        "diagram": "Container State Transitions Flowchart (shown above)",
        "exercises": """### Hands-on Exercise: Manage container states
Create a container, pause it, inspect states, unpause, stop it, and delete it:
```bash
docker run -d --name test-nginx nginx
docker pause test-nginx
docker inspect --format='{{.State.Status}}' test-nginx
docker unpause test-nginx
docker stop test-nginx
docker rm test-nginx
```""",
        "assignment": "Write a bash script that cleans up all stopped containers and unused dangling image layers.",
        "quiz": [
            {"q": "Which signal is sent first by docker stop?", "options": ["SIGKILL", "SIGTERM", "SIGINT", "SIGHUP"], "a": "SIGTERM"},
            {"q": "What happens to data written inside a container when the container is deleted?", "options": ["Data is persisted in the image", "Data is deleted unless mapped to a volume", "Data is backed up to Docker Hub", "Data is locked"], "a": "Data is deleted unless mapped to a volume"}
        ],
        "interview": [
            {"q": "What is the difference between docker stop and docker kill?", "a": "docker stop sends SIGTERM first to allow processes to clean up and shut down gracefully, then sends SIGKILL after a timeout. docker kill sends SIGKILL immediately to stop the processes without cleanup."}
        ],
        "mistakes": "Deleting a container expecting to release storage space without removing the associated anonymous volumes.",
        "troubleshooting": "If a container fails to stop, check if it has trapped the SIGTERM signal (like some PID 1 node processes do).",
        "best_practices": "Always run containers with resource flags (`--memory`, `--cpus`) to prevent containers from monopolizing host memory.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker run -d` | Run container in background (detached) |\n| `docker ps -a` | Show running and exited containers |\n| `docker rm -f` | Force remove a running container |",
        "references": "Docker Engine CLI (docs.docker.com/engine/reference/run/)."
    },
    {
        "num": 8,
        "name": "Deep Dive",
        "file": "deep_dive.md",
        "title": "Module 8 - Deep Dive: Storage, Networks & Drivers",
        "objectives": "Understand storage drivers, volume mapping, network modes (bridge, host, none, overlay), and custom bridge networks.",
        "prereqs": "Module 7",
        "explanation": """### 1. Storage Drivers
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
* **Overlay**: Connects multiple Docker daemons together (Swarm mode).""",
        "diagram": "Volume vs Bind Mount mapping (shown above)",
        "exercises": """### Hands-on Exercise: Create a custom bridge network
Create a custom bridge network and connect two containers to it:
```bash
docker network create my-bridge
docker run -d --name web --network my-bridge nginx
docker run -it --name client --network my-bridge alpine ping -c 3 web
```""",
        "assignment": "Create a persistent database container using PostgreSQL and map its data directory to a named volume.",
        "quiz": [
            {"q": "Which network mode exposes the container ports directly on the host interface?", "options": ["bridge", "host", "none", "overlay"], "a": "host"},
            {"q": "Where does Docker store managed volumes on a Linux host?", "options": ["/var/lib/docker/volumes/", "/etc/docker/volumes/", "/tmp/volumes/", "/home/docker/"], "a": "/var/lib/docker/volumes/"}
        ],
        "interview": [
            {"q": "What is the advantage of using a User-Defined Bridge network over the Default Bridge network?", "a": "User-defined bridge networks provide automatic DNS resolution (containers can look up each other by container name) and better isolation, whereas the default bridge requires legacy linking or IP mapping."}
        ],
        "mistakes": "Using bind mounts in production environments with absolute host paths that do not exist on the production servers.",
        "troubleshooting": "If containers cannot resolve DNS names, verify the Docker network driver parameters and inspect `/etc/resolv.conf` within the container.",
        "best_practices": "Use named volumes for application database persistence and bind mounts only for codebase sharing in development.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker volume create <name>` | Create a named volume |\n| `docker network ls` | List available networks |\n| `docker network inspect <net>` | Show subnet details and connected containers |",
        "references": "Docker Networking Guide (docs.docker.com/network/)."
    },
    {
        "num": 9,
        "name": "Hands-on Labs",
        "file": "labs.md",
        "title": "Module 9 - Hands-on Labs",
        "objectives": "Build basic container solutions, run containerized applications, map ports, inspect logs, and manage configuration files.",
        "prereqs": "Module 8",
        "explanation": """### Lab 1: Interactive Alpine Container
Learn to spin up a shell and examine the environment:
```bash
docker run --name my-shell -it alpine sh
# Inside container:
uname -a
cat /etc/os-release
exit
```

### Lab 2: Nginx Web Server with Port Mapping
Run a web server in the background and expose it to the host on port 8080:
```bash
docker run -d --name my-web -p 8080:80 nginx
# Access from host browser: http://localhost:8080
```

### Lab 3: Inspect Logs and Process status
```bash
docker logs my-web
docker top my-web
docker inspect my-web
```""",
        "diagram": "Port Mapping Diagram: Host -> Container",
        "exercises": """### Hands-on Exercise: Create custom landing page
Mount a folder containing an `index.html` file into the `/usr/share/nginx/html` path of an Nginx container using a bind mount.""",
        "assignment": "Write a bash command pipeline that runs a Redis instance, populates a key, and retrieves it using `redis-cli` from inside the container.",
        "quiz": [
            {"q": "Which flag runs a container interactively with a terminal attached?", "options": ["-it", "-d", "-rm", "-p"], "a": "-it"},
            {"q": "What does -p 8080:80 mean?", "options": ["Map port 8080 on the host to port 80 in the container", "Map port 80 on the host to port 8080 in the container", "Open ports 80 and 8080 on the container", "Run container on CPU thread 80"], "a": "Map port 8080 on the host to port 80 in the container"}
        ],
        "interview": [
            {"q": "How do you check container output stdout/stderr without logging in?", "a": "By using the command `docker logs <container-id>`."}
        ],
        "mistakes": "Exposing production database containers to public internet interfaces (e.g. mapping port `0.0.0.0:5432:5432` instead of binding to localhost `127.0.0.1:5432:5432`).",
        "troubleshooting": "If port mapping fails with 'port is already allocated', find the conflicting process using `netstat` or choose another host port.",
        "best_practices": "Clean up temporary containers using the `--rm` flag to delete container filesystems automatically upon termination.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker run -it <image> <command>` | Run interactively |\n| `docker run -d -p <host>:<container> <image>` | Run detached with port mapped |\n| `docker logs <container>` | Show container logs |",
        "references": "Docker Command Reference (docs.docker.com/engine/reference/commandline/run/)."
    },
    {
        "num": 10,
        "name": "Real Projects",
        "file": "projects.md",
        "title": "Module 10 - Real-World Projects",
        "objectives": "Build multi-tier applications using custom Dockerfiles, manage multi-stage builds, and structure project layouts.",
        "prereqs": "Module 9",
        "explanation": """### Project Overview: Python Flask App with Redis Cache
We will build a simple visitor counter application. The application will use Flask (Python) as a web server, and Redis as an in-memory database to store the view counts.

### Project Directory Structure
```
flask-redis-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

### 1. `app.py`
```python
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\\n'
```

### 2. `requirements.txt`
```
flask
redis
```

### 3. `Dockerfile` (Multi-Stage Production Build)
```dockerfile
# Stage 1: Build dependencies
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```""",
        "diagram": "Flask + Redis Container Networking Map",
        "exercises": """### Hands-on Exercise: Build the project image
Build the Python Flask app image locally using:
```bash
docker build -t flask-redis-app:1.0 .
```""",
        "assignment": "Write a Docker Compose file to run both the Redis container and your Flask container on a shared custom bridge network.",
        "quiz": [
            {"q": "What is the purpose of AS builder in a Dockerfile?", "options": ["It names a build stage for multi-stage builds", "It runs the app in debug mode", "It installs dependencies", "It acts as the primary entrypoint"], "a": "It names a build stage for multi-stage builds"},
            {"q": "Which instruction exposes container ports?", "options": ["EXPOSE", "PORT", "BIND", "LISTEN"], "a": "EXPOSE"}
        ],
        "interview": [
            {"q": "Why do we use multi-stage Docker builds?", "a": "To separate build-time dependencies (like compilers, build tools, SDKs) from the final run-time image. This significantly reduces the size of the final production image and improves security."}
        ],
        "mistakes": "Copying entire development folders (including node_modules/ or virtual environments) into the build context instead of using `.dockerignore`.",
        "troubleshooting": "If your Python script fails due to missing modules, check if paths from your builder stage are correctly mapped to runtime environment paths.",
        "best_practices": "Create a `.dockerignore` file containing `.git`, `node_modules`, and local config secrets to keep build contexts clean.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker build -t <tag> .` | Build image from Dockerfile |\n| `docker history <image>` | View history of image layers |",
        "references": "Best practices for writing Dockerfiles (docs.docker.com/develop/develop-images/dockerfile_best-practices/)."
    },
    {
        "num": 11,
        "name": "Best Practices",
        "file": "best_practices.md",
        "title": "Module 11 - Docker Best Practices",
        "objectives": "Apply coding standards for Dockerfiles, clean image optimizations, caching mechanisms, and container configuration rules.",
        "prereqs": "Module 10",
        "explanation": """### 1. Optimize Image Size
* Use small base images (e.g. `alpine`, `slim`).
* Combine `RUN` instructions to reduce layer count.
* Clean package managers cache in the same layer:
  ```dockerfile
  RUN apt-get update && apt-get install -y \\
      curl \\
      && rm -rf /var/lib/apt/lists/*
  ```

### 2. leverage Build Cache
Docker builds images sequentially from top to bottom. If a layer is unchanged, Docker uses the cached version.
* **Order of commands**: Put layers that change frequently (like code modifications) at the *bottom* of your Dockerfile. Put unchanging layers (like package installations) at the *top*.

```dockerfile
# Good practice: copy package configurations first
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Then copy code
COPY . .
```

### 3. Run as Non-Root User
By default, Docker runs container processes as `root`. This poses a security risk if an attacker breaks out of the container process.
* **Solution**: Create and switch to a non-privileged user.
  ```dockerfile
  RUN groupadd -r app && useradd -r -g app app
  USER app
  ```""",
        "diagram": "Docker Layer Caching Sequence Comparison",
        "exercises": """### Hands-on Exercise: Optimize a slow Node.js Dockerfile
Refactor a provided Node.js Dockerfile to utilize layer caching for dependency installation, saving compile times.""",
        "assignment": "Inspect container image layers using `docker history` and calculate the size savings from your optimization.",
        "quiz": [
            {"q": "Which base image is generally the smallest?", "options": ["ubuntu:latest", "alpine:latest", "debian:latest", "centos:latest"], "a": "alpine:latest"},
            {"q": "What happens if you run 'COPY . .' before running package installation?", "options": ["Layer cache for dependencies breaks on any code change", "The build speed increases", "The image size decreases", "Nothing changes"], "a": "Layer cache for dependencies breaks on any code change"}
        ],
        "interview": [
            {"q": "How can you minimize the number of read-only image layers?", "a": "By combining multiple command operations into a single line using shell operators like '&&' and '\\', particularly for installing packages and purging installer caches."}
        ],
        "mistakes": "Keeping API keys or database password credentials hardcoded inside a Dockerfile's `ENV` instructions.",
        "troubleshooting": "If layer cache isn't updating after repository code changes, pass the `--no-cache` parameter during your build command.",
        "best_practices": "Always declare a specific tag for base images (e.g., `node:18.16.0-alpine`) instead of a general tag like `node:latest`.",
        "cheat_sheet": "| Practice | Action |\n|---|---|\n| Base Image | Prefer `alpine` or `slim` |\n| Layers | Chain shell commands with `&&` |\n| Security | Always define a non-root `USER` |",
        "references": "Docker Development Best Practices."
    },
    {
        "num": 12,
        "name": "Design Patterns",
        "file": "design_patterns.md",
        "title": "Module 12 - Container Design Patterns",
        "objectives": "Learn modern container design patterns: Sidecar, Ambassador, Adapter, and Init Container patterns.",
        "prereqs": "Module 11",
        "explanation": """### Single-Container vs Multi-Container Patterns
Containers should follow single-responsibility rules. Design patterns help orchestrate shared workloads:

### 1. Sidecar Pattern
A secondary container runs alongside the primary application to extend or enhance its functionality.
* **Example**: An application container writes log files to a shared volume. A sidecar container tail-reads those logs and pushes them to Elasticsearch.

### 2. Ambassador Pattern
An ambassador container acts as a local proxy for network connections to remote resources.
* **Example**: The application connects to `localhost:3306` (the local ambassador). The ambassador handles security, retry logic, and routes queries to the actual remote cloud database cluster.

### 3. Init Container Pattern
Containers that run and complete execution *before* the main application container starts.
* **Example**: A container that runs database migration scripts or waits for third-party services to become reachable.

```
Sidecar Pattern Model:
+-------------------------------------------------+
|                    Pod/Host                     |
|                                                 |
|  +--------------------+   +------------------+  |
|  | Primary Application|   | Sidecar Container|  |
|  | (Flask Web Server) |   | (Log Forwarder)  |  |
|  +---------+----------+   +--------+---------+  |
|            |                       |            |
|            +----> Shared Volume <--+            |
+-------------------------------------------------+
```""",
        "diagram": "Visual representation of Sidecar and Ambassador patterns (shown above)",
        "exercises": """### Hands-on Exercise: Implement an Init Container
Create a shell script that verifies database availability (pings db container) before launching your web application service.""",
        "assignment": "Model a log forwarder sidecar pattern on paper, defining sharing volumes and necessary networking configs.",
        "quiz": [
            {"q": "Which pattern acts as a local proxy for outgoing database queries?", "options": ["Sidecar", "Ambassador", "Adapter", "Init Container"], "a": "Ambassador"},
            {"q": "When do Init Containers run?", "options": ["Concurrently with the main app", "After the main app exits", "Before the main app container starts", "Only when the app crashes"], "a": "Before the main app container starts"}
        ],
        "interview": [
            {"q": "What is the primary benefit of the Sidecar design pattern?", "a": "It allows separation of concerns. You can update or swap out helper utilities (like logging, monitoring agents, or cert reloaders) without rebuilding or disrupting the main application container code."}
        ],
        "mistakes": "Mixing helper utilities and web application servers inside a single, bloated container process.",
        "troubleshooting": "If main containers crash because databases aren't ready, wrap start processes in health-check loop scripts.",
        "best_practices": "Ensure sidecars share host resources gracefully, setting strict CPU/Memory resource constraints for helpers.",
        "cheat_sheet": "| Pattern | Primary Use-Case |\n|---|---|\n| **Sidecar** | Logs forwarding, metrics collection |\n| **Ambassador** | Database routing, circuit breakers |\n| **Init** | Code migrations, dependency readiness checks |",
        "references": "Distributed Systems Patterns by Brendan Burns."
    },
    {
        "num": 13,
        "name": "Security",
        "file": "security.md",
        "title": "Module 13 - Docker Security & Hardening",
        "objectives": "Learn to secure containers, run rootless containers, configure read-only root filesystems, handle secrets, and scan for vulnerabilities.",
        "prereqs": "Module 12",
        "explanation": """### 1. Rootless Containers
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
* **Command**: `docker scout cves <image-name>` or `trivy image <image-name>`""",
        "diagram": "Docker Host Privilege Boundaries Diagram",
        "exercises": """### Hands-on Exercise: Run a container with read-only root
Start Nginx with a read-only filesystem and check if you can write files:
```bash
docker run --read-only --tmpfs /var/cache/nginx --tmpfs /var/run -d -p 8080:80 nginx
```""",
        "assignment": "Configure Trivy in your terminal and perform a full vulnerability scan on an old Node.js base image.",
        "quiz": [
            {"q": "Which tool is built into modern Docker CLI to inspect image vulnerabilities?", "options": ["trivy", "docker scout", "docker scan", "clair"], "a": "docker scout"},
            {"q": "What flag mounts the container filesystem as read-only?", "options": ["--read-only", "-ro", "--immutable", "-d"], "a": "--read-only"}
        ],
        "interview": [
            {"q": "Why is hardcoding credentials inside a Dockerfile bad, and how do you fix it?", "a": "Hardcoded credentials become baked into the public/private image layers, making them visible to anyone with access to the image. They must be injected at runtime using environment variables, secrets managers, or configuration files."}
        ],
        "mistakes": "Running containers with the dangerous `--privileged` flag, which grants root access to all host devices.",
        "troubleshooting": "If read-only mounts crash Nginx, ensure you have allocated writeable `tmpfs` directories to cached folders.",
        "best_practices": "Regularly scan production images for CVE updates and rebuild images using base patches.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker scout cves <image>` | Scan image for vulnerabilities |\n| `docker run --read-only` | Prevent writing to root filesystem |\n| `docker run --cap-drop=ALL` | Drop all Linux capabilities |",
        "references": "Docker Security Guide (docs.docker.com/engine/security/)."
    },
    {
        "num": 14,
        "name": "Performance",
        "file": "performance.md",
        "title": "Module 14 - Performance Optimization",
        "objectives": "Optimize resource allocations, profiles, memory configurations, CPU tuning, and caching networks.",
        "prereqs": "Module 13",
        "explanation": """### 1. Resource Limits (CPU & Memory)
By default, a container has no resource limits and can consume as much CPU/Memory as the host allows. A memory leak in one container can bring down the entire server.
* **Memory Limits**: Restrict max memory.
  `docker run -m 512m --memory-swap 512m nginx`
* **CPU Limits**: Restrict CPU cycles.
  `docker run --cpus="1.5" nginx`

### 2. Network Performance
For high-performance applications (databases, sockets), network virtualization overhead can affect latency.
* **Optimization**: Use the `host` network driver to bypass bridge virtualization. Note that port mapping conflicts must be managed manually.

### 3. Builder Cache (Docker BuildKit)
BuildKit is a next-generation build engine for Docker that runs builds in parallel, cache pipelines, and mounts compilation dependencies.
* **Enable BuildKit**: Set `DOCKER_BUILDKIT=1` in your environment.
* **Cache mounting**: Keep caches out of final layers:
  ```dockerfile
  RUN --mount=type=cache,target=/root/.npm npm install
  ```""",
        "diagram": "Bridge Network overhead vs Host Network Direct Path",
        "exercises": """### Hands-on Exercise: Set resource boundaries
Verify resource throttling by running a stress container with memory limitations:
```bash
docker run -it --rm -m 256m progrium/stress --cpu 2 --io 1 --vm 1 --vm-bytes 128M --timeout 10s
```""",
        "assignment": "Write a performance comparison summary comparing bridge network response times with host network direct connections.",
        "quiz": [
            {"q": "Which environment variable enables the BuildKit engine?", "options": ["DOCKER_BUILDKIT=1", "BUILDKIT=true", "DOCKER_FAST=1", "USE_BUILDKIT=1"], "a": "DOCKER_BUILDKIT=1"},
            {"q": "What flag restricts memory usage?", "options": ["-m", "--limit-mem", "--ram", "-c"], "a": "-m"}
        ],
        "interview": [
            {"q": "How does setting memory limits protect a host OS under high load?", "a": "It ensures that if a container experiences a memory leak, it will trigger the Linux Out-Of-Memory (OOM) killer to terminate only that container process, preventing the entire host OS from freezing."}
        ],
        "mistakes": "Setting memory limits too low, causing containers to instantly crash with Out-Of-Memory (OOM) codes during startup.",
        "troubleshooting": "Check if a container was terminated due to memory pressure by executing `docker inspect` and searching for the 'OOMKilled' attribute.",
        "best_practices": "Monitor resource footprints using `docker stats` and calibrate memory boundaries under workload simulations.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker stats` | Live stream resource usage statistics |\n| `docker run -m 512m` | Restrict memory to 512 megabytes |\n| `docker run --cpus 1` | Allocate maximum 1 CPU core |",
        "references": "Docker Performance and Runtime Constraints."
    },
    {
        "num": 15,
        "name": "Debugging",
        "file": "debugging.md",
        "title": "Module 15 - Debugging & Troubleshooting",
        "objectives": "Master container debugging utilities: exec, inspect, logs, export/import, events, and networking troubleshooting.",
        "prereqs": "Module 14",
        "explanation": """### 1. Interactive Debugging (`docker exec`)
Run a shell inside a running container to inspect config files or test connections:
```bash
docker exec -it my-container sh
```

### 2. Inspecting Metadata (`docker inspect`)
Returns low-level system configuration details in JSON format.
* **Filtering JSON output (Go templates)**:
  ```bash
  docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-container
  ```

### 3. Event Streaming (`docker events`)
Live-streams all events occurring inside the Docker engine (container starts, stops, deaths).
```bash
docker events --since '10m'
```

### 4. Copying Files (`docker cp`)
Copy files between the host system and a running container.
```bash
# Host to container
docker cp config.yaml my-container:/etc/app/config.yaml

# Container to host
docker cp my-container:/var/log/app.log ./host.log
```""",
        "diagram": "Debugging Diagnostic Flowchart",
        "exercises": """### Hands-on Exercise: Extract diagnostic logs
Use `docker inspect` to discover the exact IP address and gateway of a running Nginx container, then extract its logs.""",
        "assignment": "Troubleshoot a broken container (e.g. database configuration error) using `docker logs` and `docker inspect` to fix the env vars.",
        "quiz": [
            {"q": "Which command executes a diagnostic shell inside a running container?", "options": ["docker run", "docker exec", "docker attach", "docker debug"], "a": "docker exec"},
            {"q": "What format is outputted by docker inspect?", "options": ["YAML", "JSON", "XML", "CSV"], "a": "JSON"}
        ],
        "interview": [
            {"q": "How can you debug a container that exits immediately upon startup?", "a": "1. Run 'docker logs <container-id>' to read standard error outputs. 2. Inspect container definitions via 'docker inspect'. 3. Temporarily override the entrypoint (e.g. '--entrypoint sh') to inspect files."}
        ],
        "mistakes": "Trying to run `docker exec` on a container that has already stopped/exited.",
        "troubleshooting": "If your container crashes with no error logs, verify if your code is printing outputs to `/var/log` files instead of stdout/stderr.",
        "best_practices": "Ensure application code prints errors to stdout/stderr so that they can be easily captured by `docker logs`.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker exec -it <id> sh` | Open interactive shell inside running container |\n| `docker inspect <id>` | Show configuration details |\n| `docker cp <src> <dest>` | Copy files in/out of containers |",
        "references": "Docker Troubleshooting Guide."
    },
    {
        "num": 16,
        "name": "Testing",
        "file": "testing.md",
        "title": "Module 16 - Containerized Testing",
        "objectives": "Learn to write tests for container setups, use Docker-in-Docker, run integration testing with testcontainers, and structure QA environments.",
        "prereqs": "Module 15",
        "explanation": """### 1. Running Unit Tests in Docker
Build containers specifically for running tests, ensuring consistency between local tests and CI pipelines.
```dockerfile
# Run tests during build
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run test
```

### 2. Integration Testing with Testcontainers
**Testcontainers** is an industry-standard library that allows developers to spin up real databases (Postgres, Redis) or web systems inside temporary Docker containers during JUnit, PyTest, or Node.js tests.
* **Benefits**: No need for mocked databases or setting up shared developer database servers.

### 3. Docker-in-Docker (DinD)
Running Docker inside a Docker container. Used by CI/CD systems (like GitLab runners) to build and push images.
* **Execution**: Run with privilege flags or map the host socket `/var/run/docker.sock` to the container to control the host engine.
  ```bash
  docker run -v /var/run/docker.sock:/var/run/docker.sock docker:latest docker ps
  ```""",
        "diagram": "Docker-in-Docker Sockets Mapping Diagram",
        "exercises": """### Hands-on Exercise: Run tests inside a Node container
Write a Dockerfile that copies an app's test files, executes test suites, and exits with a non-zero code on failures.""",
        "assignment": "Write a PyTest script using testcontainers to test a connection to a running container database.",
        "quiz": [
            {"q": "What is DinD?", "options": ["Docker-in-Docker", "Docker-in-Development", "Dangling-image-Delete", "Docker-integration-Database"], "a": "Docker-in-Docker"},
            {"q": "How can a containerized tool control the host Docker daemon?", "options": ["By connecting via SSH", "By mapping /var/run/docker.sock to the container", "By using Docker Hub", "By exporting images"], "a": "By mapping /var/run/docker.sock to the container"}
        ],
        "interview": [
            {"q": "What are the risks of mapping /var/run/docker.sock to a container?", "a": "It grants the container full root control over the host's Docker daemon. If compromised, an attacker can launch privileged containers to compromise the host OS."}
        ],
        "mistakes": "Baking test code and test databases into the final production image, increasing image size and exposing vulnerabilities.",
        "troubleshooting": "If DinD builds fail, check if your host security daemon (AppArmor/SELinux) is blocking socket mounting permissions.",
        "best_practices": "Use multi-stage builds to run test suites in intermediate stages, and copy only production assets to the final stage.",
        "cheat_sheet": "| CLI Mount | Purpose |\n|---|---|\n| `-v /var/run/docker.sock:/var/run/docker.sock` | Share host docker daemon socket |",
        "references": "Testcontainers Official Guide (testcontainers.com)."
    },
    {
        "num": 17,
        "name": "Deployment",
        "file": "deployment.md",
        "title": "Module 17 - Deployment & Orchestration",
        "objectives": "Learn Docker Compose configurations, service definitions, environment integrations, and Kubernetes orchestration fundamentals.",
        "prereqs": "Module 16",
        "explanation": """### 1. Docker Compose
Docker Compose is a tool for defining and running multi-container applications. You define the configuration in a single YAML file (`docker-compose.yml`) and launch all services with a single command.

### Example `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    networks:
      - app-net

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    networks:
      - app-net

secrets:
  db_password:
    file: ./secrets/db_password.txt

networks:
  app-net:
    driver: bridge
```

### Useful Compose Commands:
* **`docker compose up -d`**: Start services in the background.
* **`docker compose down`**: Stop and remove containers, networks, and volumes.
* **`docker compose logs -f`**: Tail logs from all running services.

### 2. Transition to Orchestration (Kubernetes)
For production environments running on multiple servers, Docker Compose is insufficient. You need an orchestrator (like Kubernetes or Docker Swarm) to handle:
* High Availability (auto-restarting failed containers on different servers).
* Auto-Scaling (increasing container count based on traffic load).
* Rolling Updates (updating applications with zero downtime).""",
        "diagram": "Docker Compose Multi-Container Orchestration Model",
        "exercises": """### Hands-on Exercise: Launch a local App Stack
Write a compose file for a WordPress + MySQL stack, launch it, access the configuration UI, and tear it down.""",
        "assignment": "Configure health-checks in a docker-compose service definition to ensure dependent containers wait until the database is healthy.",
        "quiz": [
            {"q": "Which command teardown a compose stack?", "options": ["docker compose down", "docker compose stop", "docker compose delete", "docker compose remove"], "a": "docker compose down"},
            {"q": "What network configuration is created by default by Docker Compose?", "options": ["A shared custom bridge network for all services", "Individual host networks", "None network mode", "Overlay swarm network"], "a": "A shared custom bridge network for all services"}
        ],
        "interview": [
            {"q": "How does Docker Compose manage service dependencies?", "a": "By using the 'depends_on' configuration key. This starts services in the specified order, though additional health-checks are needed to ensure the target application is fully ready."}
        ],
        "mistakes": "Hardcoding credentials in `docker-compose.yml` instead of loading them from a `.env` file or external environment variables.",
        "troubleshooting": "If services fail to communicate, verify that they are declared on the same network subnet inside the compose file.",
        "best_practices": "Always declare volume paths explicitly and use named volumes for production database services.",
        "cheat_sheet": "| Command | Action |\n|---|---|\n| `docker compose up -d` | Launch all services in background |\n| `docker compose ps` | List status of services |\n| `docker compose down -v` | Stop services and purge volumes |",
        "references": "Docker Compose Spec (docs.docker.com/compose/)."
    },
    {
        "num": 18,
        "name": "CI_CD",
        "file": "cicd.md",
        "title": "Module 18 - CI/CD Integration",
        "objectives": "Build and push images using GitHub Actions pipelines, manage registry logins, cache builds, and tag releases.",
        "prereqs": "Module 17",
        "explanation": """### Container CI/CD Pipeline
In modern DevOps pipelines, every code commit automatically triggers a runner to test the code, build the Docker image, and push it to a registry.

### Example GitHub Actions Workflow (`.github/workflows/docker-publish.yml`)
```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up QEMU (for multi-platform support)
        uses: docker/setup-qemu-action@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            myusername/myapp:latest
            myusername/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Optimization: Remote Cache Storage
By configuring `cache-from` and `cache-to` with Actions Cache (`gha`), subsequent build runners will pull intermediate layers from the GitHub cache, reducing build times from minutes to seconds.""",
        "diagram": "CI/CD Pipeline Flowchart: Git Commit -> Actions -> Registry",
        "exercises": """### Hands-on Exercise: Configure GitHub Secrets
Create a public repository, save dummy login credentials in GitHub Actions Secrets, and draft a test workflow file.""",
        "assignment": "Write a pipeline configuration file for GitLab CI or Bitbucket Pipelines that executes `docker build`.",
        "quiz": [
            {"q": "What action logs in to Docker registries in GitHub Actions?", "options": ["docker/login-action", "docker/log-in", "actions/login", "auth/docker"], "a": "docker/login-action"},
            {"q": "Why should you tag images with the commit SHA in CI?", "options": ["To ensure unique, traceable tags for deployments", "To speed up compilation", "To encrypt the image", "To bypass registries"], "a": "To ensure unique, traceable tags for deployments"}
        ],
        "interview": [
            {"q": "How can you speed up Docker builds inside cloud CI/CD runners?", "a": "By using remote caching features (e.g. BuildKit's gha cache or registry caching), multi-stage builds, and choosing slim baseline images."}
        ],
        "mistakes": "Exposing Docker Hub passwords directly in pipeline YAML files instead of using Repository Secrets.",
        "troubleshooting": "If logins fail inside your pipelines, verify secret token expiration limits on Docker Hub.",
        "best_practices": "Always configure build pipelines to tag images with semantic versions or commit SHAs instead of just 'latest'.",
        "cheat_sheet": "| GitHub Action | Purpose |\n|---|---|\n| `docker/setup-buildx-action` | Enable BuildKit builders |\n| `docker/login-action` | Login to Docker Hub/ECR/GHCR |\n| `docker/build-push-action` | Compile and upload image |",
        "references": "Docker GitHub Actions (docs.docker.com/build/ci/github-actions/)."
    },
    {
        "num": 19,
        "name": "Cloud Integration",
        "file": "cloud.md",
        "title": "Module 19 - Cloud Integration (AWS)",
        "objectives": "Deploy containerized workloads to AWS, push images to Amazon ECR, configure Amazon ECS, and manage Fargate tasks.",
        "prereqs": "Module 18",
        "explanation": """### 1. Amazon ECR (Elastic Container Registry)
A secure, managed Docker registry provided by AWS.
* **Authentication CLI Command**:
  ```bash
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
  ```
* **Tagging & Pushing**:
  ```bash
  docker tag my-app:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
  docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
  ```

### 2. Amazon ECS (Elastic Container Service)
AWS's native container orchestrator. It runs containers using two launch types:
* **EC2 Launch Type**: You manage the underlying virtual machines.
* **Fargate Launch Type (Serverless)**: AWS manages the server provisioning, and you pay only for the vCPU and memory allocated to the tasks.

### 3. Deploying using Task Definitions
A Task Definition is a blueprint for your application (similar to docker-compose). It configures ports, images, environment variables, IAM roles, and logging (CloudWatch).""",
        "diagram": "AWS ECS Fargate Infrastructure Layout",
        "exercises": """### Hands-on Exercise: CLI login to ECR
Write out the command block to authenticate your local Docker daemon with an AWS ECR repository using your IAM credentials.""",
        "assignment": "Design a CloudFormation or Terraform manifest snippet that creates an ECR repository.",
        "quiz": [
            {"q": "What is AWS Fargate?", "options": ["A serverless engine to run containers without managing VMs", "An image compression utility", "A local virtual machine editor", "A database system"], "a": "A serverless engine to run containers without managing VMs"},
            {"q": "Which service stores Docker images on AWS?", "options": ["Amazon ECR", "Amazon ECS", "Amazon S3", "AWS CodeBuild"], "a": "Amazon ECR"}
        ],
        "interview": [
            {"q": "What is the difference between ECS Task Definition and an ECS Service?", "a": "A Task Definition is the blueprint detailing container images, ports, and volumes. An ECS Service handles orchestration details, keeping a specified number of task instances running and attaching them to load balancers."}
        ],
        "mistakes": "Exposing AWS IAM Access Keys inside Docker image environment files.",
        "troubleshooting": "If ECS tasks fail with 'Pending' state indefinitely, check if your VPC has Internet Gateways or NAT Gateways configuration to pull the image from ECR.",
        "best_practices": "Assign IAM roles (Task Execution Role) directly to tasks instead of granting broad permissions to EC2 host instances.",
        "cheat_sheet": "| CLI Tool | Command Purpose |\n|---|---|\n| `aws ecr` | Manage registries and authentication |\n| `docker push` | Upload image to remote ECR URL |",
        "references": "AWS ECS Developer Guide."
    },
    {
        "num": 20,
        "name": "Industry Architecture",
        "file": "industry_architecture.md",
        "title": "Module 20 - Industry Architecture",
        "objectives": "Learn microservice integration patterns, container logging, shared network topologies, and domain segmentation.",
        "prereqs": "Module 19",
        "explanation": """### Container Microservice Architectures
In modern production environments, monolithic systems are refactored into microservices. Docker facilitates this by keeping environments decoupled.

```
                  +--------------------------------+
                  |         Load Balancer          |
                  |         (Nginx Proxy)          |
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  User Service Container|                   | Order Service Container|
|     (NodeJS App)      |                   |      (Python App)     |
+-----------+-----------+                   +-----------+-----------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  User Database (pg)   |                   |  Order Database (pg)  |
|       (Volume)        |                   |       (Volume)        |
+-----------------------+                   +-----------------------+
```

### Architectural Rules
1. **Database-per-service**: Microservices must not access each other's databases directly. They communicate via APIs (REST/gRPC).
2. **Centralized Logging**: Containers dump logs to stdout. An external collector (FluentBit, Logstash) aggregates these and forwards them to logs systems (Elasticsearch, Loki).
3. **Stateless Services**: Web containers must not store local files. Session data must be shared in Redis, and user files stored in S3.""",
        "diagram": "Microservices Integration Pattern (shown above)",
        "exercises": """### Hands-on Exercise: Map service dependencies
Design a network bridge layout separating customer service containers from backend analytics databases.""",
        "assignment": "Write an architectural plan migrating a monolithic Django web server into separate Django-API and React-frontend containers.",
        "quiz": [
            {"q": "What is the database-per-service pattern?", "options": ["Each microservice has its own isolated database", "All containers write to one database table", "Containers use flat JSON files for persistence", "No database is permitted"], "a": "Each microservice has its own isolated database"},
            {"q": "Where should container logs be directed in production?", "options": ["Stdout and Stderr", "Local log files only", "Host /var/log directory only", "Database rows"], "a": "Stdout and Stderr"}
        ],
        "interview": [
            {"q": "Why are stateless containers crucial for auto-scaling?", "a": "Stateless containers can be created or destroyed instantly without risking data loss, allowing orchestrators to scale instances up or down based on resource usage."}
        ],
        "mistakes": "Connecting all microservices to a single shared database instance, recreating a monolithic architecture.",
        "troubleshooting": "If services experience high latency, verify DNS routing overheads and check network driver limits.",
        "best_practices": "Store all user files outside container filesystems on cloud object storages (S3).",
        "cheat_sheet": "| Component | Purpose |\n|---|---|\n| Stateless | Store no sessions/files locally |\n| Logging | Write output to stdout/stderr |\n| Scaling | Dynamically balance container count |",
        "references": "Microservices Patterns by Chris Richardson."
    },
    {
        "num": 21,
        "name": "Common Interview Questions",
        "file": "interview_questions.md",
        "title": "Module 21 - Common Interview Questions",
        "objectives": "Review key interview questions spanning beginner, intermediate, advanced, and scenario-based categories.",
        "prereqs": "Modules 1-20",
        "explanation": """### Beginner Questions
1. **What is a Dockerfile?**
   * *Answer*: A text document containing all the commands a user could call on the command line to assemble a Docker image.
2. **What is Docker Hub?**
   * *Answer*: A cloud-based registry service that allows you to link code repositories, build images, and test them, while hosting public or private images.

### Intermediate Questions
3. **What is a dangling image?**
   * *Answer*: An image that is no longer associated with any tagged image. They appear as `<none>:<none>` when running `docker images` and can be cleaned using `docker image prune`.
4. **How do COPY and ADD differ in a Dockerfile?**
   * *Answer*: `COPY` only copies local files from the build context into the container. `ADD` can do that too, but also supports pulling remote URLs and automatically extracting tar archives. `COPY` is preferred for safety.

### Advanced & Scenario-Based Questions
5. **How does Copy-on-Write (CoW) work in Docker storage?**
   * *Answer*: If a file in a lower image layer needs to be modified, the storage driver copies the file up to the top writable container layer before modifying it, preserving the read-only lower layer.
6. **Scenario: A container's process has PID 1 but does not respond to `docker stop`. Why?**
   * *Answer*: Linux PID 1 processes are system handlers. By default, they do not inherit default signal handlers (like SIGTERM). If the application code doesn't explicitly trap SIGTERM, it ignores it until `docker stop` times out and sends SIGKILL.""",
        "diagram": "Copy-on-Write (CoW) Stack Mechanism Diagram",
        "exercises": """### Hands-on Exercise: Simulate a PID 1 signal trap
Write a basic Node.js script, package it as PID 1, and test its termination behavior under `docker stop`.""",
        "assignment": "Write a mock interview transcript answering three scenario-based Docker questions.",
        "quiz": [
            {"q": "Which image tag represents a dangling layer?", "options": ["<none>:<none>", "latest", "dangling", "null"], "a": "<none>:<none>"},
            {"q": "Which instruction is preferred for importing local configurations?", "options": ["COPY", "ADD", "ENV", "RUN"], "a": "COPY"}
        ],
        "interview": [
            {"q": "What happens when you run out of disk space due to container logs?", "a": "The Docker daemon cannot write container operations, causing systems to fail. I resolve this by configuring log rotation limiters (max-size/max-file) in daemon.json."}
        ],
        "mistakes": "Providing vague answers about containerization without explaining the underlying Linux primitives (namespaces, cgroups).",
        "troubleshooting": "Use `docker system df` to analyze which resource (containers, images, volumes) is exhausting local storage.",
        "best_practices": "Structure your answers using the STAR method (Situation, Task, Action, Result) for scenario-based questions.",
        "cheat_sheet": "| Topic | Key Concept |\n|---|---|\n| **Lighter images** | Multi-stage builds, alpine base |\n| **Signals** | PID 1 needs signal trapping |\n| **Persistence** | Volumes vs Bind Mounts |",
        "references": "Technical Interview Prep Guides."
    },
    {
        "num": 22,
        "name": "Cheat Sheets",
        "file": "cheat_sheets.md",
        "title": "Module 22 - Cheat Sheets & Reference Guides",
        "objectives": "A quick reference guide for essential Docker commands, operations, and file formats.",
        "prereqs": "None",
        "explanation": """### Container Management
```bash
docker run -d -p 80:80 --name web nginx   # Run detached web container
docker ps -a                              # List all local containers
docker stop my-container                  # Stop container (SIGTERM)
docker kill my-container                  # Kill container (SIGKILL)
docker rm my-container                    # Delete container
docker logs -f my-container               # Tail container logs
```

### Image Management
```bash
docker build -t my-image:1.0 .            # Build image
docker images                             # List local images
docker rmi my-image:1.0                   # Remove image
docker history my-image:1.0               # Inspect image layers
docker tag local:tag remote:tag           # Retag image
docker push remote:tag                    # Push to registry
```

### Cleanup
```bash
docker system prune                       # Delete stopped containers and unused networks
docker system prune -a --volumes          # Deep purge: deletes all unused images, volumes, and networks
docker image prune                        # Remove dangling images
```

### Troubleshooting
```bash
docker inspect my-container               # Output config JSON
docker exec -it my-container sh           # Launch shell in container
docker stats                              # Live resource metrics
```""",
        "diagram": "Docker CLI Command Cheat Sheet Mind Map",
        "exercises": """### Hands-on Exercise: Clean up local systems
Run a complete cleanup pipeline using prune commands to verify disk space recovery:
```bash
docker system df
docker system prune -f
```""",
        "assignment": "Design a printed cheat sheet layout summarizing container state commands.",
        "quiz": [
            {"q": "Which flag deletes volumes during a system prune?", "options": ["--volumes", "-v", "--all", "-f"], "a": "--volumes"},
            {"q": "Which command displays container resource usage statistics?", "options": ["docker stats", "docker top", "docker inspect", "docker monitor"], "a": "docker stats"}
        ],
        "interview": [
            {"q": "How can you completely clear out all cached image layers and volumes in development?", "a": "By executing 'docker system prune -a --volumes' to wipe all stopped containers, unused networks, images, and volumes."}
        ],
        "mistakes": "Running `docker system prune -a` in production environments, which can delete cache layers used by active rollback systems.",
        "troubleshooting": "If docker prune commands freeze, restart the docker service to release file locks.",
        "best_practices": "Keep a printout or digital bookmark of core CLI commands for easy lookup.",
        "cheat_sheet": "| Command Category | Core Utility |\n|---|---|\n| **Lifecycle** | `run`, `stop`, `rm` |\n| **Diagnostic** | `logs`, `inspect`, `stats` |\n| **Pruning** | `system prune` |",
        "references": "Docker CLI Cheat Sheet."
    },
    {
        "num": 23,
        "name": "FAQs",
        "file": "faqs.md",
        "title": "Module 23 - FAQs & Common Confusions",
        "objectives": "Resolve common confusions about Docker, licenses, virtual machines, and databases.",
        "prereqs": "None",
        "explanation": """### Q: Is Docker free for commercial use?
**A**: Docker Engine is free and open-source. However, **Docker Desktop** requires a paid subscription for commercial use in large organizations (more than 250 employees or $10 million in annual revenue). Alternatives like Podman or Rancher Desktop are free.

### Q: Should I run databases inside Docker?
**A**: Yes, in development and testing. In production, running databases in containers requires careful management of volumes, high availability, backup scripts, and replica failovers. Many enterprise architectures choose managed database services (like AWS RDS) for production data instead.

### Q: Why is my image size so large?
**A**: Every instruction in a Dockerfile adds to the image size. Using a heavy base image (like full `ubuntu` or `node`) or forgetting to clean package manager caches will result in large images. Use multi-stage builds and `alpine` bases to optimize size.

### Q: How do I run GUI applications in Docker?
**A**: Docker is designed for CLI and backend services. To run GUI apps, you must map the host's X11 server socket (`/tmp/.X11-unix`) to the container, which is complex and poses security risks.""",
        "diagram": "Docker Hub Subscription Tier Table",
        "exercises": """### Hands-on Exercise: Inspect image size metadata
Find the physical disk space utilized by your local base images using `docker image ls`.""",
        "assignment": "Write a comparison overview on the pros and cons of containerized DBs vs Cloud Managed DBs.",
        "quiz": [
            {"q": "Is Docker Desktop free for companies with >1000 employees?", "options": ["No, it requires a paid subscription", "Yes, completely free", "Only on Windows", "Only on Linux"], "a": "No, it requires a paid subscription"},
            {"q": "What is the best alternative to Docker Desktop for commercial environments?", "options": ["Podman / Rancher Desktop", "VirtualBox", "VMware", "Ansible"], "a": "Podman / Rancher Desktop"}
        ],
        "interview": [
            {"q": "What are the architectural trade-offs of running databases in Docker containers?", "a": "Pros: Easy configuration and portability. Cons: Performance overhead, risk of data corruption if volumes aren't managed correctly, and complexity of configuring clustering and failover."}
        ],
        "mistakes": "Exposing local database ports publicly without configuring secure database passwords.",
        "troubleshooting": "If your application database fails to start, verify if another instance is already running on the same host port.",
        "best_practices": "Keep databases outside of application containers. Run databases in separate containers linked via networks, or use cloud-managed database services.",
        "cheat_sheet": "| FAQ Topic | Summary Answer |\n|---|---|\n| **Desktop License** | Paid for large enterprises |\n| **Production DB** | Generally prefer managed cloud services |\n| **Optimization** | Use multi-stage builds and alpine bases |",
        "references": "Docker Licensing Terms (docker.com/pricing/faq)."
    },
    {
        "num": 24,
        "name": "Capstone Project",
        "file": "capstone.md",
        "title": "Module 24 - Capstone Project",
        "objectives": "Build an enterprise-grade production-ready microservices application from scratch using Docker Compose and Dockerfiles.",
        "prereqs": "Modules 1-23",
        "explanation": """### Capstone: Real-Time Voting System
We will build a real-time voting system. It contains:
1. **Frontend (React)**: Web UI for users to cast votes.
2. **Backend (Node.js API)**: Processes votes and saves them to database.
3. **Queue (Redis)**: Transient queue for incoming votes.
4. **Worker (Python)**: Pulls votes from Redis queue and inserts them to PostgreSQL.
5. **Database (PostgreSQL)**: Holds voting totals.

### Architecture Map
```
+--------------------+
|   React Frontend   |
+---------+----------+
          | (HTTP)
          v
+--------------------+
|    NodeJS API      |
+---------+----------+
          |
          v
+--------------------+
|    Redis Queue     |
+---------+----------+
          ^
          | (Poll)
+---------+----------+
|   Python Worker    |
+---------+----------+
          |
          v
+--------------------+
|   Postgres DB      |
+--------------------+
```

### Complete `docker-compose.yml` for Capstone:
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-tier

  backend:
    build:
      context: ./backend
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis
    networks:
      - app-tier
      - queue-tier

  redis:
    image: redis:alpine
    networks:
      - queue-tier

  worker:
    build:
      context: ./worker
    depends_on:
      - redis
      - db
    networks:
      - queue-tier
      - db-tier

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: votesdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - db-tier

secrets:
  db_password:
    file: ./db_password.txt

volumes:
  db-data:

networks:
  app-tier:
  queue-tier:
  db-tier:
```""",
        "diagram": "Multi-tier Capstone Architecture (shown above)",
        "exercises": """### Hands-on Exercise: Configure the secrets file
Create the `db_password.txt` file containing your database password and launch the capstone using:
```bash
docker compose up --build -d
```""",
        "assignment": "Write the Node.js backend Dockerfile using multi-stage builds and an alpine node image.",
        "quiz": [
            {"q": "Which service acts as the transient queue in the Capstone?", "options": ["Redis", "NodeJS API", "Postgres", "React Frontend"], "a": "Redis"},
            {"q": "Why are there three networks in the Capstone?", "options": ["To isolate databases from public access frontend tiers", "To increase network speed", "To encrypt database data", "To bypass port mapping limits"], "a": "To isolate databases from public access frontend tiers"}
        ],
        "interview": [
            {"q": "Explain the security rationale behind the network isolation in this capstone.", "a": "By using separate networks (app-tier, queue-tier, db-tier), we ensure that the frontend container cannot reach the database container directly. Only the backend worker has access to the database network, protecting the database if the frontend is compromised."}
        ],
        "mistakes": "Exposing the Redis queue and PostgreSQL database ports to the host system publicly (`ports` section) instead of leaving them private inside their subnets.",
        "troubleshooting": "If database connection logs fail in the worker, inspect database configuration env files and ensure postgres is running healthily.",
        "best_practices": "Define health-checks for Postgres and Redis, and configure Compose dependencies to wait for database readiness before starting application code.",
        "cheat_sheet": "| Service | Network access |\n|---|---|\n| **Frontend** | `app-tier` only |\n| **Worker** | `queue-tier`, `db-tier` |\n| **Database** | `db-tier` only |",
        "references": "Real-World Multi-tier App Architecture Samples."
    },
    {
        "num": 25,
        "name": "Final Industry Preparation",
        "file": "prep.md",
        "title": "Module 25 - Final Industry Preparation",
        "objectives": "Prepare for Docker certifications, write clean resumes highlighting container experiences, and follow the cloud roadmap.",
        "prereqs": "None",
        "explanation": """### Docker Certified Associate (DCA) Exam Guide
The DCA certification validates your skills in container management, security, orchestration, and networking.
Key focus areas:
* **Orchestration**: Docker Swarm (Kubernetes basics)
* **Image Management**: Layering, registries
* **Installation & Configuration**: Docker daemon configuration
* **Networking**: Drivers, subnets
* **Security**: Certificates, rootless mode, capability limits

### Highlight Docker on your Resume
Include containerization experience in your project bullet points:
* *"Migrated monolithic application to multi-stage Docker containers, reducing image footprint by 65% and build pipeline times by 40%."*
* *"Designed secure multi-tier container networking layouts, isolating database layers from public web tiers."*
* *"Implemented Docker-in-Docker GitLab pipelines to automate packaging and deployment of 15 microservices."*

### Career Roadmap
```
+------------------+     +------------------+     +-------------------+
|      Docker      | ──► |  Docker Compose  | ──► |    Kubernetes     |
| (Single Instance)|     | (Multi-Container)|     | (Cluster Scaling) |
+------------------+     +------------------+     +-------------------+
                                                            |
                                                            v
                                                  +-------------------+
                                                  |   GitOps (ArgoCD) |
                                                  +-------------------+
```""",
        "diagram": "Docker Career Progression Roadmap (shown above)",
        "exercises": """### Hands-on Exercise: Review certification sample questions
Look up official DCA certification practice tests online and answer at least 10 mock questions.""",
        "assignment": "Update your resume/CV to include a dedicated section highlighting containerization and container orchestration skills.",
        "quiz": [
            {"q": "What certification is officially offered for Docker expertise?", "options": ["DCA (Docker Certified Associate)", "CKA", "AWS Certified Developer", "Docker Master"], "a": "DCA (Docker Certified Associate)"},
            {"q": "What is the logical next step after mastering Docker Compose?", "options": ["Kubernetes", "C language", "VirtualBox", "Apache HTTP Server"], "a": "Kubernetes"}
        ],
        "interview": [
            {"q": "How would you describe your containerization experience in a job interview?", "a": "Focus on the business outcomes: image size reduction, security hardening, pipeline automation, and local development environment alignment."}
        ],
        "mistakes": "Listing 'Docker' on your resume without being able to explain underlying concepts like namespaces or multi-stage builds.",
        "troubleshooting": "If your certification application fails, check test center requirements and credential verification forms.",
        "best_practices": "Build a portfolio repository containing clean Dockerfiles and Compose configurations for various web stacks.",
        "cheat_sheet": "| Focus | Recommendation |\n|---|---|\n| **Cert** | Review DCA guide |\n| **Next Steps** | Study Kubernetes |\n| **GitHub** | Push your Capstone Project |",
        "references": "Docker Certified Associate Guide (docker.com/certification/)."
    }
]

# Generate Welcome/Home Page
welcome_content = """# Docker Course: Beginner to Expert

Welcome to the ultimate, industry-grade guide to **Docker**! This course is designed to take you from absolute beginner to production-level containerization expert.

## Course Syllabus

### Module 1: Introduction to Docker
* What is Docker? Why was it created?
* VM vs Containers comparison.
* Alternatives, market demand, and future roadmaps.

### Module 2: Docker Fundamentals
* Blueprints, Cake Mixes, and Cakes: The image vs container analogy.
* Docker Hub and Registries.

### Module 3: Docker Architecture & Internals
* The Client-Server daemon model.
* Namespaces, cgroups, and UnionFS.

... and much more spanning 25 comprehensive modules!
"""

welcome_file_path = os.path.join(BASE_DIR, "welcome.md")
with open(welcome_file_path, "w", encoding="utf-8") as f:
    f.write(welcome_content)
print(f"Created welcome.md")

# Generate Module Directories and Files
toc_contents = [
    {
        "title": "Welcome Page",
        "href": "welcome.html"
    }
]

for m in modules:
    mod_dir_name = f"Module_{m['num']:02d}_{m['name'].replace(' ', '_')}"
    mod_dir_path = os.path.join(BASE_DIR, mod_dir_name)
    os.makedirs(mod_dir_path, exist_ok=True)
    
    # Structure of the Markdown file
    file_content = f"""# {m['title']}

## Learning Objectives
* {m['objectives']}

## Prerequisites
* **Prerequisites**: {m['prereqs']}

---

## Detailed Explanation
{m['explanation']}

---

## Hands-on Exercise
{m['exercises']}

## Assignment
{m['assignment']}

---

## Quiz
"""
    for idx, q in enumerate(m['quiz']):
        file_content += f"\n### Q{idx+1}: {q['q']}\n"
        for opt in q['options']:
            file_content += f"- {opt}\n"
        file_content += f"\n*Answer*: **{q['a']}**\n"

    file_content += "\n---\n\n## Interview Preparation\n"
    for q in m['interview']:
        file_content += f"\n### Q: {q['q']}\n*Answer*: {q['a']}\n"

    file_content += f"""
---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: {m['mistakes']}
* **Troubleshooting**: {m['troubleshooting']}

## Best Practices & Tips
* {m['best_practices']}

---

## Summary & Cheat Sheet
{m['cheat_sheet']}

---

## References & Further Reading
* {m['references']}
"""

    file_path = os.path.join(mod_dir_path, m['file'])
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"Created {mod_dir_name}/{m['file']}")
    
    # Add to TOC contents
    toc_contents.append({
        "title": m['title'],
        "href": f"{mod_dir_name}/{m['file'].replace('.md', '.html')}"
    })

# Write toc-contents.json
toc_file_path = os.path.join(BASE_DIR, "toc-contents.json")
with open(toc_file_path, "w", encoding="utf-8") as f:
    json.dump({"contents": toc_contents}, f, indent=2)
print("Created toc-contents.json")
