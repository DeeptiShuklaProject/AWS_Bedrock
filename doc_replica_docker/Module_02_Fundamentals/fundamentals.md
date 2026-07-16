# Module 2 - Docker Fundamentals

## Learning Objectives
* Learn the core concepts of Docker: Images, Containers, Registries, and the difference between Images and Containers.

## Prerequisites
* **Prerequisites**: Module 1

---

## Detailed Explanation
### The Core Concepts
1. **Docker Image**: A read-only template containing instructions for creating a Docker container. Think of it as a class in OOP, or a blueprint.
2. **Docker Container**: A runnable instance of a Docker image. Think of it as an object/instance in OOP.
3. **Docker Registry**: A storage and distribution system for Docker images (e.g., Docker Hub, Amazon ECR).

### Analogy: Baking a Cake
* **Recipe**: The Dockerfile
* **Cake Mix / Blueprint**: The Docker Image
* **The Baked Cake**: The Docker Container
* **Baking Recipe Book Store**: The Docker Registry

### How They Work Together
```
+---------------+     Build     +--------------+     Run     +-------------------+
|  Dockerfile   | ------------> | Docker Image | ----------> |  Docker Container |
+---------------+               +--------------+             +-------------------+
                                       |
                                       | Push / Pull
                                       v
                               +----------------+
                               | Docker Registry|
                               +----------------+
```

---

## Hands-on Exercise
### Hands-on Exercise: Run your first container
Run the classic hello-world container:
```bash
docker run hello-world
```

## Assignment
Pull the 'ubuntu' image and run an interactive shell inside it.

---

## Quiz

### Q1: What is a Docker image?
- A running application instance
- A read-only blueprint template
- A database engine
- A virtual machine monitor

*Answer*: **A read-only blueprint template**

### Q2: Which command runs a container from an image?
- docker build
- docker push
- docker run
- docker create

*Answer*: **docker run**

---

## Interview Preparation

### Q: What is the difference between an Image and a Container?
*Answer*: An image is a read-only blueprint template. A container is a running, writable instance instantiated from that image.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Modifying a container's filesystem and expecting those changes to persist inside the image automatically.
* **Troubleshooting**: If an image fails to pull, check your internet connection and ensure your registry DNS is resolvable.

## Best Practices & Tips
* Always version your images. Avoid using the 'latest' tag in production environments.

---

## Summary & Cheat Sheet
| Command | Description |
|---|---|
| `docker run <image>` | Runs a container from an image |
| `docker images` | Lists all local images |

---

## References & Further Reading
* Docker Image Specification (github.com/moby/moby).
