# Module 5 - Environment Setup

## Learning Objectives
* Install Docker Desktop, verify the installation, configure environment variables, and verify configuration status.

## Prerequisites
* **Prerequisites**: Module 4

---

## Detailed Explanation
### Hardware & Software Requirements
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
```

---

## Hands-on Exercise
### Hands-on Exercise: Run verification check
Execute the diagnostic script to ensure Docker is running correctly:
```bash
docker run --rm hello-world
```

## Assignment
Add your local user to the 'docker' group on Linux to run docker commands without sudo.

---

## Quiz

### Q1: Which backend virtualizer does Windows recommend for Docker Desktop?
- WSL 2
- VirtualBox
- VMware Workstation
- Hyper-V legacy only

*Answer*: **WSL 2**

### Q2: Which command checks system information for Docker?
- docker info
- docker status
- docker diagnostic
- docker print

*Answer*: **docker info**

---

## Interview Preparation

### Q: Why do we add a user to the 'docker' group in Linux?
*Answer*: The Docker daemon binds to a UNIX socket owned by root. By adding the user to the docker group, we grant access to run docker commands without typing 'sudo'.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Forgetting to enable hardware virtualization in BIOS before launching WSL 2 or Docker Desktop.
* **Troubleshooting**: If Docker Desktop hangs on startup, restart the WSL 2 subsystem by running `wsl --shutdown` in PowerShell.

## Best Practices & Tips
* Set memory and CPU limits inside Docker Desktop settings to avoid freezing your host system during heavy builds.

---

## Summary & Cheat Sheet
| Command | Purpose |
|---|---|
| `docker info` | Inspect engine logs/status |
| `docker version` | Output version details |

---

## References & Further Reading
* Docker Installation Guide (docs.docker.com/engine/install/).
