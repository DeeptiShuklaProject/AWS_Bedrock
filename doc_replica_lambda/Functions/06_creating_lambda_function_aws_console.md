# Section 6 – Creating Lambda Function (AWS Console)

<a name="sec-6"></a>

### Step 1: Open the AWS Console
Search for **Lambda** in the search box and click **Create function**.

### Step 2: Configure Baselines
* Select **Author from scratch**.
* **Function name**: `DemoCalculator`
* **Runtime**: **Python 3.12**
* **Architecture**: `x86_64` (default) or `arm64` (Graviton2).

### Step 3: Configure Role & Permissions
* Expand **Change default execution role**.
* Select **Create a new role with basic Lambda permissions**. This creates an IAM execution role allowing your function to write runtime logs to CloudWatch.
* Click **Create function**.

### Step 4: Add Environment Variables
* Go to the **Configuration** tab, select **Environment variables**, and click **Edit**.
* Click **Add environment variable**.
* Set Key: `APP_ENV`, Value: `staging`.
* Click **Save**.

### Step 5: Adjust Memory and Timeout
* In the **Configuration** tab, select **General configuration** and click **Edit**.
* Change **Timeout** from 3 seconds to `15 seconds`.
* Click **Save**.

### Step 6: Code Deployment
* Under the **Code** tab, double-click `lambda_function.py` and replace it with:
  ```python
  import json
  import os

  def lambda_handler(event, context):
      env = os.environ.get('APP_ENV', 'production')
      return {
          'statusCode': 200,
          'body': json.dumps({
              'status': 'Connected',
              'environment': env
          })
      }
  ```
* Click **Deploy** to publish the changes.

### Step 7: Testing
* Click **Test** and configure a test event named `MyTestEvent`.
* Use the default JSON template and click **Save**.
* Click **Test** again. The execution result window will display code outputs, execution duration, and log records.

---
