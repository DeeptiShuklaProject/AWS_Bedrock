

# Troubleshooting tenant isolation for Lambda functions
<a name="tenant-isolation-troubleshooting"></a>

This page addresses common issues that occur when using tenant isolation for AWS Lambda.

## InvalidParameterValueException
<a name="tenant-isolation-invalidparametervalueexception"></a>

**Error :** Tenant ID configuration not specified or passed to a function when tenant isolation is not enabled.

### Common causes
<a name="tenant-isolation-invalidparametervalueexception-cause"></a>

This error occurs when invoking a tenant-isolated function without a tenant ID, or invoking a non-tenant-isolated function with a tenant ID.

### Resolution
<a name="tenant-isolation-invalidparametervalueexception-resolution"></a>

Add a tenant ID if the function has tenant isolation enabled, or remove the tenant ID if the function doesn't have tenant isolation enabled.

## TooManyRequestsException
<a name="tenant-isolation-toomanyrequestsexception"></a>

**Error:** Rate exceeded

### Common causes
<a name="tenant-isolation-toomanyrequestsexception-cause"></a>

In addition to rate limiting based on [maximum concurrent executions](gettingstarted-limits.md#compute-and-storage) and [function scaling rate](scaling-behavior.md), Lambda limits the maximum number of tenant-aware execution environments (active or idle) that can exist at a time to 2,500 for every 1,000 concurrent executions of your function. 

### Resolution
<a name="tenant-isolation-toomanyrequestsexception-resolution"></a>

To fix this issue, you can either lower the rate at which invocation requests with unique tenant identifiers are made, [implement retries with backoff and jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), or [request a function concurrency limit increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).