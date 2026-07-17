# Section 5 – Lambda Pricing

<a name="sec-5"></a>

AWS Lambda bills you for actual compute usage. The pricing model includes two core metrics: **Request Count** and **Execution Duration** (rounded to the nearest millisecond).

* **Request Charges**: $0.20 per 1 million requests ($0.0000002 per request).
* **Duration Charges**: Calculated in GB-seconds (gigabyte-seconds of execution).
  * Rate depends on the memory allocated to the function.
  * AWS grants 1 vCPU for every 1,769 MB of allocated memory.

### Calculation Example
Your function is allocated **1024 MB (1 GB)** of memory and runs **10,000,000 times** in a month. Each invocation takes exactly **200 milliseconds**.

1. **Request Costs**:
   * Total Requests: 10,000,000
   * Free Tier: 1,000,000 requests
   * Billable Requests: 9,000,000
   * Request Cost: $9,000,000 \times \$0.20 / 1,000,000 = \$1.80$

2. **Compute Duration Costs (GB-Seconds)**:
   * Total Execution Time: $10,000,000 \times 0.2 \text{ seconds} = 2,000,000 \text{ seconds}$
   * Allocated Memory: 1 GB
   * Total GB-Seconds: $2,000,000 \text{ seconds} \times 1 \text{ GB} = 2,000,000 \text{ GB-Seconds}$
   * Free Tier: 400,000 GB-Seconds
   * Billable GB-Seconds: $2,000,000 - 400,000 = 1,600,000 \text{ GB-Seconds}$
   * Rate: $0.0000166667 per GB-second
   * Duration Cost: $1,600,000 \times \$0.0000166667 = \$26.67$

3. **Total Monthly Bill**:
   * $\$1.80 + \$26.67 = \$28.47$

---
