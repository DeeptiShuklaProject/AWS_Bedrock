

# Create your first Lambda MicroVM
<a name="microvms-getting-started"></a>

This tutorial walks you through creating a AWS Lambda MicroVM image and running a MicroVM from it. By the end, you'll have a running application accessible over HTTPS.

## Prerequisites
<a name="microvms-getting-started-prereqs"></a>

You need two things before you start:

1. **An Amazon S3 bucket** in your preferred AWS Region to store your application artifact (the zip file you'll create in Step 2).

1. **An IAM build role** that Lambda assumes during image creation. Lambda uses this role to download your code artifact from Amazon S3 and write build logs to CloudWatch.

Create the IAM role with the following trust policy. This allows the Lambda service to assume the role:

```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": ["sts:AssumeRole", "sts:TagSession"]
  }]
}
```

Attach the following permissions policy to the role. Replace `<your-bucket-name>` with your Amazon S3 bucket name:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::<your-bucket-name>/*"
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

**Note**  
If your `Dockerfile` pulls from a private AWS ECR repository, also add `ecr:GetAuthorizationToken` and `ecr:BatchGetImage` to the permissions policy.

## Creating your first MicroVM image
<a name="microvms-getting-started-first-image"></a>

A MicroVM image captures your application in a fully initialized state. When you run a MicroVM from this image, your application starts immediately – no boot or initialization delay.

### Step 1: Write your application and Dockerfile
<a name="microvms-getting-started-step1"></a>

Create a simple HTTP server that will run inside your MicroVM. This example uses Node.js with no external dependencies:

**`app.js`**

```
// Minimal HTTP server — listens on port 8080
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'ok', path: req.url }));
});

server.listen(8080, () => {
  console.log('Listening on port 8080');
});
```

Next, create a `Dockerfile` that packages and starts your application:

**`Dockerfile`**

```
# Use a lightweight Node.js runtime for your application layers
FROM node:24-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy your application code
COPY app.js .

# Declare the port your app listens on
EXPOSE 8080

# Start the application — Lambda snapshots the running state
CMD ["node", "app.js"]
```

**Note**  
The `FROM` instruction sets the container image for your application layers. You can use any compatible container image. The Lambda managed base image (which provides the MicroVM operating system and service components) is specified separately with `--base-image-arn` in Step 3.  
If your application generates unique values (IDs, secrets, or cryptographic material), use your language's standard cryptographically secure pseudorandom number generator (CSPRNG) library to ensure uniqueness across MicroVMs. If your application uses OpenSSL, use the Lambda base container image which includes a snapshot-compatible version. For details, see the snapshot compatibility section in [MicroVM Images](microvms-images.md).

### Step 2: Package and upload to Amazon S3
<a name="microvms-getting-started-step2"></a>

Package your `app.js` and `Dockerfile` into a zip archive, then upload it to your Amazon S3 bucket. Run the following commands in your terminal:

```
zip app.zip app.js Dockerfile
aws s3 cp app.zip s3://{{your-bucket-name}}/app.zip
```

### Step 3: Create the MicroVM image
<a name="microvms-getting-started-step3"></a>

Call `create-microvm-image` to start the build. Lambda downloads your zip from Amazon S3, runs your `Dockerfile`, starts your application, and captures a Firecracker snapshot of the fully initialized state:

```
aws lambda-microvms create-microvm-image \
  --name my-first-microvm-image \
  --code-artifact uri=s3://{{your-bucket-name}}/app.zip \
  --base-image-arn arn:aws:lambda:{{us-east-1}}:aws:microvm-image:al2023-1 \
  --build-role-arn arn:aws:iam::{{123456789012}}:role/MicrovmBuildRole
```

The image starts in `CREATING` state. Check the build status with:

```
aws lambda-microvms get-microvm-image \
  --image-identifier my-first-microvm-image
```

When the build completes, the `state` field changes to `CREATED`:

```
{
  "imageName": "my-first-microvm-image",
  "imageArn": "arn:aws:lambda:us-east-1:123456789012:microvm-image:my-first-microvm-image",
  "state": "CREATED",
  "imageVersion": "1.0",
  ...
}
```

If the state is `CREATE_FAILED`, check the build logs in CloudWatch under `/aws/lambda/microvms/my-first-microvm-image`.

## Running your first MicroVM
<a name="microvms-getting-started-run"></a>

Once your MicroVM image reaches `CREATED` state, you can run MicroVMs from it. Each image can launch many MicroVMs – one per tenant, user session, or job.

Run a MicroVM with the following command:

```
aws lambda-microvms run-microvm \
  --image-identifier my-first-microvm-image \
  --ingress-network-connectors "arn:aws:lambda:{{us-east-1}}:aws:network-connector:aws-network-connector:ALL_INGRESS" \
  --egress-network-connectors "arn:aws:lambda:{{us-east-1}}:aws:network-connector:aws-network-connector:INTERNET_EGRESS" \
  --idle-policy '{"autoResumeEnabled":true,"maxIdleDurationSeconds":900,"suspendedDurationSeconds":300}'
```

Parameters explained:
+ `--ingress-network-connectors` – Enables inbound HTTPS traffic to your MicroVM on all ports. This is a Lambda-managed connector.
+ `--egress-network-connectors` – Enables outbound internet access from your MicroVM. This is a Lambda-managed connector.
+ `--idle-policy` – Configures automatic suspend-resume behavior. This policy suspends the MicroVM after 15 minutes of inactivity, keeps it suspended for up to 5 minutes, and resumes automatically when traffic arrives.

The response includes the MicroVM ID and endpoint URL:

```
{
  "microvmId": "mvm-01234567-abcd-ef01-2345-6789abcdef01",
  "state": "PENDING",
  "endpoint": "mvm-01234567-abcd-ef01-2345-6789abcdef01.lambda-microvm.us-east-1.on.aws",
  ...
}
```

Wait for the state to reach `RUNNING`:

```
aws lambda-microvms get-microvm \
  --microvm-identifier mvm-01234567-abcd-ef01-2345-6789abcdef01
```

## Connecting to your MicroVM
<a name="microvms-getting-started-connect"></a>

All requests to a MicroVM endpoint require an authentication token. Generate one with:

```
aws lambda-microvms create-microvm-auth-token \
  --microvm-identifier mvm-01234567-abcd-ef01-2345-6789abcdef01 \
  --expiration-in-minutes 30 \
  --allowed-ports '[{"allPorts":{}}]'
```

The response includes a token in the `authToken` field. Use it to send a request to your running application:

```
curl https://mvm-01234567-abcd-ef01-2345-6789abcdef01.lambda-microvm.us-east-1.on.aws/ \
  -H "X-aws-proxy-auth: {{<token-value>}}"
```

You should see the response from your application:

```
{"status":"ok","path":"/"}
```

Your MicroVM is running and serving traffic. The application you wrote in Step 1 is live at the endpoint URL.

## Clean up
<a name="microvms-getting-started-cleanup"></a>

To avoid ongoing charges, terminate the MicroVM when you're done:

```
aws lambda-microvms terminate-microvm \
  --microvm-identifier mvm-01234567-abcd-ef01-2345-6789abcdef01
```

## Next steps
<a name="microvms-getting-started-next"></a>
+ Learn about [Core concepts](microvms-how-it-works.md) to understand the snapshot process, lifecycle states, and base images.
+ Explore [MicroVM Images](microvms-images.md) to learn about image build hooks, versioning, and snapshot compatibility.
+ See [Running MicroVMs](microvms-launching.md) for SDK examples, lifecycle hooks, and scaling strategies.