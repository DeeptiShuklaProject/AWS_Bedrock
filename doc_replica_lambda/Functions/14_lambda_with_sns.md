# Section 14 – Lambda with SNS

<a name="sec-14"></a>

This integration publishes alert messages to an Amazon SNS Topic, sending emails to notify sysadmins of high-severity system issues.

### Complete Code (Python 3.12)
```python
import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    logger.info("Parsing event error details...")
    
    # Extract error payload
    source = event.get('source', 'ApplicationEngine')
    error_msg = event.get('error', 'Execution pipeline failure.')
    severity = event.get('severity', 'CRITICAL')
    
    subject = f"[{severity} ALERT] System Failure in {source}"
    message_body = (
        f"Alert: Critical system exception triggered.\n\n"
        f"- Source Component: {source}\n"
        f"- Error Message: {error_msg}\n"
        f"- Request ID: {context.aws_request_id}\n\n"
        f"Check CloudWatch Log Streams immediately."
    )
    
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message_body,
            Subject=subject
        )
        logger.info(f"Published alert to SNS. Message ID: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': json.dumps('Alert sent successfully')
        }
    except Exception as e:
        logger.error(f"SNS Publish failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Alert routing failure')
        }
```

---
