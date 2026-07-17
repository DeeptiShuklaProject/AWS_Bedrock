# Section 10 – Python Lambda Examples

<a name="sec-10"></a>

### Example 1: Hello World
```python
def lambda_handler(event, context):
    return "Hello World"
```

### Example 2: Addition Calculator
* **Input**: `{"a": 10, "b": 20}`
```python
import json

def lambda_handler(event, context):
    num_a = event.get('a', 0)
    num_b = event.get('b', 0)
    result = num_a + num_b
    return {
        "statusCode": 200,
        "body": json.dumps({"sum": result})
    }
```

### Example 3: Greeting API
* **Input**: `{"name": "John"}`
```python
def lambda_handler(event, context):
    name = event.get('name', 'User')
    return f"Hello {name}"
```

### Example 4: Current Date
```python
from datetime import datetime

def lambda_handler(event, context):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

### Example 5: Random Number Generator
```python
import random

def lambda_handler(event, context):
    low = event.get('min', 1)
    high = event.get('max', 100)
    number = random.randint(low, high)
    return {
        "number": number
    }
```

### Example 6: Environment Variables
```python
import os

def lambda_handler(event, context):
    environment = os.environ.get('ENVIRONMENT_NAME', 'development')
    return {
        "env": environment
    }
```

### Example 7: Error Handling
```python
import json

def lambda_handler(event, context):
    email = event.get('email')
    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing parameter: email"})
        }
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "Authorized"})
    }
```

### Example 8: Logging
```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Executing function initialization tasks")
    logger.warning("Resource warnings detected during runtime execution")
    return "Logs successfully dispatched"
```

---
