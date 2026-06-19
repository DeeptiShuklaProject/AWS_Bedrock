

# Troubleshooting Amazon Bedrock API Error Codes
<a name="troubleshooting-api-error-codes"></a>

This section provides detailed information about the common errors you might encounter when using Amazon Bedrock APIs, the cause of the error, and the solution for resolving the error.

## AccessDeniedException
<a name="ts-access-denied"></a>

**HTTP Status Code: **403

**Cause: **You do not have sufficient permissions to perform the requested action.

**Solution:**
+ Verify that your IAM user or role has the necessary permissions for the action you are attempting.
+ If you are using temporary security credentials, ensure they haven't expired.

## FTUFormNotFilled
<a name="ts-ftu-form"></a>

**HTTP Status Code: **404

**Cause: **Model use case details have not been submitted for this account

**Solution:**
+ Fill out the Anthropic use case details form before using the model

## IncompleteSignature
<a name="ts-incomplete-signature"></a>

**HTTP Status Code: **400

**Cause:** The request signature does not conform to AWS standards.

**Solution:**
+ Ensure you are using an AWS SDK version that supports Amazon Bedrock.
+ Verify that your AWS access key ID and secret key are correctly configured.
+ If you are manually signing requests, we suggest double-checking your signature calculation process.

## InternalFailure
<a name="ts-internal-failure"></a>

**HTTP Status Code: **500

**Cause: **The request processing has failed due to a server error

