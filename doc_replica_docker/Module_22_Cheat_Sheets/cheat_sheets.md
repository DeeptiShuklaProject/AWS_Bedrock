# Module 22 - Cheat Sheets & Reference Guides

## Learning Objectives
* A quick reference guide for essential Docker commands, operations, and file formats.

## Prerequisites
* **Prerequisites**: None

---

## Detailed Explanation
### Container Management
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
```

---

## Hands-on Exercise
### Hands-on Exercise: Clean up local systems
Run a complete cleanup pipeline using prune commands to verify disk space recovery:
```bash
docker system df
docker system prune -f
```

## Assignment
Design a printed cheat sheet layout summarizing container state commands.

---

## Quiz

### Q1: Which flag deletes volumes during a system prune?
- --volumes
- -v
- --all
- -f

*Answer*: **--volumes**

### Q2: Which command displays container resource usage statistics?
- docker stats
- docker top
- docker inspect
- docker monitor

*Answer*: **docker stats**

---

## Interview Preparation

### Q: How can you completely clear out all cached image layers and volumes in development?
*Answer*: By executing 'docker system prune -a --volumes' to wipe all stopped containers, unused networks, images, and volumes.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Running `docker system prune -a` in production environments, which can delete cache layers used by active rollback systems.
* **Troubleshooting**: If docker prune commands freeze, restart the docker service to release file locks.

## Best Practices & Tips
* Keep a printout or digital bookmark of core CLI commands for easy lookup.

---

## Summary & Cheat Sheet
| Command Category | Core Utility |
|---|---|
| **Lifecycle** | `run`, `stop`, `rm` |
| **Diagnostic** | `logs`, `inspect`, `stats` |
| **Pruning** | `system prune` |

---

## References & Further Reading
* Docker CLI Cheat Sheet.
