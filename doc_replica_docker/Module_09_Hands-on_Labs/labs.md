# Module 9 - Hands-on Labs

## Learning Objectives
* Build basic container solutions, run containerized applications, map ports, inspect logs, and manage configuration files.

## Prerequisites
* **Prerequisites**: Module 8

---

## Detailed Explanation
### Lab 1: Interactive Alpine Container
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
```

---

## Hands-on Exercise
### Hands-on Exercise: Create custom landing page
Mount a folder containing an `index.html` file into the `/usr/share/nginx/html` path of an Nginx container using a bind mount.

## Assignment
Write a bash command pipeline that runs a Redis instance, populates a key, and retrieves it using `redis-cli` from inside the container.

---

## Quiz

### Q1: Which flag runs a container interactively with a terminal attached?
- -it
- -d
- -rm
- -p

*Answer*: **-it**

### Q2: What does -p 8080:80 mean?
- Map port 8080 on the host to port 80 in the container
- Map port 80 on the host to port 8080 in the container
- Open ports 80 and 8080 on the container
- Run container on CPU thread 80

*Answer*: **Map port 8080 on the host to port 80 in the container**

---

## Interview Preparation

### Q: How do you check container output stdout/stderr without logging in?
*Answer*: By using the command `docker logs <container-id>`.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Exposing production database containers to public internet interfaces (e.g. mapping port `0.0.0.0:5432:5432` instead of binding to localhost `127.0.0.1:5432:5432`).
* **Troubleshooting**: If port mapping fails with 'port is already allocated', find the conflicting process using `netstat` or choose another host port.

## Best Practices & Tips
* Clean up temporary containers using the `--rm` flag to delete container filesystems automatically upon termination.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker run -it <image> <command>` | Run interactively |
| `docker run -d -p <host>:<container> <image>` | Run detached with port mapped |
| `docker logs <container>` | Show container logs |

---

## References & Further Reading
* Docker Command Reference (docs.docker.com/engine/reference/commandline/run/).
