# Module 20 - Industry Architecture

## Learning Objectives
* Learn microservice integration patterns, container logging, shared network topologies, and domain segmentation.

## Prerequisites
* **Prerequisites**: Module 19

---

## Detailed Explanation
### Container Microservice Architectures
In modern production environments, monolithic systems are refactored into microservices. Docker facilitates this by keeping environments decoupled.

```
                  +--------------------------------+
                  |         Load Balancer          |
                  |         (Nginx Proxy)          |
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  User Service Container|                   | Order Service Container|
|     (NodeJS App)      |                   |      (Python App)     |
+-----------+-----------+                   +-----------+-----------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  User Database (pg)   |                   |  Order Database (pg)  |
|       (Volume)        |                   |       (Volume)        |
+-----------------------+                   +-----------------------+
```

### Architectural Rules
1. **Database-per-service**: Microservices must not access each other's databases directly. They communicate via APIs (REST/gRPC).
2. **Centralized Logging**: Containers dump logs to stdout. An external collector (FluentBit, Logstash) aggregates these and forwards them to logs systems (Elasticsearch, Loki).
3. **Stateless Services**: Web containers must not store local files. Session data must be shared in Redis, and user files stored in S3.

---

## Hands-on Exercise
### Hands-on Exercise: Map service dependencies
Design a network bridge layout separating customer service containers from backend analytics databases.

## Assignment
Write an architectural plan migrating a monolithic Django web server into separate Django-API and React-frontend containers.

---

## Quiz

### Q1: What is the database-per-service pattern?
- Each microservice has its own isolated database
- All containers write to one database table
- Containers use flat JSON files for persistence
- No database is permitted

*Answer*: **Each microservice has its own isolated database**

### Q2: Where should container logs be directed in production?
- Stdout and Stderr
- Local log files only
- Host /var/log directory only
- Database rows

*Answer*: **Stdout and Stderr**

---

## Interview Preparation

### Q: Why are stateless containers crucial for auto-scaling?
*Answer*: Stateless containers can be created or destroyed instantly without risking data loss, allowing orchestrators to scale instances up or down based on resource usage.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Connecting all microservices to a single shared database instance, recreating a monolithic architecture.
* **Troubleshooting**: If services experience high latency, verify DNS routing overheads and check network driver limits.

## Best Practices & Tips
* Store all user files outside container filesystems on cloud object storages (S3).

---

## Summary & Cheat Sheet
| Component | Purpose |
|---|---|
| Stateless | Store no sessions/files locally |
| Logging | Write output to stdout/stderr |
| Scaling | Dynamically balance container count |

---

## References & Further Reading
* Microservices Patterns by Chris Richardson.
