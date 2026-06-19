

# IAM policies for Amazon Bedrock Projects
<a name="security-iam-projects"></a>

You can use IAM policies to control access to Amazon Bedrock Projects resources. These are standard IAM identity-based policies that you attach to IAM users, groups, or roles. The policies use the `Resource` element to scope permissions to specific project ARNs. For general information about creating and managing IAM policies, see [Managing IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html) in the *IAM User Guide*.

## Example IAM policies for Projects
<a name="security-iam-projects-examples"></a>

The following examples show IAM policy documents that grant access to Bedrock Projects resources. Attach these policies to IAM users, groups, or roles using the IAM console, CLI, or API.

### Deny project creation
<a name="security-iam-projects-deny-create"></a>

The following policy prevents a user from creating new projects:

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "DenyProjectCreation",
            "Effect": "Deny",
            "Action": "bedrock-mantle:CreateProject",
            "Resource": "*"
        }
    ]
}
```

### Read-only access to a project
<a name="security-iam-projects-readonly"></a>

The following policy grants read-only access to a specific project:

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "ReadOnlyProjectAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock-mantle:GetProject",
                "bedrock-mantle:ListProjects",
                "bedrock-mantle:ListTagsForResources",
                "bedrock-mantle:CreateInference"
            ],
            "Resource": "arn:aws:bedrock-mantle:us-east-1:123456789012:project/proj_abc123"
        }
    ]
}
```

### Full access to a project
<a name="security-iam-projects-full-access"></a>

The following policy grants full access to all Bedrock Projects actions on a specific project:

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Sid": "FullProjectAccess",
            "Effect": "Allow",
            "Action": "bedrock-mantle:*",
            "Resource": "arn:aws:bedrock-mantle:us-east-1:123456789012:project/proj_abc123"
        }
    ]
}
```