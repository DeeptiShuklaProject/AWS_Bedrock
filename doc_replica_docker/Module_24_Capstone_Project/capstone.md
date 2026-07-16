# Module 24 - Capstone Project

## Learning Objectives
* Build an enterprise-grade production-ready microservices application from scratch using Docker Compose and Dockerfiles.

## Prerequisites
* **Prerequisites**: Modules 1-23

---

## Detailed Explanation
### Capstone: Real-Time Voting System
We will build a real-time voting system. It contains:
1. **Frontend (React)**: Web UI for users to cast votes.
2. **Backend (Node.js API)**: Processes votes and saves them to database.
3. **Queue (Redis)**: Transient queue for incoming votes.
4. **Worker (Python)**: Pulls votes from Redis queue and inserts them to PostgreSQL.
5. **Database (PostgreSQL)**: Holds voting totals.

### Architecture Map
```
+--------------------+
|   React Frontend   |
+---------+----------+
          | (HTTP)
          v
+--------------------+
|    NodeJS API      |
+---------+----------+
          |
          v
+--------------------+
|    Redis Queue     |
+---------+----------+
          ^
          | (Poll)
+---------+----------+
|   Python Worker    |
+---------+----------+
          |
          v
+--------------------+
|   Postgres DB      |
+--------------------+
```

### Complete `docker-compose.yml` for Capstone:
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-tier

  backend:
    build:
      context: ./backend
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis
    networks:
      - app-tier
      - queue-tier

  redis:
    image: redis:alpine
    networks:
      - queue-tier

  worker:
    build:
      context: ./worker
    depends_on:
      - redis
      - db
    networks:
      - queue-tier
      - db-tier

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: votesdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - db-tier

secrets:
  db_password:
    file: ./db_password.txt

volumes:
  db-data:

networks:
  app-tier:
  queue-tier:
  db-tier:
```

---

## Hands-on Exercise
### Hands-on Exercise: Configure the secrets file
Create the `db_password.txt` file containing your database password and launch the capstone using:
```bash
docker compose up --build -d
```

## Assignment
Write the Node.js backend Dockerfile using multi-stage builds and an alpine node image.

---

## Quiz

### Q1: Which service acts as the transient queue in the Capstone?
- Redis
- NodeJS API
- Postgres
- React Frontend

*Answer*: **Redis**

### Q2: Why are there three networks in the Capstone?
- To isolate databases from public access frontend tiers
- To increase network speed
- To encrypt database data
- To bypass port mapping limits

*Answer*: **To isolate databases from public access frontend tiers**

---

## Interview Preparation

### Q: Explain the security rationale behind the network isolation in this capstone.
*Answer*: By using separate networks (app-tier, queue-tier, db-tier), we ensure that the frontend container cannot reach the database container directly. Only the backend worker has access to the database network, protecting the database if the frontend is compromised.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Exposing the Redis queue and PostgreSQL database ports to the host system publicly (`ports` section) instead of leaving them private inside their subnets.
* **Troubleshooting**: If database connection logs fail in the worker, inspect database configuration env files and ensure postgres is running healthily.

## Best Practices & Tips
* Define health-checks for Postgres and Redis, and configure Compose dependencies to wait for database readiness before starting application code.

---

## Summary & Cheat Sheet
| Service | Network access |
|---|---|
| **Frontend** | `app-tier` only |
| **Worker** | `queue-tier`, `db-tier` |
| **Database** | `db-tier` only |

---

## References & Further Reading
* Real-World Multi-tier App Architecture Samples.
