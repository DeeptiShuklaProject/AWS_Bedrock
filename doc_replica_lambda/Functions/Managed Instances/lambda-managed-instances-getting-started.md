

# Getting started with Lambda Managed Instances
<a name="lambda-managed-instances-getting-started"></a>

## Creating a Lambda Managed Instance function (console)
<a name="lambda-managed-instances-getting-started-console"></a>

You can use the Lambda console to create a Managed Instance function that runs on Amazon EC2 instances managed by a capacity provider.

**Important:** Before creating a Managed Instance function, you must first create a capacity provider. These functions require a capacity provider to define the Amazon EC2 infrastructure that will run your functions.

**To create a Lambda Managed Instance function (console)**

1. Open the Lambda console.

1. Choose **Capacity providers** from the left navigation pane.

1. Choose **Create capacity provider**.

1. In the **Capacity provider settings** section, enter a name for your capacity provider.

1. Select VPC and permissions for your capacity provider. You can either use an existing or create a new one. For information about creating the required operator role, see [Lambda Operator role for Lambda Managed Instances](lambda-managed-instances-operator-role.md).

1. Expand **Advanced settings**.

1. Define your **Instance requirements** by choosing the processor architecture and instance types.

1. Under **Auto scaling**, specify the maximum number of EC2 vCPUs for your capacity provider. You can also choose **Manual instance scaling mode** to set your own scaling value for precise control.

1. Choose **Create capacity provider** to create a new one.

1. Next, choose **Create function**.

1. Select **Author from scratch**.

1. In the **Basic information** pane, provide a **Function name**.

1. For **Runtime**, choose any of the supported Runtimes.

1. Choose the **Architecture** for your function (same as the one you selected for capacity provider). By default, **x86\_64**.

1. Under **Permissions**, ensure you have permission for the chosen **Execution role**. Otherwise, you can create a new role.

1. Under **Additional configurations**, pick the **Compute type** as **Lambda Managed Instances**.

1. Capacity provider ARN of the capacity provider you created in the previous steps should be pre-selected.

1. Choose **Memory size** and **Execution environment memory (GiB) per vCPU ratio**.

1. Choose **Create function**.

Your Lambda Managed Instance function is created and will provision capacity on your specified capacity provider. Function creation typically takes several minutes. Once complete, you can edit your function code and run your first test.

## Creating a Lambda Managed Instance function (AWS CLI)
<a name="lambda-managed-instances-getting-started-cli"></a>

### Prerequisites
<a name="lambda-managed-instances-prerequisites"></a>

