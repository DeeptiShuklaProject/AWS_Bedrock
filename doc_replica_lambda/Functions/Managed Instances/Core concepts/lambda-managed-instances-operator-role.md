

# Lambda operator role for Lambda Managed Instances
<a name="lambda-managed-instances-operator-role"></a>

When you use Lambda Managed Instances, Lambda needs permissions to manage compute capacity in your account. The operator role provides these permissions through IAM policies that allow Lambda to manage EC2 instances in the capacity provider.

Lambda assumes the operator role when performing these management operations, similar to how Lambda assumes an execution role when your function runs.

## Creating an operator role
<a name="lambda-managed-instances-creating-operator-role"></a>

You can create an operator role in the IAM console or with the AWS CLI. The role must include:
+ **Permissions policy** – Grants permissions to manage capacity providers and associated resources
+ **Trust policy** – Allows the Lambda service (`lambda.amazonaws.com`) to assume the role

### Permissions policy
<a name="lambda-managed-instances-operator-role-permissions-policy"></a>

The operator role needs permissions to manage capacity providers and the underlying compute resources. At minimum, the role requires the permissions in the [AWSLambdaManagedEC2ResourceOperator](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/policies/details/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAWSLambdaManagedEC2ResourceOperator) managed policy, currently:

```
{
  "Version": "2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances",
        "ec2:CreateTags",
        "ec2:AttachNetworkInterface"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:volume/*"
      ],
      "Condition": {
        "StringEquals": {
          "ec2:ManagedResourceOperator": "scaler.lambda.amazonaws.com"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeCapacityReservations",
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeInstanceTypeOfferings",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets",
        "ec2:DescribeVpcEncryptionControls"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances",
        "ec2:CreateNetworkInterface"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:subnet/*",
        "arn:aws:ec2:*:*:security-group/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:image/*"
      ],
      "Condition": {
        "StringEquals": {
          "ec2:Owner": "amazon"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:*:log-stream:*"
    }
  ]
}
```

### Trust policy
<a name="lambda-managed-instances-operator-role-trust-policy"></a>

The trust policy allows Lambda to assume the operator role:

```
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

## Service-Linked Role for Lambda Managed Instances
<a name="lambda-managed-instances-service-linked-role-for-lmi"></a>

To responsibly manage the lifecycle of Lambda Managed Instances, Lambda requires persistent access to terminate managed instances in your account. Lambda uses an AWS Identity and Access Management (IAM) service-linked role (SLR) to perform these operations.

**Automatic creation**: The service-linked role is automatically created the first time you create a capacity provider. The user creating the first capacity provider must have the `iam:CreateServiceLinkedRole` permission for the `lambda.amazonaws.com` principal.

**Permissions**: The service-linked role grants Lambda the following permissions on managed instances:
+ `ec2:TerminateInstances` – To terminate instances at the end of their lifecycle
+ `ec2:DescribeInstances` – To enumerate managed instances

**Deletion**: You can only delete this service-linked role after you have deleted all Lambda Managed Instances capacity providers in your account.

For more information about service-linked roles, see [Using service-linked roles for Lambda](using-service-linked-roles.md).