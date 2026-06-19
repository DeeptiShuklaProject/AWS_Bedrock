

# Monitor Amazon Bedrock Guardrails using CloudWatch metrics
<a name="monitoring-guardrails-cw-metrics"></a>

The following table describes runtime metrics provided by Amazon Bedrock Guardrails that you can monitor with Amazon CloudWatch metrics.

**Runtime metrics**


| Metric name | Unit | Description | 
| --- | --- | --- | 
| Invocations | SampleCount | Number of requests to the ApplyGuardrail API operation | 
| InvocationLatency | MilliSeconds | The time from when a request is sent to when the last token is received. | 
| InvocationClientErrors | SampleCount | Number of invocations that result in client-side errors | 
| InvocationServerErrors | SampleCount | Number of invocations that result in AWS server-side errors | 
| InvocationThrottles | SampleCount | Number of invocations that the system throttled. Throttled requests don't count as invocations or errors | 
| TextUnitCount | SampleCount | Number of text units consumed by the guardrails policies | 
| InvocationsIntervened | SampleCount | Number of invocations where the guardrails intervened | 
| FindingCounts | SampleCount | Counts for each type of finding from InvokeAutomatedReasoningCheck | 
| TotalFindings | SampleCount | Counts number of findings produced for each InvokeAutomatedReasoningCheck request | 
| Invocations (AutomatedReasoning) | SampleCount | Number of requests to InvokeAutomatedReasoningCheck | 
| Latency | MilliSeconds | Latency of verification using automated reasoning policy | 

You can view guardrail dimensions in the CloudWatch console based on the table below:

**Dimension**


| Dimension name | Dimension values | Available for the following metrics | 
| --- | --- | --- | 
| Operation | ApplyGuardrail |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| GuardrailContentSource |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| GuardrailPolicyType |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| GuardrailArn, GuardrailVersion |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| FindingType \+ PolicyArn \+ PolicyVersion | FindingType \+ PolicyArn \+ PolicyVersion |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| FindingType \+ GuardrailArn \+ GuardrailVersion | FindingType \+ GuardrailArn \+ GuardrailVersion |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| PolicyArn \+ PolicyVersion | PolicyArn \+ PolicyVersion |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 
| GuardrailArn \+ GuardrailVersion | GuardrailArn \+ GuardrailVersion |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html)  | 

**Get CloudWatch metrics for guardrails**

You can get metrics for guardrails with the AWS Management Console, the AWS CLI, or the CloudWatch API. You can use the CloudWatch API through one of the AWS Software Development Kits (SDKs) or the CloudWatch API tools. 

The namespace for guardrail metrics in CloudWatch is `AWS/Bedrock/Guardrails`.

**Note**  
You must have the appropriate CloudWatch permissions to monitor guardrails with CloudWatch. For more information, see [Authentication and Access Control for CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) in the CloudWatch User Guide. 

**View guardrails metrics in the CloudWatch console**

1. Sign in to the AWS Management Console and open the CloudWatch console at https://console.aws.amazon.com/cloudwatch/.

1. Choose the `AWS/Bedrock/Guardrails` namespace.