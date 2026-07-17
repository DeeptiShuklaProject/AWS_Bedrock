# Section 8 – Python Basics for Lambda

<a name="sec-8"></a>

Here is the essential Python syntax required to write AWS Lambda functions:

### Imports & Variables
```python
import json
import os
import math

item_count = 15                  # Integer
unit_price = 5.99                # Float
product_name = "Premium Apple"   # String
is_in_stock = True               # Boolean
```

### Lists, Dictionaries & JSON Parsing
```python
# Lists (Arrays)
categories = ["Fruits", "Vegetables", "Organic"]

# Dictionary (Key-Value)
payload = {
    "item_id": "item-901",
    "quantity": 3
}

# Convert JSON string to Python Dictionary
json_data = '{"user": "nishu", "age": 28}'
parsed_data = json.loads(json_data)
user = parsed_data["user"]

# Convert Dictionary to JSON string
raw_payload = json.dumps(payload)
```

### Conditionals and Iteration
```python
if unit_price > 10.0:
    tax_rate = 0.15
else:
    tax_rate = 0.08

for category in categories:
    print(f"Processing category: {category}")
```

### Exception Handling & Logger
```python
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    value = payload["missing_key"]
except KeyError as e:
    logger.error(f"Missing required parameter: {str(e)}")
```

---
