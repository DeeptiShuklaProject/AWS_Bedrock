# Module 16 - Containerized Testing

## Learning Objectives
* Learn to write tests for container setups, use Docker-in-Docker, run integration testing with testcontainers, and structure QA environments.

## Prerequisites
* **Prerequisites**: Module 15

---

## Detailed Explanation
### 1. Running Unit Tests in Docker
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
  ```

---

## Hands-on Exercise
### Hands-on Exercise: Run tests inside a Node container
Write a Dockerfile that copies an app's test files, executes test suites, and exits with a non-zero code on failures.

## Assignment
Write a PyTest script using testcontainers to test a connection to a running container database.

---

## Quiz

### Q1: What is DinD?
- Docker-in-Docker
- Docker-in-Development
- Dangling-image-Delete
- Docker-integration-Database

*Answer*: **Docker-in-Docker**

### Q2: How can a containerized tool control the host Docker daemon?
- By connecting via SSH
- By mapping /var/run/docker.sock to the container
- By using Docker Hub
- By exporting images

*Answer*: **By mapping /var/run/docker.sock to the container**

---

## Interview Preparation

### Q: What are the risks of mapping /var/run/docker.sock to a container?
*Answer*: It grants the container full root control over the host's Docker daemon. If compromised, an attacker can launch privileged containers to compromise the host OS.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Baking test code and test databases into the final production image, increasing image size and exposing vulnerabilities.
* **Troubleshooting**: If DinD builds fail, check if your host security daemon (AppArmor/SELinux) is blocking socket mounting permissions.

## Best Practices & Tips
* Use multi-stage builds to run test suites in intermediate stages, and copy only production assets to the final stage.

---

## Summary & Cheat Sheet
| CLI Mount | Purpose |
|---|---|
| `-v /var/run/docker.sock:/var/run/docker.sock` | Share host docker daemon socket |

---

## References & Further Reading
* Testcontainers Official Guide (testcontainers.com).
