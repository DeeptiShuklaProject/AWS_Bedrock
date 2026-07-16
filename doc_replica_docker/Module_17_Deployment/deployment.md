# Module 17 - Deployment & Orchestration

## Learning Objectives
* Learn Docker Compose configurations, service definitions, environment integrations, and Kubernetes orchestration fundamentals.

## Prerequisites
* **Prerequisites**: Module 16

---

## Detailed Explanation
### 1. Docker Compose
Docker Compose is a tool for defining and running multi-container applications. You define the configuration in a single YAML file (`docker-compose.yml`) and launch all services with a single command.

### Example `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    networks:
      - app-net

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    networks:
      - app-net

secrets:
  db_password:
    file: ./secrets/db_password.txt

networks:
  app-net:
    driver: bridge
```

### Useful Compose Commands:
* **`docker compose up -d`**: Start services in the background.
* **`docker compose down`**: Stop and remove containers, networks, and volumes.
* **`docker compose logs -f`**: Tail logs from all running services.

### 2. Transition to Orchestration (Kubernetes)
For production environments running on multiple servers, Docker Compose is insufficient. You need an orchestrator (like Kubernetes or Docker Swarm) to handle:
* High Availability (auto-restarting failed containers on different servers).
* Auto-Scaling (increasing container count based on traffic load).
* Rolling Updates (updating applications with zero downtime).

---

## Hands-on Exercise
### Hands-on Exercise: Launch a local App Stack
Write a compose file for a WordPress + MySQL stack, launch it, access the configuration UI, and tear it down.

## Assignment
Configure health-checks in a docker-compose service definition to ensure dependent containers wait until the database is healthy.

---

## Quiz

### Q1: Which command teardown a compose stack?
- docker compose down
- docker compose stop
- docker compose delete
- docker compose remove

*Answer*: **docker compose down**

### Q2: What network configuration is created by default by Docker Compose?
- A shared custom bridge network for all services
- Individual host networks
- None network mode
- Overlay swarm network

*Answer*: **A shared custom bridge network for all services**

---

## Interview Preparation

### Q: How does Docker Compose manage service dependencies?
*Answer*: By using the 'depends_on' configuration key. This starts services in the specified order, though additional health-checks are needed to ensure the target application is fully ready.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Hardcoding credentials in `docker-compose.yml` instead of loading them from a `.env` file or external environment variables.
* **Troubleshooting**: If services fail to communicate, verify that they are declared on the same network subnet inside the compose file.

## Best Practices & Tips
* Always declare volume paths explicitly and use named volumes for production database services.

---

## Summary & Cheat Sheet
| Command | Action |
|---|---|
| `docker compose up -d` | Launch all services in background |
| `docker compose ps` | List status of services |
| `docker compose down -v` | Stop services and purge volumes |

---

## References & Further Reading
* Docker Compose Spec (docs.docker.com/compose/).
