

# Configure streaming response behavior to filter content
<a name="guardrails-streaming"></a>

The [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) API returns data in a streaming format. This allows you to access responses in chunks without waiting for the entire result. When using guardrails with a streaming response, there are two modes of operation: synchronous and asynchronous.

**Synchronous mode**

In the default synchronous mode, guardrails will buffer and apply the configured policies to one or more response chunks before the response is sent back to the user. The synchronous processing mode introduces some latency to the response chunks, as it means that the response is delayed until the guardrails scan completes. However, it provides better accuracy, as every response chunk is scanned by guardrails before being sent to the user.

**Asynchronous mode**

In asynchronous mode, guardrails sends the response chunks to the user as soon as they become available, while asynchronously applying the configured policies in the background. The advantage is that response chunks are provided immediately with no latency impact, but response chunks may contain inappropriate content until guardrails scan completes. As soon as inappropriate content is identified, subsequent chunks will be blocked by guardrails.

**Warning**  
Amazon Bedrock Guardrails doesn't support the masking of sensitive information with asynchronous mode.

**Enabling asynchronous mode**

To enable asynchronous mode, you need to include the `streamProcessingMode` parameter in the `amazon-bedrock-guardrailConfig` object of your `InvokeModelWithResponseStream` request:

```
{
   "amazon-bedrock-guardrailConfig": {
   "streamProcessingMode": "ASYNCHRONOUS"
   }
}
```

By understanding the trade-offs between the synchronous and asynchronous modes, you can choose the appropriate mode based on your application's requirements for latency and content moderation accuracy.