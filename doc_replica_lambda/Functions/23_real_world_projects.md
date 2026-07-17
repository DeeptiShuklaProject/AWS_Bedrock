# Section 23 – Real-World Projects

<a name="sec-23"></a>

### Project 1: Image Processing Engine
**Goal**: Automatically resize images uploaded to a source S3 bucket to `150x150` and save them to a destination bucket.

```python
import os
import io
import boto3
from PIL import Image
import urllib.parse
import json

s3 = boto3.client('s3')
TARGET_BUCKET = os.environ.get('TARGET_BUCKET', 'my-resized-thumbnails')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # 1. Download image from source S3
    response = s3.get_object(Bucket=source_bucket, Key=file_key)
    raw_data = response['Body'].read()
    
    # 2. Open and resize image using Pillow
    img = Image.open(io.BytesIO(raw_data))
    img.thumbnail((150, 150))
    
    # 3. Save output image to a memory buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, format=img.format or 'JPEG')
    output_buffer.seek(0)
    
    # 4. Upload resized thumbnail to target S3
    s3.put_object(
        Bucket=TARGET_BUCKET,
        Key=f"thumb-{file_key}",
        Body=output_buffer,
        ContentType=response['ContentType']
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail generated!')
    }
```

### Project 2: CSV to JSON Converter
**Goal**: Convert uploaded raw CSV files into JSON format and save them to a target database directory.

```python
import json
import csv
import io
import boto3
import urllib.parse

s3 = boto3.client('s3')
TARGET_BUCKET = "my-json-database-bucket"

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Download file contents
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_content = response['Body'].read().decode('utf-8')
    
    # Read CSV and convert to list of dicts
    reader = csv.DictReader(io.StringIO(csv_content))
    data_list = [row for row in reader]
    
    # Save output as JSON
    json_filename = key.replace('.csv', '.json')
    s3.put_object(
        Bucket=TARGET_BUCKET,
        Key=json_filename,
        Body=json.dumps(data_list, indent=2),
        ContentType='application/json'
    )
    
    return "CSV converted to JSON successfully."
```

### Project 3: Automatic EBS Backup Engine
**Goal**: Scan EBS volumes daily and create backup snapshots of volumes tagged with `Backup=True`.

```python
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    logger.info("Executing daily automated EBS snapshot pipeline...")
    
    # Find instances tagged with Backup=True
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Backup', 'Values': ['True']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    snapshots = []
    
    for reservation in instances.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instance_id = instance['InstanceId']
            for mapping in instance.get('BlockDeviceMappings', []):
                volume_id = mapping['Ebs']['VolumeId']
                
                # Create snapshot
                snap = ec2.create_snapshot(
                    VolumeId=volume_id,
                    Description=f"Auto backup for instance {instance_id}"
                )
                snapshots.append(snap['SnapshotId'])
                logger.info(f"Snapshot created: {snap['SnapshotId']} for volume {volume_id}")
                
    return {"createdSnapshots": snapshots}
```

### Project 4: DynamoDB Streams Welcome Email Sender
**Goal**: Send a welcome email when a new user registers and is added to the UsersTable in DynamoDB.

```python
import boto3
import json

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:WelcomeEmails"

def lambda_handler(event, context):
    for record in event['Records']:
        # Trigger on INSERT only
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            user_email = new_image['email']['S']
            user_name = new_image['name']['S']
            
            # Send notification message via SNS
            msg = f"Welcome, {user_name}! Your registration was successful."
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=msg,
                Subject="Welcome to Inventure AI!"
            )
            
    return "Welcome emails processed"
```

### Project 5: System Health Monitoring Alert
**Goal**: Send Slack notifications when EC2 system health checks fail.

```python
import urllib3
import json

http = urllib3.PoolManager()
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00/B00/X00"

def lambda_handler(event, context):
    alarm_name = event['alarmData']['alarmName']
    state_value = event['alarmData']['state']['value']
    reason = event['alarmData']['state']['reason']
    
    slack_message = {
        "text": f"🚨 *SYSTEM ALERT*: {alarm_name} transitioned to state *{state_value}*.\nReason: {reason}"
    }
    
    response = http.request(
        'POST',
        SLACK_WEBHOOK_URL,
        body=json.dumps(slack_message),
        headers={'Content-Type': 'application/json'}
    )
    
    return {"slack_response": response.status}
```

### Project 6: Server Log Error Monitor
**Goal**: Analyze CloudWatch subscription log logs for the keyword "ERROR" and send notifications.

```python
import gzip
import json
import base64
import boto3

sns = boto3.client('sns')
SNS_TOPIC = "arn:aws:sns:us-east-1:123456789012:LogAlerts"

def lambda_handler(event, context):
    # Decode and decompress CloudWatch logs
    data = base64.b64decode(event['awslogs']['data'])
    decompressed = gzip.decompress(data)
    log_json = json.loads(decompressed)
    
    for log_event in log_json['logEvents']:
        message = log_event['message']
        if "ERROR" in message:
            sns.publish(
                TopicArn=SNS_TOPIC,
                Message=f"Log Error Detected:\n{message}",
                Subject="Server Error Detected"
            )
            
    return "Logs processed"
```

### Project 7: Daily Transaction Summary Reporter
**Goal**: Summarize database transaction statistics and send reports to administrators.

```python
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TransactionsTable')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Query transactions
    response = table.scan()
    items = response.get('Items', [])
    
    total_sales = sum(float(item['amount']) for item in items)
    report = f"Daily Transaction Summary ({datetime.utcnow().date()}):\n- Total Transactions: {len(items)}\n- Total Sales: ${total_sales:.2f}"
    
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123456789012:DailyReports",
        Message=report,
        Subject="Daily Sales Report Summary"
    )
    
    return "Report delivered"
```

---
