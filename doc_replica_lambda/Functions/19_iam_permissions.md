# Section 19 – IAM Permissions

<a name="sec-19"></a>

AWS Lambda enforces security policies via IAM roles:

* **Execution Role**: An IAM role attached to your function. It defines which AWS resources the function is authorized to interact with (e.g. S3, DynamoDB, CloudWatch Logs).
* **Least Privilege**: Always restrict permissions to the exact resources required. Avoid using broad wildcards (e.g. `"Action": "s3:*"` on `"Resource": "*"`).

### trust-relationship.json
This trust policy permits the Lambda service to assume the execution role:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---
