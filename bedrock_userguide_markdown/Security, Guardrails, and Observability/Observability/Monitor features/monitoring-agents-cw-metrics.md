

# Monitor Amazon Bedrock Agents using CloudWatch Metrics
<a name="monitoring-agents-cw-metrics"></a>

The following table describes runtime metrics provided by Amazon Bedrock Agents that you can monitor with Amazon CloudWatch Metrics.

**Runtime metrics**


****  

| Metric name | Unit | Description | 
| --- | --- | --- | 
| InvocationCount | SampleCount | Number of requests to the API operation | 
| TotalTime | Milliseconds | The time it took for the server to process the request | 
| TTFT | Milliseconds | Time-to-first-token metric. Emitted when Streaming configuration is enabled for an invokeAgent or invokeInlineAgent request | 
| InvocationThrottles | SampleCount | Number of invocations that the system throttled. Throttled requests and other invocation errors don't count as either Invocations or Errors. | 
| InvocationServerErrors | SampleCount | Number of invocations that result in AWS server-side errors | 
| InvocationClientErrors | SampleCount | Number of invocations that result in client-side errors | 
| ModelLatency | Milliseconds | The latency of the model | 
| ModelInvocationCount | SampleCount | Number of requests that the agent made to the model | 
| ModelInvocationThrottles | SampleCount | Number of model invocations that the Amazon Bedrock core throttled. Throttled requests and other invocation errors don't count as either Invocations or Errors. | 
| ModelInvocationClientErrors | SampleCount | Number of model invocations that result in client-side errors | 
| ModelInvocationServerErrors | SampleCount | Number of model invocations that result in AWS server-side errors | 
| InputTokenCount | SampleCount | Number of tokens input to the model. | 
| outputTokenCount | SampleCount | Number of tokens ouptut from the model. | 

You can view agent dimensions in the CloudWatch console based on the table below:

**Dimension**


****  

| Dimension name | Dimension values | Available for the following metrics | 
| --- | --- | --- | 
| Operation | [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html), [InvokeInlineAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeInlineAgent.html) |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-agents-cw-metrics.html)  | 
| Operation, ModelId | Any Amazon Bedrock agent operation listed in the Operation dimension and the  modelId of any Amazon Bedrock core model |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-agents-cw-metrics.html)  | 
| Operation, AgentAliasArn, ModelId | Any Amazon Bedrock agent operation listed in the Operation dimension and any modelId of an Amazon Bedrock model, grouped by the agentAliasArn of an agent alias  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-agents-cw-metrics.html)  | 

**Use CloudWatch metrics for agents**

You can get metrics for agents with the AWS Management Console, the AWS CLI, or the CloudWatch API. You can use the CloudWatch API through one of the AWS Software Development Kits (SDKs) or the CloudWatch API tools. 

The namespace for agent metrics in CloudWatch is `AWS/Bedrock/Agents`.

You must have the appropriate CloudWatch permissions to monitor agents with CloudWatch. For more information, see [Authentication and Access Control for CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) in the CloudWatch User Guide. 

**Important**  
If you don’t want CloudWatch to use collected data for CloudWatch service improvement, you can create an opt out policy. For more information, [AI services opt-out policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html).

If you aren't seeing metrics published in the CloudWatch dashboard, make sure the IAM service role that you used to [create](agents-create.md) the agent has the following policy.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": {
        "Effect": "Allow",
        "Resource": "*",
        "Action": "cloudwatch:PutMetricData",
        "Condition": {
            "StringEquals": {
                "cloudwatch:namespace": "AWS/Bedrock/Agents"
            }
        }
    }
}
```

------