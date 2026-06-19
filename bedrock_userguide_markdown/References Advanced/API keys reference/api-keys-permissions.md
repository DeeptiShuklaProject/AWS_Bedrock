

# Control permissions for generating and using Amazon Bedrock API keys
<a name="api-keys-permissions"></a>

The generation and usage of Amazon Bedrock API keys is controlled by actions and condition keys in both the Amazon Bedrock and IAM services.

**Controlling the generation of Amazon Bedrock API keys**  
The [iam:CreateServiceSpecificCredential](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsidentityandaccessmanagementiam.html#awsidentityandaccessmanagementiam-actions-as-permissions) action controls the generation of a service-specific key (such as a long-term Amazon Bedrock API key). You can scope this action to IAM users as a resource to limit the users for which a key can be generated.

You can use the following condition keys to impose conditions on the permission for the `iam:CreateServiceSpecificCredential` action:
+ [iam:ServiceSpecificCredentialAgeDays](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#ck_ServiceSpecificCredentialAgeDays) – Lets you specify, in the condition, the key's expiration time in days. For example, you can use this condition key to only allow the creation of API keys that expire within 90 days.
+ [iam:ServiceSpecificCredentialServiceName](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#ck_ServiceSpecificCredentialAgeDays) – Lets you specify, in the condition, the name of a service. For example, you can use this condition key to only allow the creation of API keys for Amazon Bedrock and not other services.

**Controlling the usage of Amazon Bedrock API keys**  
The [bedrock:CallWithBearerToken](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions) action controls the use of a short-term or long-term Amazon Bedrock API key.

You can use the `bedrock:bearerTokenType` condition key with [string condition operators](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html#Conditions_String) to specify the type of bearer token for which to apply the permission for `bedrock:CallWithBearerToken`. You can specify one of the following values:
+ `SHORT_TERM` – Specifies short-term Amazon Bedrock API keys in the condition.
+ `LONG_TERM` – Specifies long-term Amazon Bedrock API keys in the condition.

The following table summarizes how to prevent an identity from generating or using Amazon Bedrock API keys:


****  

| Purpose | Long-term key | Short-term key | 
| --- | --- | --- | 
| Prevent generation of keys | Attach a policy that denies the iam:CreateServiceSpecificCredential action to an IAM identity. | N/A | 
| Prevent usage of a key | Attach a policy that denies the bedrock:CallWithBearerToken action to the IAM user associated with the key. | Attach a policy that denies the bedrock:CallWithBearerToken action to IAM identities that you don't want to be able to use the key. | 

**Warning**  
Because a short-term Amazon Bedrock API key uses existing credentials from a session, you can prevent its usage by denying the `bedrock:CallWithBearerToken` action on the identity that generated the key. However, you can't prevent generation of a short-term key.

## Example policies to control generation and usage of API keys
<a name="api-keys-permissions-examples"></a>

For example IAM policies to control the generation and usage of API keys, select from the following topics:

**Topics**
+ [Prevent an identity from generating long-term keys and from using Amazon Bedrock API keys](#api-keys-permissions-examples-prevent-generation-and-use)
+ [Prevent an identity from using short-term API keys](#api-keys-permissions-examples-prevent-use-short-term)
+ [Prevent an identity from using long-term API keys](#api-keys-permissions-examples-prevent-use-long-term)
+ [Explicitly prevent an identity from using short-term API keys](#api-keys-permissions-examples-deny-use-short-term-explicitly)
+ [Explicitly prevent an identity from using long-term API keys](#api-keys-permissions-examples-deny-use-long-term-explicitly)
+ [Allow the creation of Amazon Bedrock keys only if they expire within 90 days](#api-keys-permissions-examples-allow-bedrock-keys-expire-within-90-days)

### Prevent an identity from generating long-term keys and from using Amazon Bedrock API keys
<a name="api-keys-permissions-examples-prevent-generation-and-use"></a>

To prevent an IAM identity from generating long-term Amazon Bedrock API keys and using any Amazon Bedrock API keys, attach the following policy to the identity:

------
#### [ JSON ]

****  

```
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid":"DenyBedrockShortAndLongTermAPIKeys",
      "Effect": "Deny",
      "Action": [
        "iam:CreateServiceSpecificCredential",
        "bedrock:CallWithBearerToken"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

------

**Warning**  
You can't prevent the generation of short-term keys.
This policy will prevent the creation of credentials for all AWS services that support creating service-specific credentials. For more information, see [Service-specific credentials for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_service-specific-creds.html).

### Prevent an identity from using short-term API keys
<a name="api-keys-permissions-examples-prevent-use-short-term"></a>

To prevent an IAM identity from using short-term Amazon Bedrock API keys, attach the following policy to the identity:

### Prevent an identity from using long-term API keys
<a name="api-keys-permissions-examples-prevent-use-long-term"></a>

To prevent an IAM identity from using long-term Amazon Bedrock API keys, attach the following policy to the identity:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "bedrock:CallWithBearerToken",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "bedrock:bearerTokenType": "LONG_TERM"
                }
            }
        }
    ]
}
```

------

### Explicitly prevent an identity from using short-term API keys
<a name="api-keys-permissions-examples-deny-use-short-term-explicitly"></a>

To explicitly prevent an IAM identity from using short-term Amazon Bedrock API keys, but allow other API key usage, attach the following policy to the identity:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "bedrock:CallWithBearerToken",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "bedrock:bearerTokenType": "SHORT_TERM"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "bedrock:CallWithBearerToken",
            "Resource": "*"
        }
    ]
}
```

------

### Explicitly prevent an identity from using long-term API keys
<a name="api-keys-permissions-examples-deny-use-long-term-explicitly"></a>

To explicitly prevent an IAM identity from using long-term Amazon Bedrock API keys, but allow other API key usage, attach the following policy to the identity:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "bedrock:CallWithBearerToken",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "bedrock:bearerTokenType": "LONG_TERM"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "bedrock:CallWithBearerToken",
            "Resource": "*"
        }
    ]
}
```

------

### Allow the creation of Amazon Bedrock keys only if they expire within 90 days
<a name="api-keys-permissions-examples-allow-bedrock-keys-expire-within-90-days"></a>

To allow an IAM identity to create a long-term API key only if it is for Amazon Bedrock and if the expiration time is 90 days or less, attach the following policy to the identity:

------
#### [ JSON ]

****  

```
{
   "Version":"2012-10-17",		 	 	 
   "Statement": [
       {
           "Effect": "Allow",
           "Action": "iam:CreateServiceSpecificCredential",
           "Resource": "arn:aws:iam::123456789012:user/{{username}}",
           "Condition": {
               "StringEquals": {
                   "iam:ServiceSpecificCredentialServiceName": "bedrock.amazonaws.com"
               },
               "NumericLessThanEquals": {
                   "iam:ServiceSpecificCredentialAgeDays": "90"
               }
           }
       }
   ]
}
```

------