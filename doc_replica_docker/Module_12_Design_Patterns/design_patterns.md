# Module 12 - Container Design Patterns

## Learning Objectives
* Learn modern container design patterns: Sidecar, Ambassador, Adapter, and Init Container patterns.

## Prerequisites
* **Prerequisites**: Module 11

---

## Detailed Explanation
### Single-Container vs Multi-Container Patterns
Containers should follow single-responsibility rules. Design patterns help orchestrate shared workloads:

### 1. Sidecar Pattern
A secondary container runs alongside the primary application to extend or enhance its functionality.
* **Example**: An application container writes log files to a shared volume. A sidecar container tail-reads those logs and pushes them to Elasticsearch.

### 2. Ambassador Pattern
An ambassador container acts as a local proxy for network connections to remote resources.
* **Example**: The application connects to `localhost:3306` (the local ambassador). The ambassador handles security, retry logic, and routes queries to the actual remote cloud database cluster.

### 3. Init Container Pattern
Containers that run and complete execution *before* the main application container starts.
* **Example**: A container that runs database migration scripts or waits for third-party services to become reachable.

```
Sidecar Pattern Model:
+-------------------------------------------------+
|                    Pod/Host                     |
|                                                 |
|  +--------------------+   +------------------+  |
|  | Primary Application|   | Sidecar Container|  |
|  | (Flask Web Server) |   | (Log Forwarder)  |  |
|  +---------+----------+   +--------+---------+  |
|            |                       |            |
|            +----> Shared Volume <--+            |
+-------------------------------------------------+
```

---

## Hands-on Exercise
### Hands-on Exercise: Implement an Init Container
Create a shell script that verifies database availability (pings db container) before launching your web application service.

## Assignment
Model a log forwarder sidecar pattern on paper, defining sharing volumes and necessary networking configs.

---

## Quiz

### Q1: Which pattern acts as a local proxy for outgoing database queries?
- Sidecar
- Ambassador
- Adapter
- Init Container

*Answer*: **Ambassador**

### Q2: When do Init Containers run?
- Concurrently with the main app
- After the main app exits
- Before the main app container starts
- Only when the app crashes

*Answer*: **Before the main app container starts**

---

## Interview Preparation

### Q: What is the primary benefit of the Sidecar design pattern?
*Answer*: It allows separation of concerns. You can update or swap out helper utilities (like logging, monitoring agents, or cert reloaders) without rebuilding or disrupting the main application container code.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Mixing helper utilities and web application servers inside a single, bloated container process.
* **Troubleshooting**: If main containers crash because databases aren't ready, wrap start processes in health-check loop scripts.

## Best Practices & Tips
* Ensure sidecars share host resources gracefully, setting strict CPU/Memory resource constraints for helpers.

---

## Summary & Cheat Sheet
| Pattern | Primary Use-Case |
|---|---|
| **Sidecar** | Logs forwarding, metrics collection |
| **Ambassador** | Database routing, circuit breakers |
| **Init** | Code migrations, dependency readiness checks |

---

## References & Further Reading
* Distributed Systems Patterns by Brendan Burns.
