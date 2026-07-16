# Module 15 - Debugging & Troubleshooting

## Learning Objectives
* Master container debugging utilities: exec, inspect, logs, export/import, events, and networking troubleshooting.

## Prerequisites
* **Prerequisites**: Module 14

---

## Detailed Explanation
### 1. Interactive Debugging (`docker exec`)
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
```

---

## Hands-on Exercise
### Hands-on Exercise: Extract diagnostic logs
Use `docker inspect` to discover the exact IP address and gateway of a running Nginx container, then extract its logs.

## Assignment
Troubleshoot a broken container (e.g. database configuration error) using `docker logs` and `docker inspect` to fix the env vars.

---

## Quiz

### Q1: Which command executes a diagnostic shell inside a running container?
- docker run
- docker exec
- docker attach
- docker debug

*Answer*: **docker exec**

### Q2: What format is outputted by docker inspect?
- YAML
- JSON
- XML
- CSV

*Answer*: **JSON**

---

## Interview Preparation

### Q: How can you debug a container that exits immediately upon startup?
*Answer*: 1. Run 'docker logs <container-id>' to read standard error outputs. 2. Inspect container definitions via 'docker inspect'. 3. Temporarily override the entrypoint (e.g. '--entrypoint sh') to inspect files.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Trying to run `docker exec` on a container that has already stopped/exited.
* **Troubleshooting**: If your container crashes with no error logs, verify if your code is printing outputs to `/var/log` files instead of stdout/stderr.

## Best Practices & Tips
* Ensure application code prints errors to stdout/stderr so that they can be easily captured by `docker logs`.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker exec -it <id> sh` | Open interactive shell inside running container |
| `docker inspect <id>` | Show configuration details |
| `docker cp <src> <dest>` | Copy files in/out of containers |

---

## References & Further Reading
* Docker Troubleshooting Guide.
