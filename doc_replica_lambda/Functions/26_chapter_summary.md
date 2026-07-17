# Section 26 – Chapter Summary

<a name="sec-26"></a>

### Key Takeaways
* AWS Lambda is a serverless compute service that executes code in response to triggers.
* It operates on a pay-per-use billing model based on request count and execution duration.
* Runtimes like Python 3.12 are fully managed, and security is enforced using IAM execution roles.
* Maximum runtime duration is **15 minutes**.

### Important AWS Lambda Limits
| Metric | Limit |
|---|---|
| **Memory Allocation** | 128 MB to 10,240 MB |
| **Timeout Limit** | 15 Minutes |
| **Local Temporary Storage (`/tmp`)** | 512 MB to 10 GB |
| **Deployment Package Size** | 50 MB zipped, 250 MB unzipped |
| **Concurrent Executions** | 1,000 per region (Soft limit, request increase) |
