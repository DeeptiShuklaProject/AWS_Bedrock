# Section 25 – Hands-on Labs

<a name="sec-25"></a>

### Lab 1: Hello World Lambda via AWS CLI
* **Objective**: Package, deploy, and invoke a basic Python function using the command line.
* **Steps**:
  1. Save code as `lambda_function.py`:
     ```python
     def lambda_handler(event, context):
         return {"message": "Hello from CLI!"}
     ```
  2. Compress the file: `zip function.zip lambda_function.py`
  3. Deploy the function:
     ```bash
     aws lambda create-function --function-name CLIHelloWorld \
       --runtime python3.12 --role arn:aws:iam::123456789012:role/MyExecutionRole \
       --handler lambda_function.lambda_handler --zip-file fileb://function.zip
     ```
  4. Invoke the function: `aws lambda invoke --function-name CLIHelloWorld response.json`
* **Expected Output**: File `response.json` contains `{"message": "Hello from CLI!"}`.

### Lab 2: Event Payload Inspector
* **Objective**: Create a function that prints details of the incoming trigger payload to CloudWatch.
* **Code**:
  ```python
  import logging
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  
  def lambda_handler(event, context):
      logger.info(f"Incoming Event payload: {event}")
      return {"status": "Logged"}
  ```

### Lab 3: Image Resizer (Pillow Layer)
* **Objective**: Create a function that triggers on S3 uploads, resizes the images, and saves them to a destination bucket.
* **Steps**: Create source and destination buckets, attach the Pillow library layer, and deploy the code from Section 23, Project 1.

### Lab 4: API Gateway Proxy
* **Objective**: Create an HTTP GET endpoint that returns query parameters in the response.
* **Code**: Deploy the code from Section 12, integrate it with an API Gateway REST API, and test the endpoint using `curl`.

### Lab 5: DynamoDB Writer
* **Objective**: Save incoming data fields to a DynamoDB database table.
* **Code**: Deploy the CREATE block code from Section 13. Test by invoking with `{"action": "CREATE", "userId": "1", "name": "Nishu"}`.

### Lab 6: Scheduled EBS Volume Checker
* **Objective**: Trigger a Lambda function every 5 minutes to verify EBS volume status.
* **Steps**: Create an EventBridge rule with a cron schedule, set the target as your Lambda function, and verify executions in CloudWatch Logs.

### Lab 7: SQS Queue Consumer
* **Objective**: Process messages from an SQS queue.
* **Code**: Deploy the batch consumer code from Section 15 and verify that processed messages are deleted from the queue.

### Lab 8: SNS Email Publisher
* **Objective**: Publish alerts to an SNS topic that sends email notifications.
* **Code**: Deploy the alert code from Section 14 and verify email delivery.

### Lab 9: Environment Variable Decryptor
* **Objective**: Decrypt and read sensitive environment variables.
* **Code**: Set an environment variable `SECRET_KEY`, retrieve it in Python using `os.environ.get('SECRET_KEY')`, and print it to logs.

### Lab 10: S3 Metadata Analyzer
* **Objective**: Read and print metadata of files uploaded to S3.
* **Code**: Deploy the metadata parser code from Section 11.

### Lab 11: Error Handler & Status Router
* **Objective**: Return appropriate HTTP status codes based on request validation.
* **Code**: Deploy the validation code from Section 10, Example 7.

### Lab 12: Lambda Layer Integrator
* **Objective**: Attach a custom Lambda Layer to your function.
* **Steps**: Create a layer zip containing the `requests` library, publish it to AWS, attach it to your function, and import `requests` in your code.

### Lab 13: Concurrency Limiter Test
* **Objective**: Configure reserved concurrency to throttle excess traffic.
* **Steps**: Set **Reserved Concurrency** to `1` on a test function, invoke it multiple times in parallel, and observe throttled requests in metrics.

### Lab 14: RDS Proxy Pooler
* **Objective**: Connect a Lambda function to an RDS database securely using RDS Proxy.
* **Steps**: Create an RDS Proxy, configure the IAM role, and initialize database connections inside the Lambda code.

### Lab 15: Log Alarm Slack Dispatcher
* **Objective**: Send errors matching "CRITICAL" in CloudWatch logs to a Slack channel.
* **Code**: Configure a CloudWatch log subscription filter to trigger the Slack dispatcher Lambda from Section 23, Project 5.

---
