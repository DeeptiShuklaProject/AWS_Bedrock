

# Observability for managed knowledge bases
<a name="kb-managed-observability"></a>

For a managed knowledge base, Amazon Bedrock publishes operational metrics and ingestion logs to your AWS account so that you can monitor the health and usage of your knowledge base. Runtime metrics let you track request volume, errors, and throttling for your knowledge base API operations, and ingestion logs let you track the status of individual documents during a data ingestion job. The following sections describe the observability data that is available and how to access it.

## Runtime metrics for managed knowledge bases
<a name="kb-managed-observability-runtime-metrics"></a>

Amazon Bedrock publishes runtime metrics for your knowledge base API operations to Amazon CloudWatch under the `AWS/Bedrock/KnowledgeBases` namespace. Use these metrics to monitor invocation volume, error rates, and throttling for operations such as `Retrieve`. Metrics are published to your account at no additional charge and appear in the CloudWatch console.

The following table describes the runtime metrics that Amazon Bedrock publishes for managed knowledge bases.


| Metric name | Unit | Description | 
| --- | --- | --- | 
| Invocations | Count | Number of requests to the knowledge base operation. This metric is published for every request, including requests that result in an error. | 
| ClientErrors | Count | Number of requests that resulted in a client-side error (an HTTP `4xx` response other than throttling). | 
| ServerErrors | Count | Number of requests that resulted in a server-side error (an HTTP `5xx` response). | 
| Throttles | Count | Number of requests that were throttled (an HTTP `429` response). Throttled requests are not counted as `ClientErrors` or `ServerErrors`. | 

The `ClientErrors`, `ServerErrors`, and `Throttles` metrics are published only when the corresponding condition occurs. The `Invocations` metric is published for every request.

### Additional metric for the AgenticRetrieveStream operation
<a name="kb-managed-observability-runtime-metrics-agentic"></a>

In addition to the metrics in the preceding table, the `AgenticRetrieveStream` operation publishes the following metric.


| Metric name | Unit | Description | 
| --- | --- | --- | 
| TotalIterationCount | Count | The total number of agentic retrieval iterations performed during the request. This metric is published only for the `AgenticRetrieveStream` operation, when the request completes successfully. | 

This metric uses the `Operation` dimension with a value of `AgenticRetrieveStream`.

### Dimensions for managed knowledge base metrics
<a name="kb-managed-observability-runtime-metrics-dimensions"></a>

Amazon Bedrock uses the following dimensions for managed knowledge base runtime metrics.


| Dimension | Description | 
| --- | --- | 
| Operation | The knowledge base API operation that the metric is published for. Possible values are `Retrieve` and `AgenticRetrieveStream`. | 
| KnowledgeBaseId | The knowledge base that the request targets, in the format `knowledge-base/{{knowledge-base-id}}`. This dimension is included for the `Retrieve` operation, which targets a single knowledge base. Operations that do not target a single knowledge base are published with the `Operation` dimension only. | 

### Permissions for publishing metrics
<a name="kb-managed-observability-runtime-metrics-permissions"></a>

Amazon Bedrock publishes these metrics to your account using the credentials associated with the request:
+ For the `Retrieve` operation, Amazon Bedrock uses the knowledge base service role.
+ For other operations, Amazon Bedrock uses the credentials of the calling identity (the IAM user or role that calls the operation), through a forward access session.

