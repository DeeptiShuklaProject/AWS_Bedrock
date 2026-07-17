# Section 11 – Lambda with S3

<a name="sec-11"></a>

This integration processes file uploads to an S3 bucket in real time, extracts file metadata, and saves a status summary JSON to a destination bucket.

```
Upload File ──► [Source S3 Bucket] ──► Event Trigger ──► [Lambda Function] ──► Write Output ──► [Target Audit S3 Bucket]
```

### Complete Code (Python 3.12)
```python
import json
import urllib.parse
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Parse bucket and file keys from S3 trigger event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Get Object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        size_bytes = response['ContentLength']
        content_type = response['ContentType']
        
        logger.info(f"File processed: Bucket: {bucket} | Key: {key} | Size: {size_bytes} bytes | Type: {content_type}")
        
        # 3. Create Audit report dictionary
        audit_payload = {
            "source_bucket": bucket,
            "filename": key,
            "file_size": size_bytes,
            "content_type": content_type,
            "status": "PROCESSED_SUCCESSFULLY"
        }
        
        # 4. Upload summary to target audit bucket
        target_bucket = f"{bucket}-audit-logs"
        target_key = f"audit-{key}.json"
        
        s3_client.put_object(
            Bucket=target_bucket,
            Key=target_key,
            Body=json.dumps(audit_payload, indent=2),
            ContentType='application/json'
        )
        logger.info(f"Audit log saved: {target_bucket}/{target_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('S3 Event processed successfully')
        }
        
    except Exception as e:
        logger.error(f"Error handling S3 object: {str(e)}")
        raise e
```

---
