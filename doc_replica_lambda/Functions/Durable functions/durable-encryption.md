

# Encrypting AWS Lambda durable execution data
<a name="durable-encryption"></a>

With [AWS Lambda durable functions](durable-functions.md), you can build resilient, multi-step applications that run for up to one year, using checkpoints to recover each execution from failures by replaying completed work.

Lambda always encrypts durable execution data at rest. You can additionally configure your own AWS KMS customer managed key on the function for rotation control, audit visibility, or compliance. With a customer managed key, only principals you authorize can read execution data.

## How encryption works
<a name="durable-encryption-how-it-works"></a>

A Lambda durable execution uses the same KMS key it started with for its entire lifetime. Changing or removing the key on the function affects only executions that start after the change. See [When the customer managed key is unavailable](#durable-encryption-key-unavailable) for how a durable execution behaves when its key is unavailable.

Customer managed keys incur standard AWS KMS charges. For pricing details, see [AWS Key Management Service pricing](https://aws.amazon.com/kms/pricing/).

## What is encrypted
<a name="durable-encryption-what-is-encrypted"></a>

When you configure a customer managed key on a durable function, Lambda uses that key to encrypt the following durable execution data at rest:
+ The input payload that you pass with each `Invoke` request.
+ Checkpoint data persisted by the `CheckpointDurableExecution` API, including step results, step errors, and chained invoke inputs.
+ Execution results and errors.
+ Callback results and errors that you submit through `SendDurableExecutionCallbackSuccess` and `SendDurableExecutionCallbackFailure`.

**Function-level and durable execution keys are independent**  
The function-level `KMSKeyArn` that encrypts [environment variables](configuration-envvars-encryption.md), [.zip deployment packages](encrypt-zip-package.md), and [SnapStart](snapstart-security.md) snapshots is separate from the `KMSKeyArn` in `DurableConfig` that encrypts durable execution data. Setting one does not set the other. You can use the same KMS key for both, or you can use different KMS keys.

## Set up customer managed key encryption
<a name="durable-encryption-setup"></a>

Setting up customer managed key encryption for a durable function is a three-step process. Complete the following steps in order.

### Create a customer managed key
<a name="durable-encryption-create-key"></a>

Durable functions support symmetric encryption KMS keys in the same AWS Region as the function. Cross-Region keys are not supported. To create a symmetric customer managed key, follow the steps for [creating symmetric encryption KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk) in the *AWS Key Management Service Developer Guide*.

### Permissions
<a name="durable-encryption-permissions"></a>

You grant AWS KMS permissions through the KMS key's key policy.

Configuring a customer managed key requires AWS KMS permissions on the principal that creates or updates the function. Invoking a durable function does not require AWS KMS permissions on the caller; Lambda performs the encryption with its service principal.

#### Key policy
<a name="durable-encryption-key-policy"></a>

[Key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) control access to your customer managed key. Every customer managed key must have exactly one key policy. In a key policy, `Resource: "*"` refers only to the KMS key that the policy is attached to, not to all KMS keys in your account.

A durable function's key policy grants each principal only the AWS KMS actions it needs, scoped by service and function ARN. The following sections describe the statements, conditions, and a complete example.

**Required policy statements**  
The policy grants the following capabilities:
+ **Enable IAM User Permissions**. Grants the account root unconditional access to manage the key. This statement uses no conditions because scoping it would prevent you from rotating, updating, or deleting the key.
+ **Allow Lambda to use this key for durable functions**. Grants the Lambda service principal `kms:GenerateDataKey` and `kms:Decrypt`.
+ **Allow the function execution role to decrypt durable execution data**. Grants the execution role `kms:Decrypt` to read state and progress the execution.
+ **Allow the function author to describe this key**. Grants `kms:DescribeKey` so Lambda can validate that the key is symmetric and enabled during `CreateFunction` or `UpdateFunctionConfiguration`.
+ **Allow the function author to validate this key for a specific function**. Grants `kms:GenerateDataKey` and `kms:Decrypt` so Lambda can validate key permissions and access with the function's encryption context during `CreateFunction` or `UpdateFunctionConfiguration`. This confirms the key policy accepts calls for this specific function before the function is created or updated.
+ **Allow durable execution operators**. Grants operators `kms:Decrypt` for calls to `GetDurableExecution`, `GetDurableExecutionHistory` with `IncludeExecutionData=true`, `GetDurableExecutionState`, `StopDurableExecution`, and the callback APIs.

As a best practice, use separate principals for the execution role, function author, and durable execution operator so each identity has only the capabilities it needs.

**Recommended policy conditions**  
The policy uses the following conditions to scope down access:
+ [https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-via-service](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-via-service) restricts key use to requests routed through Lambda. Applying this to the execution role, function author, and operator statements prevents them from using the key directly through AWS KMS.
+ [https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcearn](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcearn) and [https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount) protect against the [cross-service confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html). Lambda forwards these values when it calls AWS KMS using its own service credentials. This condition applies only to the Lambda service principal statement. The execution role, function author, and operator statements call AWS KMS with the caller's forward access session credentials, which do not carry these headers.
+ [https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-encryption-context](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-encryption-context) scopes the key to a specific function. Lambda adds this to the encryption context on every AWS KMS call for durable execution data.

The following example combines the statements and conditions above.

**Example Key policy for durable functions**  

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111122223333:root" },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow Lambda to use this key for durable functions",
            "Effect": "Allow",
            "Principal": { "Service": "lambda.amazonaws.com" },
            "Action": [ "kms:GenerateDataKey", "kms:Decrypt" ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "111122223333",
                    "aws:SourceArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction",
                    "kms:EncryptionContext:aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
                }
            }
        },
        {
            "Sid": "Allow the function execution role to decrypt durable execution data",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111122223333:role/myDurableFunctionRole" },
            "Action": "kms:Decrypt",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "lambda.us-east-1.amazonaws.com",
                    "kms:EncryptionContext:aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
                }
            }
        },
        {
            "Sid": "Allow the function author to describe this key",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111122223333:role/FunctionAuthor" },
            "Action": "kms:DescribeKey",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "lambda.us-east-1.amazonaws.com"
                }
            }
        },
        {
            "Sid": "Allow the function author to validate this key for a specific function",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111122223333:role/FunctionAuthor" },
            "Action": [ "kms:GenerateDataKey", "kms:Decrypt" ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "lambda.us-east-1.amazonaws.com",
                    "kms:EncryptionContext:aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
                }
            }
        },
        {
            "Sid": "Allow durable execution operators",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111122223333:role/DurableExecutionOperator" },
            "Action": "kms:Decrypt",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "lambda.us-east-1.amazonaws.com",
                    "kms:EncryptionContext:aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
                }
            }
        }
    ]
}
```

For more information about AWS KMS key policies, see [How to change a key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying.html#key-policy-modifying-how-to) in the *AWS Key Management Service Developer Guide*.

### Configure a customer managed key on a durable function
<a name="durable-encryption-configure"></a>

You configure the customer managed key for durable execution data through the `KMSKeyArn` field of the `DurableConfig` object. Set it when you create the function with [CreateFunction](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html); update it on an existing durable function with [UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html).

------
#### [ Lambda console ]

**To configure a customer managed key on an existing durable function**

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.

1. Choose a durable function.

1. Choose **Configuration**, then choose **Durable execution** from the left navigation bar.

1. Choose **Edit**.

1. Under **Encryption**, choose **Use a customer managed key**, and then choose a KMS key from the list.

1. Choose **Save**.

------
#### [ AWS CLI ]

**To configure a customer managed key when you create a function**

In the following [create-function](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/create-function.html) example, the `--durable-config` option specifies the customer managed key ARN along with the durable execution timeout and retention period.

```
aws lambda create-function \
  --function-name myDurableFunction \
  --runtime nodejs24.x \
  --handler index.handler \
  --role arn:aws:iam::111122223333:role/myDurableFunctionRole \
  --zip-file fileb://{{function.zip}} \
  --durable-config '{"KMSKeyArn":"{{arn:aws:kms:us-east-1:111122223333:key/key-id}}","ExecutionTimeout":3600,"RetentionPeriodInDays":30}'
