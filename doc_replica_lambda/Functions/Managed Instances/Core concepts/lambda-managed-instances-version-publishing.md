

# $LATEST.PUBLISHED version in Lambda Managed Instances
<a name="lambda-managed-instances-version-publishing"></a>

Lambda Managed Instances functions support the same numbered versioning workflow as Lambda (default). If you prefer not to maintain numbered versions, Lambda Managed Instances introduces a new version type: `$LATEST.PUBLISHED`. This version allows you to create or republish a latest published version as needed with updated code or configuration, without managing numbered versions.

**Key difference from $LATEST:** When you invoke a Lambda Managed Instances function using an unqualified ARN, Lambda implicitly invokes the `$LATEST.PUBLISHED` version rather than the unpublished $LATEST version.

The following AWS CLI command creates or republishes the `$LATEST.PUBLISHED` version.

```
aws lambda publish-version --function-name my-function --publish-to LATEST_PUBLISHED
```

You should see the following output:

```
{
  "FunctionName": "my-function",
  "FunctionArn": "arn:aws:lambda:us-east-2:123456789012:function:my-function:$LATEST.PUBLISHED",
  "Version": "$LATEST.PUBLISHED",
  "Role": "arn:aws:iam::123456789012:role/lambda-role",
  "Handler": "function.handler",
  "Runtime": "nodejs24.x",
  ...
}
```

**Note**  
If you use AWS CloudFormation or the Lambda console to create a Lambda Managed Instances function, Lambda automatically creates the `$LATEST.PUBLISHED` version.