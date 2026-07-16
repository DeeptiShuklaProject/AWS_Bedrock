# Module 7 - Core Concepts

## Learning Objectives
* Learn to manage the lifecycle of Docker containers, understand container states, image layers, and key CLI utilities.

## Prerequisites
* **Prerequisites**: Module 6

---

## Detailed Explanation
### Container Lifecycle States
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
When a container is started, a thin **Writable Layer** (container layer) is added on top of the stack. All changes (writing files, deleting files) are written to this writable layer.

---

## Hands-on Exercise
### Hands-on Exercise: Manage container states
Create a container, pause it, inspect states, unpause, stop it, and delete it:
```bash
docker run -d --name test-nginx nginx
docker pause test-nginx
docker inspect --format='{{.State.Status}}' test-nginx
docker unpause test-nginx
docker stop test-nginx
docker rm test-nginx
```

## Assignment
Write a bash script that cleans up all stopped containers and unused dangling image layers.

---

## Quiz

### Q1: Which signal is sent first by docker stop?
- SIGKILL
- SIGTERM
- SIGINT
- SIGHUP

*Answer*: **SIGTERM**

### Q2: What happens to data written inside a container when the container is deleted?
- Data is persisted in the image
- Data is deleted unless mapped to a volume
- Data is backed up to Docker Hub
- Data is locked

*Answer*: **Data is deleted unless mapped to a volume**

---

## Interview Preparation

### Q: What is the difference between docker stop and docker kill?
*Answer*: docker stop sends SIGTERM first to allow processes to clean up and shut down gracefully, then sends SIGKILL after a timeout. docker kill sends SIGKILL immediately to stop the processes without cleanup.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Deleting a container expecting to release storage space without removing the associated anonymous volumes.
* **Troubleshooting**: If a container fails to stop, check if it has trapped the SIGTERM signal (like some PID 1 node processes do).

## Best Practices & Tips
* Always run containers with resource flags (`--memory`, `--cpus`) to prevent containers from monopolizing host memory.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker run -d` | Run container in background (detached) |
| `docker ps -a` | Show running and exited containers |
| `docker rm -f` | Force remove a running container |

---

## References & Further Reading
* Docker Engine CLI (docs.docker.com/engine/reference/run/).