```

**To configure a customer managed key on an existing durable function**

Use the [update-function-configuration](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/update-function-configuration.html) command. Include all `DurableConfig` fields that you want to keep, because `--durable-config` replaces the entire object.

```
aws lambda update-function-configuration \
  --function-name myDurableFunction \
  --durable-config '{"KMSKeyArn":"{{arn:aws:kms:us-east-1:111122223333:key/key-id}}","ExecutionTimeout":3600,"RetentionPeriodInDays":30}'
```

**To remove the customer managed key from a durable function**

Omit `KMSKeyArn` from `--durable-config`. Existing executions keep using the customer managed key they started with. New executions use the default encryption instead.

```
aws lambda update-function-configuration \
  --function-name myDurableFunction \
  --durable-config '{"ExecutionTimeout":3600,"RetentionPeriodInDays":30}'
```

------
#### [ AWS CloudFormation ]

In an `AWS::Lambda::Function` resource, set the `KMSKeyArn` property of `DurableConfig`:

```
Resources:
  MyDurableFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: myDurableFunction
      Runtime: nodejs24.x
      Handler: index.handler
      Role: !GetAtt MyDurableFunctionRole.Arn
      Code:
        ZipFile: |
          // Your durable function code
      DurableConfig:
        KMSKeyArn: "arn:aws:kms:us-east-1:111122223333:key/key-id"
        ExecutionTimeout: 3600
        RetentionPeriodInDays: 30
