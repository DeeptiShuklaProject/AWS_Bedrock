import os
import re

notes_dir = r"c:\Users\nishu\workspace\wscs_bedrock\Uday_AWS_Services_notes"

war_room_templates = {
    "Chapter_01_AWS_Lambda.md": """# Production Incident War Room

## Incident 1: Unexpected High Cold Starts and HTTP 504 Gateway Timeouts
### Incident Summary
A major e-commerce API experienced sudden HTTP 504 Gateway Timeouts during a flash sale. Upstream API Gateway timed out waiting for AWS Lambda invocations to complete.

### Symptoms
- API Gateway returns HTTP `504 Gateway Timeout`.
- User requests latency spikes from 150ms to >15,000ms.
- CloudWatch metric `Duration` shows sharp peaks reaching maximum configured function timeout.

### Possible Causes
- Cold start initialization latency due to heavy imports or VPC ENI provisioning.
- Database connection pool exhaustion during rapid execution environment scaling.
- Unhandled synchronous blocking calls inside the Lambda handler.

### Investigation Steps
1. Inspect CloudWatch Metrics for `Invocations`, `ConcurrentExecutions`, `Duration`, and `Errors`.
2. Filter CloudWatch Log Group `/aws/lambda/enterprise_api_handler` for `REPORT` lines containing `Init Duration`.
3. Check RDS CloudWatch metric `DatabaseConnections` for connection spikes.

### CloudWatch Metrics to Check
- `ConcurrentExecutions`
- `Duration` (p95, p99)
- `Throttles`
- `Errors`
- `InitDuration`

### CloudWatch Logs
Search `/aws/lambda/<function-name>`:
```text
REPORT RequestId: 8f72a1b9-3c1d... Duration: 15004.23 ms Billed Duration: 15005 ms Memory Size: 1024 MB Max Memory Used: 210 MB Init Duration: 4820.12 ms
```

### CloudTrail Events
- `UpdateFunctionConfiguration`
- `UpdateFunctionCode`

### IAM Verification
- Verify execution role has `AWSLambdaVPCAccessExecutionRole` (`ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`, `ec2:DeleteNetworkInterface`).

### Networking Verification
- Confirm Lambda subnets have NAT Gateway access or VPC Endpoints for S3/DynamoDB/Secrets Manager.

### CLI Commands
```bash
aws lambda get-function-concurrency --function-name enterprise_api_handler
aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Duration --dimensions Name=FunctionName,Value=enterprise_api_handler --start-time 2026-07-22T00:00:00Z --end-time 2026-07-23T00:00:00Z --period 300 --statistics Average Maximum
```

### SDK Verification (Python Boto3)
```python
import boto3
client = boto3.client('lambda')
res = client.get_function_configuration(FunctionName='enterprise_api_handler')
print("Timeout:", res['Timeout'], "Memory:", res['MemorySize'])
```

### Root Cause Analysis
The function imported unneeded heavyweight data processing packages inside the handler and created a new RDS database connection per invocation instead of sharing global state, causing DB connection starvation and massive initialization delays.

### Immediate Mitigation
- Increase function Memory to 3072 MB (allocates proportional vCPU).
- Enable Provisioned Concurrency (e.g., 50 warm instances) via CLI to eliminate cold starts.

### Permanent Resolution
- Move Boto3 and database initialization code outside the handler function to leverage warm execution context.
- Implement RDS Proxy to multiplex database connections.

### Prevention
- Configure CloudWatch Alarms on `Duration` > 3000ms.
- Establish automated CI/CD load testing with Locust or K6 before production deployments.

---

## Incident 2: Throttling Exceptions (Rate Exceeded `429 Too Many Requests`)
### Incident Summary
During peak traffic, asynchronous S3 file uploads failed to trigger processing functions, returning `TooManyRequestsException`.

### Symptoms
- CloudWatch `Throttles` metric spikes.
- Upstream event sources experience delay or missing notifications.

### Possible Causes
- Account-level regional concurrency limit (1,000) reached by another noisy-neighbor function.
- Reserved concurrency set too low on the target function.

### Investigation Steps
1. Check CloudWatch `Throttles` metric for the specific function vs account total.
2. Query AWS Service Quotas for regional concurrency limits.

### CloudWatch Metrics to Check
- `Throttles`
- `ConcurrentExecutions`
- `UnreservedConcurrentExecutions`

### CloudWatch Logs
```text
Task timed out / Rate Exceeded. Account limit exceeded for concurrent executions.
```

### CloudTrail Events
- `PutFunctionConcurrency`

### IAM Verification
- Check service quota permissions.

### Networking Verification
- N/A (Concurrency is control plane).

### CLI Commands
```bash
aws lambda get-account-settings
aws cloudwatch get-metric-data --metric-data-queries file://query.json
```

### SDK Verification (Python Boto3)
```python
import boto3
client = boto3.client('lambda')
account_info = client.get_account_settings()
print(account_info['AccountLimit'])
```

### Root Cause Analysis
A background ETL Lambda function consumed 950 of the 1,000 account concurrent executions, leaving only 50 for the critical API handler.

### Immediate Mitigation
- Set Reserved Concurrency = 0 on non-critical background ETL function to stop it.
- Request AWS Service Quota increase for concurrent executions.

### Permanent Resolution
- Assign explicit Reserved Concurrency to production critical functions.
- Isolate environments (Dev, Staging, Prod) into separate AWS Accounts.

### Prevention
- Set CloudWatch Alarm on `UnreservedConcurrentExecutions` < 200.
""",
}

print("War room template dictionary ready.")
