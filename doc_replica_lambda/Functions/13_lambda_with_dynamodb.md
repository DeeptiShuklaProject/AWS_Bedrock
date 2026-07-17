# Section 13 – Lambda with DynamoDB

<a name="sec-13"></a>

This section covers complete CRUD (Create, Read, Update, Delete) operations on Amazon DynamoDB database tables using `boto3`.

### Complete Code (Python 3.12)
```python
import json
import os
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get('USERS_TABLE', 'UsersTable')
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(TABLE_NAME)

def lambda_handler(event, context):
    # Parse transaction request
    action = event.get('action')
    user_id = event.get('userId')
    
    if not action or not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing parameters: action and userId'})
        }
        
    try:
        if action == 'CREATE':
            name = event.get('name', 'N/A')
            email = event.get('email', 'N/A')
            table.put_item(
                Item={
                    'userId': user_id,
                    'name': name,
                    'email': email,
                    'status': 'ACTIVE'
                }
            )
            return {'statusCode': 201, 'body': json.dumps('User added successfully')}
            
        elif action == 'READ':
            response = table.get_item(Key={'userId': user_id})
            user_data = response.get('Item')
            if not user_data:
                return {'statusCode': 404, 'body': json.dumps({'error': 'User record not found'})}
            return {'statusCode': 200, 'body': json.dumps(user_data)}
            
        elif action == 'UPDATE':
            new_email = event.get('email')
            if not new_email:
                return {'statusCode': 400, 'body': json.dumps('Missing email parameter')}
            
            table.update_item(
                Key={'userId': user_id},
                UpdateExpression="set email = :val",
                ExpressionAttributeValues={':val': new_email},
                ReturnValues="UPDATED_NEW"
            )
            return {'statusCode': 200, 'body': json.dumps('User record updated')}
            
        elif action == 'DELETE':
            table.delete_item(Key={'userId': user_id})
            return {'statusCode': 200, 'body': json.dumps('User record deleted')}
            
        else:
            return {'statusCode': 400, 'body': json.dumps(f'Unsupported action operation: {action}')}
            
    except ClientError as e:
        logger.error(f"DynamoDB transaction failed: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Database transaction error occurred'})
        }
```

---
