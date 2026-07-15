

# Invoking Lambda functions with Amazon SNS notifications
<a name="with-sns"></a>

You can use a Lambda function to process Amazon Simple Notification Service (Amazon SNS) notifications. Amazon SNS supports Lambda functions as a target for messages sent to a topic. You can subscribe your function to topics in the same account or in other AWS accounts. For a detailed walkthrough, see [Tutorial: Using AWS Lambda with Amazon Simple Notification Service](with-sns-example.md).

Lambda supports SNS triggers for standard SNS topics only. FIFO topics aren't supported.

Lambda processes SNS messages asynchronously by queuing the messages and handling retries. If Amazon SNS can't reach Lambda or the message is rejected, Amazon SNS retries at increasing intervals over several hours. For details, see [Reliability](https://aws.amazon.com/sns/faqs/#Reliability) in the Amazon SNS FAQs.

**Warning**  
Lambda asynchronous invocations process each event at least once, and duplicate processing of records can occur. To avoid potential issues related to duplicate events, we strongly recommend that you make your function code idempotent. To learn more, see [ How do I make my Lambda function idempotent](https://repost.aws/knowledge-center/lambda-function-idempotent) in the AWS Knowledge Center.

## Idempotency utility from Powertools for AWS Lambda
<a name="services-sns-powertools-idempotency"></a>

The idempotency utility from Powertools for AWS Lambda makes your Lambda functions idempotent. It is available for Python, TypeScript, Java, and .NET. For more information, see [Idempotency utility](https://docs.powertools.aws.dev/lambda/python/latest/utilities/idempotency/) in the *Powertools for AWS Lambda (Python) documentation*, [Idempotency Utility](https://docs.aws.amazon.com/powertools/typescript/2.1.1/utilities/idempotency/) in the *Powertools for AWS Lambda (TypeScript) documentation*, [Idempotency Utility](https://docs.powertools.aws.dev/lambda/java/latest/utilities/idempotency/) in the *Powertools for AWS Lambda (Java) documentation*, and [Idempotency Utility](https://docs.powertools.aws.dev/lambda/dotnet/utilities/idempotency/) in the *Powertools for AWS Lambda (.NET) documentation*.

**Topics**
+ [Idempotency utility from Powertools for AWS Lambda](#services-sns-powertools-idempotency)
+ [Adding an Amazon SNS topic trigger for a Lambda function using the console](#sns-trigger-console)
+ [Manually adding an Amazon SNS topic trigger for a Lambda function](#sns-trigger-manual)
+ [Sample SNS event shape](#sns-sample-event)
+ [Tutorial: Using AWS Lambda with Amazon Simple Notification Service](with-sns-example.md)

## Adding an Amazon SNS topic trigger for a Lambda function using the console
<a name="sns-trigger-console"></a>

To add an SNS topic as a trigger for a Lambda function, the easiest way is to use the Lambda console. When you add the trigger via the console, Lambda automatically sets up the necessary permissions and subscriptions to start receiving events from the SNS topic.

**To add an SNS topic as a trigger for a Lambda function (console)**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose the name of a function you want to add the trigger for.

1. Choose **Configuration**, and then choose **Triggers**.

1. Choose **Add trigger**.

1. Under **Trigger configuration**, in the dropdown menu, choose **SNS**.

1. For **SNS topic**, choose the SNS topic to subscribe to.

## Manually adding an Amazon SNS topic trigger for a Lambda function
<a name="sns-trigger-manual"></a>

To set up an SNS trigger for a Lambda function manually, you need to complete the following steps:
+ Define a resource-based policy for your function to allow SNS to invoke it.
+ Subscribe your Lambda function to the Amazon SNS topic.
**Note**  
If your SNS topic and your Lambda function are in different AWS accounts, you also need to grant extra permissions to allow cross-account subscriptions to the SNS topic. For more information, see [Grant cross-account permission for Amazon SNS subscription](with-sns-example.md#with-sns-subscription-grant-permission).

You can use the AWS Command Line Interface (AWS CLI) to complete both of these steps. First, to define a resource-based policy for a Lambda function that allows SNS invocations, use the following AWS CLI command. Be sure to replace the value of `--function-name` with your Lambda function name, and the value of `--source-arn` with your SNS topic ARN.

```
aws lambda add-permission --function-name {{example-function}} \
    --source-arn {{arn:aws:sns:us-east-1:123456789012:sns-topic-for-lambda}} \
    --statement-id function-with-sns --action "lambda:InvokeFunction" \
    --principal sns.amazonaws.com
```

To subscribe your function to the SNS topic, use the following AWS CLI command. Replace the value of `--topic-arn` with your SNS topic ARN, and the value of `--notification-endpoint` with your Lambda function ARN.

```
aws sns subscribe --protocol lambda \
    --region us-east-1 \
    --topic-arn {{arn:aws:sns:us-east-1:123456789012:sns-topic-for-lambda}} \
    --notification-endpoint {{arn:aws:lambda:us-east-1:123456789012:function:example-function}}
```

## Sample SNS event shape
<a name="sns-sample-event"></a>

Amazon SNS invokes your function [asynchronously](invocation-async.md) with an event that contains a message and metadata.

**Example Amazon SNS message event**  

```
{
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "2019-01-02T12:45:07.000Z",
        "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==",
        "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": "Hello from SNS!",
        "MessageAttributes": {
          "Test": {
            "Type": "String",
            "Value": "TestString"
          },
          "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
          }
        },
        "Type": "Notification",
        "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-1:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
        "TopicArn":"arn:aws:sns:us-east-1:123456789012:sns-lambda",
        "Subject": "TestInvoke"
      }
    }
  ]
}
```