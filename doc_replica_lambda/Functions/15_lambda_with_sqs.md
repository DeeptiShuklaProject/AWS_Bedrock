# Section 15 – Lambda with SQS

<a name="sec-15"></a>

This integration polls messages from Amazon SQS, processes the payloads in batches, and utilizes Partial Batch Failure Reporting so that only failed messages remain in the queue.

### Complete Code (Python 3.12)
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received batch of {len(event['Records'])} messages.")
    
    batch_item_failures = []
    
    for record in event['Records']:
        message_id = record['messageId']
        payload = record['body']
        
        try:
            # 1. Parse JSON payload
            data = json.loads(payload)
            order_id = data.get('orderId')
            quantity = data.get('quantity')
            
            logger.info(f"Processing message {message_id} | Order ID: {order_id} | Qty: {quantity}")
            
            if int(quantity) <= 0:
                raise ValueError("Order quantity must be positive")
                
        except Exception as e:
            logger.error(f"Failed to process message {message_id}: {str(e)}")
            # Record failed message ID to preserve in the queue for DLQ processing
            batch_item_failures.append({"itemIdentifier": message_id})
            
    # SQS reads this list to determine which items failed processing
    return {
        "batchItemFailures": batch_item_failures
    }
```

---
