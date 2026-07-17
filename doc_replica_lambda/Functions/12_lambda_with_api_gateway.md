# Section 12 – Lambda with API Gateway

<a name="sec-12"></a>

With API Gateway **Proxy Integration**, Lambda parses the full request parameters and responds with a JSON payload that API Gateway maps to an HTTP response.

```
Client Request ──► [API Gateway] ──► Trigger Payload ──► [AWS Lambda] ──► Returns ──► Response JSON
```

### Complete Code (Python 3.12)
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Parsing incoming API HTTP request event")
    
    # Extract headers and request context
    method = event.get('httpMethod', 'GET')
    path_parameters = event.get('pathParameters') or {}
    query_parameters = event.get('queryStringParameters') or {}
    
    # Get user identifier
    user_id = path_parameters.get('userId', 'anonymous')
    search_query = query_parameters.get('q', 'all')
    
    # Read POST payload if present
    post_payload = {}
    if method == 'POST' and event.get('body'):
        try:
            post_payload = json.loads(event['body'])
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Malformed JSON payload'})
            }
            
    response_body = {
        "status": "SUCCESS",
        "userId": user_id,
        "searchQuery": search_query,
        "requestMethod": method,
        "parsedPayload": post_payload
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' # Enable CORS for browser clients
        },
        'body': json.dumps(response_body)
    }
```

---
