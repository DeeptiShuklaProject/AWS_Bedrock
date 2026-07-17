# Section 9 – Lambda Function Structure

<a name="sec-9"></a>

Every Python Lambda function requires a core entrypoint handler function, configured in the Lambda runtime settings.

```python
import json
import logging

# Instantiate heavy clients globally for warm start reusability
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Core Lambda Entrypoint.
    
    :param event: The JSON event trigger payload (dict)
    :param context: Runtime context helper object (instance of LambdaContext)
    :return: Return values or status responses
    """
    logger.info("Executing function handler execution...")
    
    # Extract Request Metadata from context
    request_id = context.aws_request_id
    remaining_time = context.get_remaining_time_in_millis()
    
    logger.info(f"Request ID: {request_id} | Remaining Execution Window: {remaining_time}ms")
    
    # Access Event Payload
    user_name = event.get('name', 'Guest')
    
    response = {
        'message': f"Hello, {user_name}!",
        'request_id': request_id
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
```

---