For metrics to be published, that identity must be allowed to call `cloudwatch:PutMetricData` for the `AWS/Bedrock/KnowledgeBases` namespace. Attach a policy that grants this permission to the knowledge base service role and to any identity that calls the knowledge base operations. The following example grants the required permission.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricData",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "cloudwatch:namespace": "AWS/Bedrock/KnowledgeBases"
                }
            }
        }
    ]
}
```

Metric publishing is best effort. If the identity does not have the required permission, the corresponding metrics are not published, but the knowledge base request itself is not affected.

### View runtime metrics
<a name="kb-managed-observability-runtime-metrics-view"></a>

You can get metrics for your knowledge base with the AWS Management Console, the AWS CLI, or the CloudWatch API. You can use the CloudWatch API through one of the AWS Software Development Kits (SDKs) or the CloudWatch API tools.

To view managed knowledge base metrics in the CloudWatch console, go to the metrics section in the navigation pane and select the all metrics option, then search for the `AWS/Bedrock/KnowledgeBases` namespace.

You must have the appropriate CloudWatch permissions to monitor your knowledge base with CloudWatch. For more information, see [Authentication and Access Control for Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) in the *Amazon CloudWatch User Guide*.

## Storage metrics for managed knowledge bases
<a name="kb-managed-observability-storage-metrics"></a>

For a managed knowledge base, Amazon Bedrock publishes a storage metric to Amazon CloudWatch under the `AWS/Bedrock/KnowledgeBases` namespace. This metric reports the total raw size of the source data stored in the knowledge base, and is published to your account after a data ingestion job completes, so that you can track how much data is stored in your knowledge base over time.

The following table describes the storage metric that Amazon Bedrock publishes for managed knowledge bases.


| Metric name | Unit | Description | 
| --- | --- | --- | 
| RawDataSize  | Gigabytes | The total raw size of the source data stored in the knowledge base, in gigabytes. This metric is published after a data ingestion job completes. | 

The storage metric uses the `KnowledgeBaseId` dimension, in the format `knowledge-base/{{knowledge-base-id}}`.

## Ingestion observability for managed knowledge bases
<a name="kb-managed-observability-ingestion"></a>

Amazon Bedrock emits logs that track the progress of a data ingestion job for your managed knowledge base, including the overall job status and the status of each document that is processed. You can use these logs to confirm which documents were ingested, investigate why a document was not returned in retrieval results, and troubleshoot ingestion failures.

Logs are delivered to a destination that you configure (CloudWatch Logs, Amazon S3, or Amazon Data Firehose). The following sections describe how to enable log delivery, the lifecycle of a document during ingestion, the log types that are emitted, and example queries.

### Enable ingestion log delivery
<a name="kb-managed-observability-ingestion-enable"></a>

To receive ingestion logs, configure a log delivery for your knowledge base using either the AWS Management Console or the CloudWatch API. You can deliver logs to CloudWatch Logs, Amazon S3, or Amazon Data Firehose.

#### Enable log delivery using the console
<a name="kb-managed-observability-ingestion-enable-console"></a>

1. **Open your knowledge base**: In the Amazon Bedrock console, open the managed knowledge base that you want to monitor.

1. **Add a log delivery**: Edit the knowledge base to add a log delivery, and configure the following details:
   + The logging destination (CloudWatch Logs, Amazon S3, or Amazon Data Firehose).
   + (CloudWatch Logs) The log group name.
   + (Amazon S3) The bucket name.
   + (Amazon Data Firehose) The Firehose stream.

1. **Confirm delivery status**: Verify that the log delivery status is *Delivery active* in the console.

#### Enable log delivery using the CloudWatch API
<a name="kb-managed-observability-ingestion-enable-api"></a>

1. **Get the ARN of your knowledge base**: Call the [GetKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_GetKnowledgeBase.html) API to get the Amazon Resource Name (ARN) of the knowledge base. A knowledge base ARN has the following format: {{arn:aws:bedrock:your-region:your-account-id:knowledge-base/knowledge-base-id}}.

1. **Call `PutDeliverySource`**: Use the [PutDeliverySource](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliverySource.html) API to create a delivery source for the knowledge base. Pass the knowledge base ARN as the `resourceArn` and specify `APPLICATION_LOGS` as the `logType`.

   ```
   {
       "logType": "APPLICATION_LOGS",
       "name": "my-knowledge-base-delivery-source",
       "resourceArn": "arn:aws:bedrock:your-region:your-account-id:knowledge-base/knowledge_base_id"
   }
   ```

1. **Call `PutDeliveryDestination`**: Use the [PutDeliveryDestination](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestination.html) API to configure where the logs are stored. Specify the ARN of a CloudWatch Logs, Amazon S3, or Amazon Data Firehose destination. You can set `outputFormat` to `json`, `plain`, `w3c`, `raw`, or `parquet`.

   ```
   {
      "deliveryDestinationConfiguration": {
         "destinationResourceArn": "arn:aws:s3:::bucket-name"
      },
      "name": "my-knowledge-base-delivery-destination",
      "outputFormat": "json"
   }
   ```

   If you are delivering logs to a different account, use the `PutDeliveryDestinationPolicy` API to attach an AWS Identity and Access Management (IAM) policy to the destination account.

1. **Call `CreateDelivery`**: Use the [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html) API to link the delivery source to the delivery destination.

   ```
   {
      "deliveryDestinationArn": "string",
      "deliverySourceName": "my-knowledge-base-delivery-source"
   }
   ```

#### Supported log types and permissions
<a name="kb-managed-observability-ingestion-enable-logtypes"></a>

Managed knowledge bases support the following log types:
+ `APPLICATION_LOGS`: Logs that track the status of the ingestion job and of each document that is processed during the job.
+ `TRACES`: Distributed traces (spans) for runtime operations. Traces are emitted only for the `Retrieve` operation and are delivered to AWS X-Ray. For more information, see [Trace observability for managed knowledge bases](#kb-managed-observability-traces).

To enable log delivery, the user or role must have the `bedrock:AllowVendedLogDeliveryForResource` permission for the knowledge base resource, in addition to the permissions required to write to your chosen destination. For example IAM policies for each destination, see [Vended logs permissions for different delivery destinations](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html#AWS-vended-logs-permissions-V2) in the *Amazon CloudWatch Logs User Guide*.

### Document lifecycle during ingestion
<a name="kb-managed-observability-ingestion-lifecycle"></a>

During a data ingestion job, each document moves through three stages, and the log for the document records the status of each stage:
+ **Crawl** (`crawl_status`): Amazon Bedrock retrieves the document from the data source and determines whether it must be added, updated, or deleted. The `crawl_action` field is set to `ADD`, `DELETE`, or `UNMODIFIED`. A document that is `UNMODIFIED` is skipped in the remaining stages.
+ **Sync** (`sync_status`): the document is submitted for processing into the knowledge base.
+ **Index** (`index_status`): the document is chunked, embedded, and persisted in the knowledge base. The `chunk_statistics` field summarizes the chunks that were created or deleted.

Each stage status is `SUCCESS` or `FAILED`. The `connector_document_status` field reports the consolidated status of the document, and the `error_message` field is populated only when a document fails to process.

### Log types and examples
<a name="kb-managed-observability-ingestion-example-log"></a>

Amazon Bedrock emits two kinds of log entries for a managed knowledge base ingestion job, distinguished by the `event_type` field:
+ `StartIngestionJob.StatusChanged` – job-level logs that record the progress of the overall ingestion job, such as when crawling starts and completes. The `message` field contains a human-readable status, for example `Crawling started` or `Crawling completed`.
+ `StartIngestionJob.ResourceStatusChanged` – document-level logs that record the processing status of an individual document.

The following is an example of a job-level status log.

```
{
    "event_timestamp": 1718677300000,
    "event": {
        "ingestion_job_id": "<IngestionJobId>",
        "data_source_id": "<DataSourceId>",
        "knowledge_base_arn": "arn:aws:bedrock:<region>:<accountId>:knowledge-base/<KnowledgeBaseId>",
        "message": "Crawling started"
    },
    "event_version": "1.0",
    "event_type": "StartIngestionJob.StatusChanged",
    "level": "INFO"
}
```

The following is an example of a document-level log that records the processing status of a single document.

```
{
    "event_timestamp": 1718677342332,
    "event": {
        "ingestion_job_id": "<IngestionJobId>",
        "data_source_id": "<DataSourceId>",
        "knowledge_base_arn": "arn:aws:bedrock:<region>:<accountId>:knowledge-base/<KnowledgeBaseId>",
        "document_id": "<DocumentId>",
        "source_uri": "<SourceUri>",
        "content_type": "<ContentType>",
        "crawl_action": "ADD" | "DELETE" | "UNMODIFIED",
        "index_status": { "Status": "SUCCESS" | "FAILED", "UpdatedTime": "<epochMillis>" },
        "crawl_status": { "Status": "SUCCESS" | "FAILED", "UpdatedTime": "<epochMillis>" },
        "sync_status": { "Status": "SUCCESS" | "FAILED", "UpdatedTime": "<epochMillis>" },
        "chunk_statistics": {
            "created": int,
            "deleted": int,
            "failed_to_create": int,
            "failed_to_delete": int
        },
        "error_message": "<ErrorMessage>"
    },
    "event_version": "1.0",
    "event_type": "StartIngestionJob.ResourceStatusChanged",
    "level": "INFO" | "ERROR"
}
```

The `error_message` field is present only when a document fails to process. The `chunk_statistics` field summarizes the chunks that were created or deleted for the document.

Some document-level logs report a connector status message instead of the status fields shown above. These logs include a `message` field with a human-readable description (for example, a message indicating that a document could not be fetched or deleted) and a `level` of `INFO`, `WARN`, or `ERROR`.

### Example queries
<a name="kb-managed-observability-ingestion-queries"></a>

If you deliver logs to CloudWatch Logs, you can use CloudWatch Logs Insights to query the ingestion logs for your knowledge base. The following are some common queries.
+ List all documents that failed to process during ingestion, with their error messages.

  `filter event.connector_document_status.Status = "FAILED" | fields event.document_id, event.source_uri, event.error_message, @timestamp | sort @timestamp desc`
+ Find all log entries for a specific document by its source location.

  `filter event.source_uri = "s3://<bucketName>/<objectKey>" | fields event.document_id, event.connector_document_status.Status, @timestamp | sort @timestamp desc`
+ List all documents processed by a specific ingestion job.

  `filter event.ingestion_job_id = "<IngestionJobId>" | fields event.document_id, event.connector_document_status.Status, @timestamp | sort @timestamp desc`
+ View the overall progress of an ingestion job, including when crawling started and completed.

  `filter event_type = "StartIngestionJob.StatusChanged" | fields event.message, @timestamp | sort @timestamp asc`

## Trace observability for managed knowledge bases
<a name="kb-managed-observability-traces"></a>

Amazon Bedrock can emit distributed traces (spans) for knowledge base runtime operations so that you can analyze request latency and the internal steps of a request. Traces are emitted only for the `Retrieve` operation and are delivered to [AWS X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html). Trace delivery uses the same vended log delivery pipeline as ingestion logs, with the `TRACES` log type and an X-Ray delivery destination.

### Enable trace delivery using the CloudWatch API
<a name="kb-managed-observability-traces-enable"></a>

To deliver traces to AWS X-Ray, use the CloudWatch API to create a delivery, following these steps.

1. **Call `PutDeliverySource`**: Use the [PutDeliverySource](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliverySource.html) API to create a delivery source for the knowledge base. Pass the knowledge base ARN as the `resourceArn` and specify `TRACES` as the `logType`.

1. **Call `PutDeliveryDestination`**: Use the [PutDeliveryDestination](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestination.html) API with a `deliveryDestinationType` of `XRAY`. X-Ray is a managed destination, so you do not specify a `destinationResourceArn`. Note the ARN that is returned in the response.

1. **Call `CreateDelivery`**: Use the [CreateDelivery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html) API to link the delivery source name to the X-Ray delivery destination ARN.

**Note**  
These API calls are idempotent. If a resource already exists, you can safely ignore a `ConflictException` or `ResourceAlreadyExistsException`.

### Permissions for trace delivery
<a name="kb-managed-observability-traces-permissions"></a>

To enable trace delivery, the user or role must have the `bedrock:AllowVendedLogDeliveryForResource` permission for the knowledge base resource, in addition to the permissions required to deliver to AWS X-Ray.

### View traces
<a name="kb-managed-observability-traces-view"></a>

After you enable trace delivery, call the `Retrieve` operation to generate traces, and then view them in the AWS X-Ray console.

## AgentCore observability for managed knowledge bases
<a name="kb-managed-observability-agentcore"></a>

Amazon Bedrock integrates managed knowledge base observability data with the Amazon Bedrock AgentCore observability experience, giving you a consolidated view of your knowledge base metrics and traces alongside your other AgentCore telemetry.

No additional configuration is required for this integration. After you enable runtime metrics and trace delivery as described in the preceding sections, your AgentCore observability page populates automatically with the corresponding knowledge base data. There are no extra actions to take.

**Note**  
AgentCore observability integration is available only for managed knowledge bases.

## Customer support and troubleshooting
<a name="kb-managed-observability-support"></a>

Amazon Bedrock Managed Knowledge Bases temporarily stores customer queries and associated retrieval data solely to provide debugging support in response to customer-reported issues. AWS does not access this data unless the customer explicitly consents during a support engagement. Amazon Bedrock does not use this data for training or improving underlying models.