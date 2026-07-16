# Module 14 - Performance Optimization

## Learning Objectives
* Optimize resource allocations, profiles, memory configurations, CPU tuning, and caching networks.

## Prerequisites
* **Prerequisites**: Module 13

---

## Detailed Explanation
### 1. Resource Limits (CPU & Memory)
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
  ```

---

## Hands-on Exercise
### Hands-on Exercise: Set resource boundaries
Verify resource throttling by running a stress container with memory limitations:
```bash
docker run -it --rm -m 256m progrium/stress --cpu 2 --io 1 --vm 1 --vm-bytes 128M --timeout 10s
```

## Assignment
Write a performance comparison summary comparing bridge network response times with host network direct connections.

---

## Quiz

### Q1: Which environment variable enables the BuildKit engine?
- DOCKER_BUILDKIT=1
- BUILDKIT=true
- DOCKER_FAST=1
- USE_BUILDKIT=1

*Answer*: **DOCKER_BUILDKIT=1**

### Q2: What flag restricts memory usage?
- -m
- --limit-mem
- --ram
- -c

*Answer*: **-m**

---

## Interview Preparation

### Q: How does setting memory limits protect a host OS under high load?
*Answer*: It ensures that if a container experiences a memory leak, it will trigger the Linux Out-Of-Memory (OOM) killer to terminate only that container process, preventing the entire host OS from freezing.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Setting memory limits too low, causing containers to instantly crash with Out-Of-Memory (OOM) codes during startup.
* **Troubleshooting**: Check if a container was terminated due to memory pressure by executing `docker inspect` and searching for the 'OOMKilled' attribute.

## Best Practices & Tips
* Monitor resource footprints using `docker stats` and calibrate memory boundaries under workload simulations.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker stats` | Live stream resource usage statistics |
| `docker run -m 512m` | Restrict memory to 512 megabytes |
| `docker run --cpus 1` | Allocate maximum 1 CPU core |

---

## References & Further Reading
* Docker Performance and Runtime Constraints.