```

------

**Important**  
Each durable execution uses the customer managed key that was configured on the function when it started. Changing or removing the key affects only executions that start after the change; in-flight executions keep using the key they started with until they complete or fail.

## Reading durable execution data
<a name="durable-encryption-reading-data"></a>

Two read APIs return durable execution data:
+ `GetDurableExecution` returns the current state of a single execution, including its input payload, latest checkpoint data, and result or error information.
+ `GetDurableExecutionHistory` returns the ordered list of events that the execution emitted, showing checkpoint inputs and results, chained-invoke inputs and results, and the final outcome.

Both APIs accept an `IncludeExecutionData` request parameter. When `IncludeExecutionData` is `true`, Lambda uses the caller's credentials to call `kms:Decrypt` on the customer managed key. Lambda then returns the decrypted execution data in the response. The caller's identity must have `kms:Decrypt` on the customer managed key.

When `IncludeExecutionData` is `false`, Lambda does not call AWS KMS or decrypt execution data, and the response sets `ExecutionDataIncluded` to `false`. The response still includes `DurableConfig`, which echoes the customer managed key ARN that the execution used. `IncludeExecutionData` defaults to `false`, so callers that only need metadata don't need AWS KMS permissions.

**Example: `GetDurableExecution` response with `IncludeExecutionData=false`**

```
{
    "DurableExecutionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction:execution:exec-abc123",
    "DurableExecutionName": "exec-abc123",
    "FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction",
    "StartTimestamp": 1733256000,
    "Status": "RUNNING",
    "ExecutionDataIncluded": false,
    "DurableConfig": {
        "ExecutionTimeout": 3600,
        "KMSKeyArn": "arn:aws:kms:us-east-1:111122223333:key/key-id",
        "RetentionPeriodInDays": 30
    }
}
```

## Chained invokes
<a name="durable-encryption-chained-invokes"></a>

When a durable function uses chained invoke to call another durable function, Lambda treats the child execution as an independent durable execution: it has its own execution ID, its own checkpoint stream, and its own customer managed key. The parent's customer managed key configuration has no effect on the child's data, and the child's customer managed key configuration has no effect on the parent's data.

**Permissions**  
The Lambda service principal must have `kms:GenerateDataKey` and `kms:Decrypt` on the child function's customer managed key. If the parent and child functions use different customer managed keys, you grant the service principal access on each key separately. The parent function's execution role does not need permissions on the child's customer managed key.

**Identifying which key encrypted which execution**  
Both `GetDurableExecution` and `ListDurableExecutionsByFunction` return the customer managed key ARN that encrypted each execution. Use these APIs to confirm which key was in effect when a parent or child execution started.

## Data key caching
<a name="durable-encryption-data-key-caching"></a>

To reduce AWS KMS call volume and improve availability during service disruptions, Lambda caches a data key generated from your customer managed key for up to 15 minutes. While the cache is warm, Lambda reuses the same data key across operations within an execution and across executions started during the cache window.

**Cost**  
Per-execution AWS KMS cost stays low because Lambda calls `GenerateDataKey` at most once per cache window, not once per checkpoint. At high request rates, the cost per execution falls further because more executions share each cached data key. You're billed for the AWS KMS calls that Lambda actually makes, not for every checkpoint or read.

**Static stability**  
Data keys stay cached for up to 15 minutes. Changes to your key take effect on the next cache refresh. During extended service disruptions, Lambda continues to serve from the cache, keeping in-flight executions running.

**CloudTrail**  
Data key caching means you see fewer `GenerateDataKey` events in CloudTrail than you have executions or checkpoints. See [Monitoring KMS keys for durable functions](#durable-encryption-monitoring) for example events.

## When the customer managed key is unavailable
<a name="durable-encryption-key-unavailable"></a>

If the customer managed key that an execution started with is disabled, scheduled for deletion, or has its access revoked through the key policy, the execution cannot make further progress. At the next checkpoint, Lambda fails the execution with a non-retryable AWS KMS error. Restoring access to the key does not automatically resume the execution. You must start a new execution.

APIs that read or write payloads also fail when the key is unavailable. They can return one of the following exceptions:
+ `KMSAccessDeniedException`: Lambda could not decrypt durable execution data because access to the KMS key was denied.
+ `KMSDisabledException`: Lambda could not decrypt durable execution data because the KMS key is disabled.
+ `KMSInvalidStateException`: Lambda could not decrypt durable execution data because the state of the KMS key is not valid for `Decrypt`.
+ `KMSNotFoundException`: Lambda could not decrypt durable execution data because the KMS key was not found.

Restoring access to the KMS key lets these read APIs succeed again for executions that already failed. Failed executions stay failed; you must start a new execution.

To inspect execution metadata while the KMS key is unavailable, call `GetDurableExecution` with `IncludeExecutionData=false`. This returns the execution's status, timestamps, and `DurableConfig` (including the KMS key ARN) without calling AWS KMS.

Because Lambda caches data keys, disabling a key does not take effect immediately. For details, see [Data key caching](#durable-encryption-data-key-caching).

**Important**  
Deleting a KMS key that in-flight or retained executions still depend on permanently destroys those executions and their history.

## Monitoring KMS keys for durable functions
<a name="durable-encryption-monitoring"></a>

When you use a customer managed key with a durable function, you can use [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) to track the AWS KMS calls that Lambda makes on your behalf. For general guidance on searching AWS KMS events, see [Searching AWS KMS API activity](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html#searching-kms-ct).

To confirm that Lambda is using your key as intended, look for these fields in each event:
+ `eventName`: one of `GenerateDataKey`, `Decrypt`, or `DescribeKey`
+ `eventSource`: `kms.amazonaws.com`
+ `userIdentity.invokedBy`: `lambda.amazonaws.com`
+ `requestParameters.encryptionContext.aws:lambda:FunctionArn`: the ARN of the durable function

The following examples are CloudTrail events from a `CreateFunction` or `UpdateFunctionConfiguration` call that configures a customer managed key on a durable function. Lambda issues three AWS KMS calls to validate the key: a real `DescribeKey`, and dry-run `GenerateDataKey` and `Decrypt`.

------
#### [ GenerateDataKey ]

When you set or change the `KMSKeyArn` in `DurableConfig`, Lambda issues a dry-run `GenerateDataKey` against your customer managed key to validate that the key policy allows Lambda to derive data keys for this function's encryption context. The dry-run performs no cryptographic work but records a full CloudTrail event. The following example event records the dry-run `GenerateDataKey` operation:

```
{
    "eventVersion": "1.11",
    "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROA123456789EXAMPLE:example",
        "arn": "arn:aws:sts::111122223333:assumed-role/FunctionAuthor/example",
        "accountId": "111122223333",
        "accessKeyId": "ASIA123456789EXAMPLE",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROA123456789EXAMPLE",
                "arn": "arn:aws:iam::111122223333:role/FunctionAuthor",
                "accountId": "111122223333",
                "userName": "FunctionAuthor"
            },
            "attributes": {
                "creationDate": "2026-01-15T16:54:42Z",
                "mfaAuthenticated": "false"
            }
        },
        "invokedBy": "lambda.amazonaws.com"
    },
    "eventTime": "2026-01-15T16:55:00Z",
    "eventSource": "kms.amazonaws.com",
    "eventName": "GenerateDataKey",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "lambda.amazonaws.com",
    "userAgent": "lambda.amazonaws.com",
    "errorCode": "DryRunOperationException",
    "errorMessage": "The request would have succeeded, but the DryRun option is set.",
    "requestParameters": {
        "encryptionContext": {
            "aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
        },
        "dryRun": true,
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/key-id",
        "keySpec": "AES_256"
    },
    "responseElements": null,
    "additionalEventData": {
        "keyMaterialId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0EXAMPLE"
    },
    "requestID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEaaaaa",
    "eventID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEbbbbb",
    "readOnly": true,
    "resources": [
        {
            "accountId": "111122223333",
            "type": "AWS::KMS::Key",
            "ARN": "arn:aws:kms:us-east-1:111122223333:key/key-id"
        }
    ],
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management"
}
```

------
#### [ Decrypt ]

When you set or change the `KMSKeyArn` in `DurableConfig`, Lambda also issues a dry-run `Decrypt` against your customer managed key to validate that the key policy allows Lambda to decrypt data for this function's encryption context. The dry-run uses `IGNORE_CIPHERTEXT`, so no real ciphertext is required. The following example event records the dry-run `Decrypt` operation:

```
{
    "eventVersion": "1.11",
    "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROA123456789EXAMPLE:example",
        "arn": "arn:aws:sts::111122223333:assumed-role/FunctionAuthor/example",
        "accountId": "111122223333",
        "accessKeyId": "ASIA123456789EXAMPLE",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROA123456789EXAMPLE",
                "arn": "arn:aws:iam::111122223333:role/FunctionAuthor",
                "accountId": "111122223333",
                "userName": "FunctionAuthor"
            },
            "attributes": {
                "creationDate": "2026-01-15T16:54:42Z",
                "mfaAuthenticated": "false"
            }
        },
        "invokedBy": "lambda.amazonaws.com"
    },
    "eventTime": "2026-01-15T16:55:00Z",
    "eventSource": "kms.amazonaws.com",
    "eventName": "Decrypt",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "lambda.amazonaws.com",
    "userAgent": "lambda.amazonaws.com",
    "errorCode": "DryRunOperationException",
    "errorMessage": "The request would have succeeded, but the DryRun option is set.",
    "requestParameters": {
        "encryptionContext": {
            "aws:lambda:FunctionArn": "arn:aws:lambda:us-east-1:111122223333:function:myDurableFunction"
        },
        "dryRun": true,
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/key-id",
        "dryRunModifiers": ["IGNORE_CIPHERTEXT"],
        "encryptionAlgorithm": "SYMMETRIC_DEFAULT"
    },
    "responseElements": null,
    "additionalEventData": {
        "keyMaterialId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0EXAMPLE"
    },
    "requestID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEaaaaa",
    "eventID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEbbbbb",
    "readOnly": true,
    "resources": [
        {
            "accountId": "111122223333",
            "type": "AWS::KMS::Key",
            "ARN": "arn:aws:kms:us-east-1:111122223333:key/key-id"
        }
    ],
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management"
}
```

------
#### [ DescribeKey ]

When you set or change the `KMSKeyArn` in `DurableConfig`, Lambda calls `DescribeKey` to confirm that the key is symmetric and enabled before it accepts the change. Unlike the `GenerateDataKey` and `Decrypt` probes, this is a real call, not a dry-run. The following example event records the `DescribeKey` operation:

```
{
    "eventVersion": "1.11",
    "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROA123456789EXAMPLE:example",
        "arn": "arn:aws:sts::111122223333:assumed-role/FunctionAuthor/example",
        "accountId": "111122223333",
        "accessKeyId": "ASIA123456789EXAMPLE",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROA123456789EXAMPLE",
                "arn": "arn:aws:iam::111122223333:role/FunctionAuthor",
                "accountId": "111122223333",
                "userName": "FunctionAuthor"
            },
            "attributes": {
                "creationDate": "2026-01-15T16:54:42Z",
                "mfaAuthenticated": "false"
            }
        },
        "invokedBy": "lambda.amazonaws.com"
    },
    "eventTime": "2026-01-15T16:55:00Z",
    "eventSource": "kms.amazonaws.com",
    "eventName": "DescribeKey",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "lambda.amazonaws.com",
    "userAgent": "lambda.amazonaws.com",
    "requestParameters": {
        "keyId": "arn:aws:kms:us-east-1:111122223333:key/key-id"
    },
    "responseElements": null,
    "requestID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEaaaaa",
    "eventID": "a1b2c3d4-5678-90ab-cdef-EXAMPLEbbbbb",
    "readOnly": true,
    "resources": [
        {
            "accountId": "111122223333",
            "type": "AWS::KMS::Key",
            "ARN": "arn:aws:kms:us-east-1:111122223333:key/key-id"
        }
    ],
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "111122223333",
    "eventCategory": "Management"
}
```

------

## Related encryption topics
<a name="durable-encryption-related"></a>
+ [Data encryption at rest for Lambda](security-encryption-at-rest.md)
+ [Securing Lambda environment variables](configuration-envvars-encryption.md)
+ [Encrypting Lambda .zip deployment packages](encrypt-zip-package.md)
+ [Security model for Lambda SnapStart](snapstart-security.md)
+ [Configure Lambda durable functions](durable-configuration.md)