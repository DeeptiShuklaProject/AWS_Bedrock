

# Sending Lambda function logs to CloudWatch Logs
<a name="monitoring-cloudwatchlogs"></a>

By default, Lambda automatically captures logs for all function invocations and sends them to CloudWatch Logs, provided your function's execution role has the necessary permissions. These logs are, by default, stored in a log group named /aws/lambda/{{<function-name>}}. To enhance debugging, you can insert custom logging statements into your code, which Lambda will seamlessly integrate with CloudWatch Logs. If needed, you can configure your function to send logs to a different group using the Lambda console, AWS CLI, or Lambda API. See [Configuring CloudWatch log groups](monitoring-cloudwatchlogs-loggroups.md) to learn more.

You can view logs for Lambda functions using the Lambda console, the CloudWatch console, the AWS Command Line Interface (AWS CLI), or the CloudWatch API. For more information, see to [Viewing CloudWatch logs for Lambda functions](monitoring-cloudwatchlogs-view.md).

**Note**  
It may take 5 to 10 minutes for logs to show up after a function invocation.

## Required IAM permissions
<a name="monitoring-cloudwatchlogs-prereqs"></a>

Your [execution role](lambda-intro-execution-role.md) needs the following permissions to upload logs to CloudWatch Logs:
+ `logs:CreateLogGroup`
+ `logs:CreateLogStream`
+ `logs:PutLogEvents`

To learn more, see [Using identity-based policies (IAM policies) for CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/iam-identity-based-access-control-cwl.html) in the *Amazon CloudWatch User Guide*.

You can add these CloudWatch Logs permissions using the `AWSLambdaBasicExecutionRole` AWS managed policy provided by Lambda. To add this policy to your role, run the following command:

```
aws iam attach-role-policy --role-name {{your-role}} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

For more information, see [Working with AWS managed policies in the execution role](permissions-managed-policies.md).

## Pricing
<a name="monitoring-cloudwatchlogs-pricing"></a>

There is no additional charge for using Lambda logs; however, standard CloudWatch Logs charges apply. For more information, see [CloudWatch pricing.](https://aws.amazon.com/cloudwatch/pricing/)