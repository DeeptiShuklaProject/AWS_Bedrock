# Module 10 - Real-World Projects

## Learning Objectives
* Build multi-tier applications using custom Dockerfiles, manage multi-stage builds, and structure project layouts.

## Prerequisites
* **Prerequisites**: Module 9

---

## Detailed Explanation
### Project Overview: Python Flask App with Redis Cache
We will build a simple visitor counter application. The application will use Flask (Python) as a web server, and Redis as an in-memory database to store the view counts.

### Project Directory Structure
```
flask-redis-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

### 1. `app.py`
```python
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'
```

### 2. `requirements.txt`
```
flask
redis
```

### 3. `Dockerfile` (Multi-Stage Production Build)
```dockerfile
# Stage 1: Build dependencies
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## Hands-on Exercise
### Hands-on Exercise: Build the project image
Build the Python Flask app image locally using:
```bash
docker build -t flask-redis-app:1.0 .
```

## Assignment
Write a Docker Compose file to run both the Redis container and your Flask container on a shared custom bridge network.

---

## Quiz

### Q1: What is the purpose of AS builder in a Dockerfile?
- It names a build stage for multi-stage builds
- It runs the app in debug mode
- It installs dependencies
- It acts as the primary entrypoint

*Answer*: **It names a build stage for multi-stage builds**

### Q2: Which instruction exposes container ports?
- EXPOSE
- PORT
- BIND
- LISTEN

*Answer*: **EXPOSE**

---

## Interview Preparation

### Q: Why do we use multi-stage Docker builds?
*Answer*: To separate build-time dependencies (like compilers, build tools, SDKs) from the final run-time image. This significantly reduces the size of the final production image and improves security.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Copying entire development folders (including node_modules/ or virtual environments) into the build context instead of using `.dockerignore`.
* **Troubleshooting**: If your Python script fails due to missing modules, check if paths from your builder stage are correctly mapped to runtime environment paths.

## Best Practices & Tips
* Create a `.dockerignore` file containing `.git`, `node_modules`, and local config secrets to keep build contexts clean.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker build -t <tag> .` | Build image from Dockerfile |
| `docker history <image>` | View history of image layers |

---

## References & Further Reading
* Best practices for writing Dockerfiles (docs.docker.com/develop/develop-images/dockerfile_best-practices/).
