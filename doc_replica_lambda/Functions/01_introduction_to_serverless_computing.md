# Section 1 – Introduction to Serverless Computing

<a name="sec-1"></a>

### What is Serverless?
In traditional cloud computing, developers deploy applications on servers (e.g., AWS EC2 instances). Developers must provision hardware, configure operating systems, apply security patches, manage network firewalls, and manually scale applications up or down.

**Serverless Computing** is a cloud execution model where cloud providers dynamically manage server provisioning, runtime execution, and resource allocation. As a developer, you only upload code. You do not manage, patch, or configure the underlying instances. The cloud provider handles all scaling, high availability, and operational overhead.

> [!NOTE]
> Serverless does not mean there are no servers. Servers still exist, but they are fully managed by AWS, abstracted away from your day-to-day work.

### Compute Evolution: From Bare Metal to Serverless
```
+------------------+     +------------------+     +------------------+     +------------------+
| Physical Servers | ──► | Virtual Machines | ──► |    Containers    | ──► |    Serverless    |
| (Bare Metal)     |     | (e.g., AWS EC2)  |     | (e.g., Docker)   |     | (e.g., Lambda)   |
| Years/Months     |     | Minutes          |     | Seconds          |     | Milliseconds     |
+------------------+     +------------------+     +------------------+     +------------------+
```

1. **Traditional On-Premises Servers**: Long procurement times, high capital costs, manual maintenance, and paid for regardless of utilization.
2. **Virtual Machines (VMs/EC2)**: Faster provisioning, but still requires operating system patching, daemon management, scaling rules, and payments for idle CPU hours.
3. **Containers (Docker/Kubernetes/ECS)**: Excellent portability and fast startup, but requires managing cluster container orchestrators, resource sizing, and task definitions.
4. **Serverless (AWS Lambda)**: No server management, millisecond startup times, sub-second billing, and automatic scaling from zero to thousands of parallel executions.

### Benefits of Serverless
* **Zero Infrastructure Management**: Focus exclusively on application business logic.
* **Continuous & Automatic Scaling**: Scaled dynamically per request.
* **Cost Efficiency (Pay-per-Use)**: Pay only for the duration of execution, rounded to the nearest millisecond. Idle environments cost **$0**.
* **High Availability & Fault Tolerance**: Built-in multi-AZ availability.

### Limitations of Serverless
* **Execution Timeout**: Max execution limit is 15 minutes.
* **Cold Starts**: Startup latency when a container boots up for the first time.
* **Ephemeral Storage**: Configurable local temporary storage (`/tmp`) from 512 MB to 10 GB.
* **State Management**: Execution environments are stateless; no persistence of in-memory variables between separate requests.

---
