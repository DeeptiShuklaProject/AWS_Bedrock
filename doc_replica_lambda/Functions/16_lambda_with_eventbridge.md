# Section 16 – Lambda with EventBridge

<a name="sec-16"></a>

This script triggers daily at 11:00 PM via EventBridge Scheduler to check EBS volumes and take snapshots of instances tagged for automated backups.

### Complete Code (Python 3.12)
```python
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    logger.info("Initiating automated EC2 EBS snapshot sequence")
    
    try:
        # Find instances with the 'Backup=True' tag
        reservations = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Backup', 'Values': ['True']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )['Reservations']
        
        created_snapshots = []
        
        for res in reservations:
            for instance in res['Instances']:
                instance_id = instance['InstanceId']
                
                # Iterate over attached volumes
                for device in instance.get('BlockDeviceMappings', []):
                    volume_id = device['Ebs']['VolumeId']
                    logger.info(f"Found Volume {volume_id} on Instance {instance_id}")
                    
                    # Create EBS Snapshot
                    snapshot = ec2_client.create_snapshot(
                        VolumeId=volume_id,
                        Description=f"AutoBackup snapshot for instance {instance_id}"
                    )
                    
                    snapshot_id = snapshot['SnapshotId']
                    logger.info(f"Snapshot created: {snapshot_id}")
                    created_snapshots.append(snapshot_id)
                    
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'BACKUP_COMPLETE',
                'snapshots': created_snapshots
            })
        }
        
    except Exception as e:
        logger.error(f"Backup operation failed: {str(e)}")
        raise e
```

---
