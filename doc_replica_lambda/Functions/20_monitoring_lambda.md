# Section 20 – Monitoring Lambda

<a name="sec-20"></a>

### Logging with CloudWatch
Anything printed using standard Python statements or logged with `logging` is automatically sent to **Amazon CloudWatch Logs** under the Log Group `/aws/lambda/<function-name>`.

### Key Metrics to Monitor
* **Invocations**: The total number of execution requests.
* **Errors**: The number of runs that ended with an unhandled exception (raising 4xx/5xx responses).
* **Duration**: The time it takes to run your code, in milliseconds.
* **Throttles**: Invocation requests rejected because concurrency limits were exceeded.

### Tracing with AWS X-Ray
Enable X-Ray tracing to map request execution steps across downstream AWS services and pinpoint latency bottlenecks.

---
