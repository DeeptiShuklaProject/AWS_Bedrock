# Section 7 – Creating Lambda using AWS CLI

<a name="sec-7"></a>

To manage Lambda functions from your terminal, use the **AWS CLI**.

### Command 1: Create a Function
Deploy a packaged zip file to Lambda:
```bash
aws lambda create-function \
    --function-name CLIProductFetcher \
    --runtime python3.12 \
    --role arn:aws:iam::123456789012:role/MyLambdaExecutionRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 10 \
    --memory-size 256
```
* **Parameters**:
  * `--handler`: Points to `filename.method` inside the zip container.
  * `--zip-file`: Path to the local deployment package prefixed with `fileb://`.

### Command 2: Update Function Code
Upload a new zip file version:
```bash
aws lambda update-function-code \
    --function-name CLIProductFetcher \
    --zip-file fileb://function_v2.zip
```

### Command 3: Invoke the Function
Trigger execution and save the result locally:
```bash
aws lambda invoke \
    --function-name CLIProductFetcher \
    --payload '{"productId": "prod-1002"}' \
    --cli-binary-format raw-in-base64-out \
    output.json
```

### Command 4: Delete the Function
Clean up the resource:
```bash
aws lambda delete-function \
    --function-name CLIProductFetcher
```

---