**Solution:**
+ We suggest employing AWS recommended approach of using [retries with exponential backoff](https://docs.aws.amazon.com//prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) and random [jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) for improved reliability.
+ If the issue persists, please contact [AWS Support Center](https://aws.amazon.com/support) and provide details about your request and the error you are encountering.

## InvalidAction
<a name="ts-invalid-action"></a>

**HTTP Status Code: **400

**Cause: **The action or operation requested is invalid

**Solution:**
+ We suggest double-checking the spelling and formatting of the action name in your request.
+ Verify that the action calling is supported by Amazon Bedrock and is correctly documented as shown in [Amazon Bedrock API Reference.](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_Operations.html)
+ Ensure you are using the most up-to-date version of the AWS SDK or CLI.

## InvalidClientTokenId
<a name="ts-invalid-client-token"></a>

**HTTP Status Code: **403

**Cause: **The X.509 certificate or AWS access key ID provided does not exist in our records.

**Solution:**
+ Verify that you are using the correct AWS access key ID.
+ If you recently created new access keys, ensure you are using the new credentials and not the old ones.

## AWS Marketplace Agreement Failed within 15 minutes
<a name="ts-mp-agreement-failed"></a>

**HTTP Status Code: **403

**Cause: **The AWS Marketplace Agreement failed due to an underlying issue.

**Solution:**
+ Review the error message and remediate the underlying issue. Common underlying issues are invalid payment error and restricted geo-location.
+ For invalid payment error, please review [Restriction on credit and debit card purchases for AISPL customers using AWS Marketplace](https://aws.amazon.com/blogs/awsmarketplace/restriction-on-credit-and-debit-card-purchases-for-aispl-customers-using-aws-marketplace/) and [INVALID\_PAYMENT\_INSTRUMENT after requesting model access in Amazon Bedrock.](https://repost.aws/questions/QU0UOsutrWSSS4nOqgHcIUJg/invalid-payment-instrument-after-requesting-model-access-in-amazon-bedrock).

## AWS Marketplace Agreement Pending after 15 minutes
<a name="ts-mp-agreement-pending"></a>

**HTTP Status Code: **403

**Cause: **The AWS Marketplace Agreement has not succeeded and it has been 15 minutes since the request was made.

**Solution:**
+ Try the request again every 15 minutes. If the issue persists, please contact [AWS Support Center](https://aws.amazon.com/support) and provide details about your request and the error you are encountering.

## MPAgreementBeingCreated
<a name="ts-mp-agreement-created"></a>

**HTTP Status Code: **403

**Cause: **Your account is not authorized to access this model. Your AWS Marketplace subscription for this model is still being processed

**Solution:**
+ Try again after 15 minutes

## NotAuthorized
<a name="ts-not-authorized"></a>

**HTTP Status Code: **400

**Cause: **You do not have permission to perform this action.

**Solution:**
+ Review your IAM permissions and ensure you have the necessary rights to perform the requested action on Amazon Bedrock resources.
+ If you are using an IAM role, verify that the role has the appropriate permissions and trust relationships.
+ Check for any organizational policies or service control policies that might be restricting your access.

## RequestExpired
<a name="ts-request-expired"></a>

**HTTP Status Code: **400

**Cause: **The request is no longer valid due to expired timestamps.

**Solution:**
+ Ensure your system clock is correctly synchronized with a reliable time source.
+ If you are making requests from different time zones, be aware of potential timestamp discrepancies.

## ServiceUnavailable
<a name="ts-service-unavailable"></a>

**HTTP Status Code: **503

**Cause: **The service is temporarily unable to handle the request. 503 errors indicate that the service is experiencing high demand or temporary capacity constraints. This is not related to your account-level quotas or rate limits (which return 429 ThrottlingException).

**Solution:**
+ We suggest employing AWS recommended approach of using [retries with exponential backoff](https://docs.aws.amazon.com//prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) and random [jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) for improved reliability.
+ Consider switching to a different AWS Region if the issue persists in your current Region. Different Regions may have varying levels of load and availability.
+ [Use Cross-Region inference](https://docs.aws.amazon.com//bedrock/latest/userguide/cross-region-inference.html) to seamlessly manage unplanned traffic bursts by using compute across different AWS Regions.
+ If you have high throughput requirements, we suggest exploring [Provisioned Throughput](https://docs.aws.amazon.com//bedrock/latest/userguide/prov-throughput.html) for your use case.

**Best practices**
+ Ensure your application can handle 503 status codes appropriately in your error handling and retry logic.
+ Check the AWS Service Health Dashboard for any announced issues or scheduled maintenance that might affect the service.

If you experience frequent 503 errors or if they significantly impact your operations, please contact [AWS Support](https://aws.amazon.com/support)for further assistance and guidance tailored to your specific use case.

## ThrottlingException
<a name="ts-throttling-exception"></a>

**HTTP Status Code: **429

**Cause: **The request was denied due to exceeding the account quotas for Amazon Bedrock.

**Solution:**
+ Check the Amazon Bedrock service quotas in the [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) console to learn about the limits allotted to your account.
+ We suggest employing AWS recommended approach of using [retries with exponential backoff.](https://docs.aws.amazon.com//prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) and random [jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) for improved reliability.
+ If you have high throughput requirements, we suggest exploring [Provisioned Throughput](https://docs.aws.amazon.com//bedrock/latest/userguide/prov-throughput.html) for your use case.
+ Request for quota increase by contacting your account manager or [AWS Support](https://aws.amazon.com/support) if your workload traffic exceeds your account quotas.

## ValidationError
<a name="ts-validation-error"></a>

**HTTP Status Code: **400

**Cause: **The input fails to satisfy the constraints specified by Amazon Bedrock.

**Solution:**
+ Review the API documentation to ensure all required parameters are included and formatted correctly.
+ Check that your input values are within the allowed ranges or conform to the expected patterns.
+ We suggest paying attention to any specific validation rules mentioned in the API reference for the action you are using.

## ResourceNotFound
<a name="ts-resource-not-found"></a>

**HTTP Status Code: **404

**Cause: **The requested resource could not be found.

**Solution:**
+ Verify the correctness of model ID, endpoint name, or other resource identifiers in your request.
+ Please implement a fallback mechanism to use alternative models or endpoints when a primary resource is not found.

**Best practices**
+ Use [ListFoundationModels](https://docs.aws.amazon.com//bedrock/latest/APIReference/API_ListFoundationModels.html) to learn about the available Amazon Bedrock foundation models that you can use.
+ We suggest implementing a periodic synchronization process to update your local resource catalog.

If you continue to experience issues after trying these solutions, contact [AWS Support](https://aws.amazon.com/support)for further assistance and guidance tailored to your specific use case.

## Connection timeout or reset on long-running or idle connections
<a name="ts-connection-timeout"></a>

**Symptom: **API calls fail with connection resets or timeouts, especially for long-running requests such as streaming, extended thinking, or large inference responses, when traffic goes through NAT Gateways, interface VPC endpoints, or Network Load Balancers. Symptoms can also appear as long cold-start latency (for example, the first call after an idle period takes 70\+ seconds instead of the usual few) when an idle pooled connection is reused after the network has silently dropped it.

**Cause: **NAT Gateways, interface VPC endpoints, and Network Load Balancers have a fixed idle connection timeout of 350 seconds. If a TCP connection remains idle longer than this period, the connection is dropped without notifying the client. The client may not detect the dropped connection until the next request, at which point it must wait for the OS-level TCP retry or timeout before reestablishing the connection.

**When this applies:**
+ Applications running on Amazon EKS or Amazon ECS where pod traffic to Amazon Bedrock egresses through a NAT Gateway or VPC interface endpoint.
+ Applications running on Amazon EC2 instances behind a NAT Gateway, an interface VPC endpoint for Amazon Bedrock, or a Network Load Balancer.
+ Long-running or bursty workloads where Amazon Bedrock client connections sit idle in a connection pool between calls.

**Solution:**

Enabling TCP keep-alive on the Amazon Bedrock client requires *two* settings working together. Setting only one is not enough.

1. **Enable TCP keep-alive in your AWS SDK client.** The boto3 `Config` object accepts a `tcp_keepalive` parameter, which defaults to `False`. Set it to `True` when constructing the Amazon Bedrock client:

   ```
   import boto3
   from botocore.config import Config
   
   config = Config(tcp_keepalive=True)
   client = boto3.client("bedrock-runtime", config=config)
   ```

   For other AWS SDKs, see the corresponding HTTP client configuration documentation.

1. **Configure the OS-level keep-alive interval to fire before the 350-second idle timeout.** Linux defaults to `net.ipv4.tcp_keepalive_time = 7200` (2 hours), which is much longer than the NAT or VPC endpoint idle timeout, so SDK-level keep-alive alone has no effect. Lower the kernel setting to a value safely below 350 seconds (for example, 45 seconds):

   ```
   sysctl -w net.ipv4.tcp_keepalive_time=45
   ```

   On Amazon EKS and Amazon ECS, apply the sysctl in the pod or task `securityContext`, in an init container, or in a custom node AMI. On Amazon EC2, set it in `/etc/sysctl.d/` so the value persists across reboots.

For a deeper discussion of long-running TCP connections in VPC networking, see [Implementing long-running TCP Connections within VPC networking](https://aws.amazon.com/blogs/networking-and-content-delivery/implementing-long-running-tcp-connections-within-vpc-networking/) on the AWS Networking & Content Delivery Blog.

If you continue to experience connection issues after applying both settings, contact [AWS Support](https://aws.amazon.com/support) for further assistance.