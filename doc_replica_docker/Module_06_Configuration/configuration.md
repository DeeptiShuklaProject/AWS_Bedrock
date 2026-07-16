# Module 6 - Configuration & daemon.json

## Learning Objectives
* Configure the Docker Daemon using daemon.json, set up environment variables, and manage configuration profiles.

## Prerequisites
* **Prerequisites**: Module 5

---

## Detailed Explanation
### The daemon.json File
The Docker daemon can be configured globally using a JSON file called `daemon.json`. 
* **Location (Linux)**: `/etc/docker/daemon.json`
* **Location (Windows)**: `C:\ProgramData\docker\config\daemon.json`

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
* `DOCKER_CERT_PATH`: Directory containing security certificates.

---

## Hands-on Exercise
### Hands-on Exercise: Configure log rotation
Create or modify your local `/etc/docker/daemon.json` to include log-driver size limits to prevent hard drive exhaustion.

## Assignment
Configure the Docker CLI to connect to a remote Docker instance running on a virtual machine.

---

## Quiz

### Q1: Where is the default location for daemon.json in Linux?
- /etc/docker/daemon.json
- /var/lib/docker/daemon.json
- /usr/bin/daemon.json
- /etc/daemon.json

*Answer*: **/etc/docker/daemon.json**

### Q2: Which env variable points Docker CLI to a remote daemon socket?
- DOCKER_HOST
- DOCKER_DAEMON
- DOCKER_REMOTE
- DOCKER_SOCKET

*Answer*: **DOCKER_HOST**

---

## Interview Preparation

### Q: How can you restrict container logs from filling up the entire server disk?
*Answer*: By configuring log rotation limits inside `daemon.json` under the 'log-opts' key, setting 'max-size' (e.g., '10m') and 'max-file' limit parameters.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Typing malformed JSON (missing commas or unclosed brackets) in `daemon.json`, which prevents the daemon from starting.
* **Troubleshooting**: Run `journalctl -u docker` to view daemon startup logs if dockerd fails to reload after modifying config files.

## Best Practices & Tips
* Always validate the JSON configuration before restarting the Docker service.

---

## Summary & Cheat Sheet
| Settings Key | Value | Description |
|---|---|---|
| `debug` | `true/false` | Toggles debug mode logs |
| `log-driver` | `"json-file"` | Sets default logs format |

---

## References & Further Reading
* Docker Daemon Reference (docs.docker.com/engine/reference/commandline/dockerd).
