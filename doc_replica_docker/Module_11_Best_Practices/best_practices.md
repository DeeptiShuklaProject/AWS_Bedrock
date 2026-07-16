# Module 11 - Docker Best Practices

## Learning Objectives
* Apply coding standards for Dockerfiles, clean image optimizations, caching mechanisms, and container configuration rules.

## Prerequisites
* **Prerequisites**: Module 10

---

## Detailed Explanation
### 1. Optimize Image Size
* Use small base images (e.g. `alpine`, `slim`).
* Combine `RUN` instructions to reduce layer count.
* Clean package managers cache in the same layer:
  ```dockerfile
  RUN apt-get update && apt-get install -y \
      curl \
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
  ```

---

## Hands-on Exercise
### Hands-on Exercise: Optimize a slow Node.js Dockerfile
Refactor a provided Node.js Dockerfile to utilize layer caching for dependency installation, saving compile times.

## Assignment
Inspect container image layers using `docker history` and calculate the size savings from your optimization.

---

## Quiz

### Q1: Which base image is generally the smallest?
- ubuntu:latest
- alpine:latest
- debian:latest
- centos:latest

*Answer*: **alpine:latest**

### Q2: What happens if you run 'COPY . .' before running package installation?
- Layer cache for dependencies breaks on any code change
- The build speed increases
- The image size decreases
- Nothing changes

*Answer*: **Layer cache for dependencies breaks on any code change**

---

## Interview Preparation

### Q: How can you minimize the number of read-only image layers?
*Answer*: By combining multiple command operations into a single line using shell operators like '&&' and '\', particularly for installing packages and purging installer caches.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Keeping API keys or database password credentials hardcoded inside a Dockerfile's `ENV` instructions.
* **Troubleshooting**: If layer cache isn't updating after repository code changes, pass the `--no-cache` parameter during your build command.

## Best Practices & Tips
* Always declare a specific tag for base images (e.g., `node:18.16.0-alpine`) instead of a general tag like `node:latest`.

---

## Summary & Cheat Sheet
| Practice | Action |
|---|---|
| Base Image | Prefer `alpine` or `slim` |
| Layers | Chain shell commands with `&&` |
| Security | Always define a non-root `USER` |

---

## References & Further Reading
* Docker Development Best Practices.