Before you begin, make sure you have the following:
+ **AWS CLI** – Install and configure the AWS CLI. For more information, see [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
+ **IAM permissions** – Your IAM user or role must have permissions to create Lambda functions, capacity providers, and pass IAM roles. Note that you'll also need `iam:CreateServiceLinkedRole` if it's the first time creating a capacity provider in the account or if the Service Linked Role (SLR) was deleted.

### Step 1: Create the required IAM roles
<a name="lambda-managed-instances-step1-iam"></a>

Lambda Managed Instances require two IAM roles: an execution role for your function and an operator role for the capacity provider. The operator role allows Lambda to launch, terminate, and monitor Amazon EC2 instances on your behalf. The function execution role grants the function permissions to access other AWS services and resources.

**To create the Lambda execution role**

1. Create a trust policy document that allows Lambda to assume the role:

   ```
   cat > lambda-trust-policy.json << 'EOF'
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
   EOF
   ```

1. Create the execution role:

   ```
   aws iam create-role \
     --role-name MyLambdaExecutionRole \
     --assume-role-policy-document file://lambda-trust-policy.json
   ```

1. Attach the basic execution policy:

   ```
   aws iam attach-role-policy \
     --role-name MyLambdaExecutionRole \
     --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```

**To create the capacity provider operator role**

1. Create a trust policy document that allows Lambda to assume the operator role:

   ```
   cat > operator-trust-policy.json << 'EOF'
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
   EOF
   ```

1. Create the operator role:

   ```
   aws iam create-role \
     --role-name MyCapacityProviderOperatorRole \
     --assume-role-policy-document file://operator-trust-policy.json
   ```

1. Attach the required EC2 permissions policy:

   ```
   aws iam attach-role-policy \
     --role-name MyCapacityProviderOperatorRole \
     --policy-arn arn:aws:iam::aws:policy/AWSLambdaManagedEC2ResourceOperator
   ```

### Step 2: Set up VPC resources
<a name="lambda-managed-instances-step2-vpc"></a>

Lambda Managed Instances run in your VPC and require a subnet and security group.

**To create VPC resources**

1. Create a VPC:

   ```
   VPC_ID=$(aws ec2 create-vpc \
     --cidr-block 10.0.0.0/16 \
     --query 'Vpc.VpcId' \
     --output text)
   ```

1. Create a subnet:

   ```
   SUBNET_ID=$(aws ec2 create-subnet \
     --vpc-id $VPC_ID \
     --cidr-block 10.0.1.0/24 \
     --query 'Subnet.SubnetId' \
     --output text)
   ```

1. Create a security group:

   ```
   SECURITY_GROUP_ID=$(aws ec2 create-security-group \
     --group-name my-capacity-provider-sg \
     --description "Security group for Lambda Managed Instances" \
     --vpc-id $VPC_ID \
     --query 'GroupId' \
     --output text)
   ```

**Note:** Your Lambda Managed Instances functions require VPC configuration to access resources outside the VPC and to transmit telemetry data to CloudWatch Logs and X-Ray. For configuration details, see [Networking for Lambda Managed Instances](lambda-managed-instances-networking.md).

### Step 3: Create a capacity provider
<a name="lambda-managed-instances-step3-capacity-provider"></a>

A capacity provider manages the EC2 instances that run your Lambda functions.

**To create a capacity provider**

```
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws lambda create-capacity-provider \
  --capacity-provider-name my-capacity-provider \
  --vpc-config SubnetIds=[$SUBNET_ID],SecurityGroupIds=[$SECURITY_GROUP_ID] \
  --permissions-config CapacityProviderOperatorRoleArn=arn:aws:iam::${ACCOUNT_ID}:role/MyCapacityProviderOperatorRole \
  --instance-requirements Architectures=[x86_64] \
  --capacity-provider-scaling-config MaxVCpuCount=30
```

This command creates a capacity provider with the following configuration:
+ **VPC configuration** – Specifies the subnet and security group for the EC2 instances
+ **Permissions** – Defines the IAM role that Lambda uses to manage EC2 instances
+ **Instance requirements** – Specifies the x86\_64 architecture
+ **Scaling configuration** – Sets a maximum of 30 vCPUs for the capacity provider

### Step 4: Create a Lambda function with inline code
<a name="lambda-managed-instances-step4-function"></a>

**To create a function with inline code**

1. First, create a simple Python function and package it inline:

   ```
   # Create a temporary directory for the function code
   mkdir -p /tmp/my-lambda-function
   cd /tmp/my-lambda-function
   
   # Create a simple Python handler
   cat > lambda_function.py << 'EOF'
   import json
   
   def lambda_handler(event, context):
       return {
           'statusCode': 200,
           'body': json.dumps({
               'message': 'Hello from Lambda Managed Instances!',
               'event': event
           })
       }
   EOF
   
   # Create a ZIP file
   zip function.zip lambda_function.py
   ```

1. Create the Lambda function using the inline ZIP file:

   ```
   ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   REGION=$(aws configure get region)
   
   aws lambda create-function \
     --function-name my-managed-instance-function \
     --package-type Zip \
     --runtime python3.13 \
     --handler lambda_function.lambda_handler \
     --zip-file fileb:///tmp/my-lambda-function/function.zip \
     --role arn:aws:iam::${ACCOUNT_ID}:role/MyLambdaExecutionRole \
     --architectures x86_64 \
     --memory-size 2048 \
     --ephemeral-storage Size=512 \
     --capacity-provider-config LambdaManagedInstancesCapacityProviderConfig={CapacityProviderArn=arn:aws:lambda:${REGION}:${ACCOUNT_ID}:capacity-provider:my-capacity-provider}
   ```

   The function is created with:
   + **Runtime** – Python 3.13
   + **Handler** – The `lambda_handler` function in `lambda_function.py`
   + **Memory** – 2048 MB
   + **Ephemeral storage** – 512 MB
   + **Capacity provider** – Links to the capacity provider you created

### Step 5: Publish a function version
<a name="lambda-managed-instances-step5-publish"></a>

To run your function on Lambda Managed Instances, you must publish a version.

**To publish a function version**

```
aws lambda publish-version \
  --function-name my-managed-instance-function
```

This command publishes version 1 of your function and deploys it to the capacity provider.

### Step 6: Invoke your function
<a name="lambda-managed-instances-step6-invoke"></a>

After publishing, you can invoke your function.

**To invoke your function**

```
aws lambda invoke \
  --function-name my-managed-instance-function:1 \
  --payload '{"name": "World"}' \
  response.json

# View the response
cat response.json
```

The function runs on the EC2 instances managed by your capacity provider and returns a response.

### Clean up
<a name="lambda-managed-instances-cleanup"></a>

To avoid incurring charges, delete the resources you created:

1. Delete the function:

   ```
   aws lambda delete-function --function-name my-managed-instance-function
   ```

1. Delete the capacity provider:

   ```
   aws lambda delete-capacity-provider --capacity-provider-name my-capacity-provider
   ```

1. Delete the VPC resources:

   ```
   aws ec2 delete-security-group --group-id $SECURITY_GROUP_ID
   aws ec2 delete-subnet --subnet-id $SUBNET_ID
   aws ec2 delete-vpc --vpc-id $VPC_ID
   ```

1. Delete the IAM roles:

   ```
   aws iam detach-role-policy \
     --role-name MyLambdaExecutionRole \
     --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   aws iam detach-role-policy \
     --role-name MyCapacityProviderOperatorRole \
     --policy-arn arn:aws:iam::aws:policy/AWSLambdaManagedEC2ResourceOperator
   
   aws iam delete-role --role-name MyLambdaExecutionRole
   aws iam delete-role --role-name MyCapacityProviderOperatorRole
   ```