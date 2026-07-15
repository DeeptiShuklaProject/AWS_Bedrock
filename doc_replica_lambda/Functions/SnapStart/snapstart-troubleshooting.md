

# Troubleshooting SnapStart errors for Lambda functions
<a name="snapstart-troubleshooting"></a>

This page addresses common issues that occur when using Lambda SnapStart, including snapshot creation errors, timeout errors, and internal service errors.

## SnapStartNotReadyException
<a name="snapstartnotreadyexception"></a>

**Error:** An error occurred (SnapStartNotReadyException) when calling the Invoke20150331 operation: Lambda is initializing your function. It will be ready to invoke once your function state becomes ACTIVE.

### Common causes
<a name="snapstartnotreadyexception-cause"></a>

This error occurs when you try to invoke a function version that is in the `Inactive` [state](snapstart-activate.md#snapstart-function-states). Your function version becomes `Inactive` when it hasn't been invoked for 14 days or when Lambda periodically recycles the execution environment

### Resolution
<a name="snapstartnotreadyexception-resolution"></a>

Wait until the function version reaches the `Active` state, and then invoke it again.

## SnapStartTimeoutException
<a name="snapstart-invocation-failure"></a>

**Issue:** You receive a `SnapStartTimeoutException` when you try to invoke a SnapStart function version.

### Common cause
<a name="snapstart-invocation-failure-cause"></a>

During the [Restore](lambda-runtime-environment.md#runtimes-lifecycle-restore) phase, Lambda restores the Java runtime and runs any after-restore [runtime hooks](snapstart-runtime-hooks.md). If an after-restore runtime hook runs for longer than 10 seconds, the `Restore` phase times out and you get an error when you try to invoke the function. Network connection and credentials issues can also cause `Restore` phase timeouts.

### Resolution
<a name="snapstart-invocation-failure-resolution"></a>

Check the function's CloudWatch logs for timeout errors that happened during the [Restore](lambda-runtime-environment.md#runtimes-lifecycle-restore) phase. Make sure that all after-restore hooks complete in less than 10 seconds.

**Example CloudWatch log**  

```
{ "cause": "Lambda couldn't restore the snapshot within the timeout limit. (Service: Lambda, Status Code: 408, Request ID: 11a222c3-410f-427c-ab22-931d6bcbf4f2)", "error": "Lambda.SnapStartTimeoutException"}
```

## 500 Internal Service Error
<a name="snapstart-500-error"></a>

**Error:** Lambda was unable to create a new snapshot because you have reached your concurrent snapshot creation limit.

### Common cause
<a name="snapstart-500-error-cause"></a>

A 500 error is an internal error within the Lambda service itself, rather than an issue with your function or code. These errors are often intermittent.

### Resolution
<a name="snapstart-500-error-resolution"></a>

Try to publish the function version again.

## 401 Unauthorized
<a name="snapstart-401-unauthorized"></a>

**Error:** Bad session token or header key

### Common cause
<a name="snapstart-401-unauthorized-cause"></a>

This error occurs when using the [AWS Systems Manager Parameter Store and AWS Secrets Manager extension](with-secrets-manager.md) with Lambda SnapStart.

### Resolution
<a name="snapstart-401-unauthorized-resolution"></a>

The AWS Systems Manager Parameter Store and AWS Secrets Manager extension isn't compatible with SnapStart. The extension generates credentials for communicating with AWS Secrets Manager during function initialization, which causes expired credential errors when used with SnapStart.

## UnknownHostException (Java)
<a name="snapstart-dns-caching"></a>

**Error:** Unable to execute HTTP request: Certificate for `abc.us-east-1.amazonaws.com` doesn't match any of the subject alternative names.

### Common cause
<a name="snapstart-dns-caching-cause"></a>

Lambda functions already cache DNS responses. If you use another DNS cache with SnapStart, then you might experience connection timeouts when the function resumes from a snapshot.

### Resolution
<a name="snapstart-dns-caching-resolution"></a>

To prevent `UnknownHostException` failures in the Java 11 runtime, we recommend setting `networkaddress.cache.negative.ttl` to 0. In Java 17 and later runtimes, this step isn't necessary. You can set this property for a Lambda function with the `AWS_LAMBDA_JAVA_NETWORKADDRESS_CACHE_NEGATIVE_TTL=0` environment variable.

## Snapshot creation failures
<a name="snapstart-creation-failure"></a>

**Error:** AWS Lambda could not invoke your SnapStart function. If this error persists, check your function's CloudWatch logs for initialization errors.

### Resolution
<a name="snapstart-creation-failure-resolution"></a>

Review your function's Amazon CloudWatch logs for before-checkpoint [runtime hook](snapstart-runtime-hooks.md) timeouts. You can also try publishing a new function version, which can sometimes resolve the issue.

## Snapshot creation latency
<a name="snapstart-creation-latency"></a>

**Issue:** When you publish a new function version, the function stays in the `Pending` [state](snapstart-activate.md#snapstart-function-states) for a long time.

### Common cause
<a name="snapstart-creation-latency-cause"></a>

When Lambda creates a snapshot, your initialization code can run for up to 15 minutes. The time limit is 130 seconds or the [configured function timeout](configuration-timeout.md) (maximum 900 seconds), whichever is higher.

If your function is [attached to a VPC](configuration-vpc.md#configuration-vpc-attaching), Lambda might also need to create network interfaces before the function becomes `Active`. If you try to invoke the function version while the function is `Pending`, you might get a 409 `ResourceConflictException`. If the function is invoked using an Amazon API Gateway endpoint, you might get a 500 error in API Gateway.

### Resolution
<a name="snapstart-creation-latency-resolution"></a>

Wait at least 15 minutes for the function version to initialize before invoking it.