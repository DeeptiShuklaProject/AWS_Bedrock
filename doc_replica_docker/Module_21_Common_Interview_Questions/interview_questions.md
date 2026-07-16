# Module 21 - Common Interview Questions

## Learning Objectives
* Review key interview questions spanning beginner, intermediate, advanced, and scenario-based categories.

## Prerequisites
* **Prerequisites**: Modules 1-20

---

## Detailed Explanation
### Beginner Questions
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
   * *Answer*: Linux PID 1 processes are system handlers. By default, they do not inherit default signal handlers (like SIGTERM). If the application code doesn't explicitly trap SIGTERM, it ignores it until `docker stop` times out and sends SIGKILL.

---

## Hands-on Exercise
### Hands-on Exercise: Simulate a PID 1 signal trap
Write a basic Node.js script, package it as PID 1, and test its termination behavior under `docker stop`.

## Assignment
Write a mock interview transcript answering three scenario-based Docker questions.

---

## Quiz

### Q1: Which image tag represents a dangling layer?
- <none>:<none>
- latest
- dangling
- null

*Answer*: **<none>:<none>**

### Q2: Which instruction is preferred for importing local configurations?
- COPY
- ADD
- ENV
- RUN

*Answer*: **COPY**

---

## Interview Preparation

### Q: What happens when you run out of disk space due to container logs?
*Answer*: The Docker daemon cannot write container operations, causing systems to fail. I resolve this by configuring log rotation limiters (max-size/max-file) in daemon.json.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Providing vague answers about containerization without explaining the underlying Linux primitives (namespaces, cgroups).
* **Troubleshooting**: Use `docker system df` to analyze which resource (containers, images, volumes) is exhausting local storage.

## Best Practices & Tips
* Structure your answers using the STAR method (Situation, Task, Action, Result) for scenario-based questions.

---

## Summary & Cheat Sheet
| Topic | Key Concept |
|---|---|
| **Lighter images** | Multi-stage builds, alpine base |
| **Signals** | PID 1 needs signal trapping |
| **Persistence** | Volumes vs Bind Mounts |

---

## References & Further Reading
* Technical Interview Prep Guides.
