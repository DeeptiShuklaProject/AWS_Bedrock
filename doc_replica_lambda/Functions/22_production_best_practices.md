# Section 22 – Production Best Practices

<a name="sec-22"></a>

* **Keep Functions Small**: Write focused, modular code that does one thing well.
* **Reuse Connections**: Initialize database clients, SDK clients, and heavy data stores outside the handler function to reuse them during warm starts.
* **Minimize Cold Start Latency**: Package only required dependencies and initialize code outside the handler.
* **Manage Concurrency**: Configure **Reserved Concurrency** on critical microservices to prevent non-critical scripts from consuming your account's concurrent execution limits.

---
