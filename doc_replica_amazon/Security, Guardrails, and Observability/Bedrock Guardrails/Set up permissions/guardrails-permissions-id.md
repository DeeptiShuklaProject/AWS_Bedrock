

# Enforce the use of specific guardrails in model inference requests
<a name="guardrails-permissions-id"></a>

You can enforce the use of a specific guardrail for model inference by including the `bedrock:GuardrailIdentifier` condition key in your IAM policy. This allows you to deny any inference API request that doesn't include the guardrail configured in your IAM policy.

You can apply this enforcement for the following inference APIs:
+ [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
+ [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html)
+ [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
+ [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)

The following examples are some ways in which you can using the `bedrock:GuardrailIdentifier` condition key.

**Example 1: Enforce the use of a specific guardrail and its numeric version**  
Use the following policy to enforce the use of a specific guardrail (`{{guardrail-id}}`) and its numeric version 1 during model inference.  
The explicit deny keeps the user request from calling the listed actions with any other `GuardrailIdentifier` and guardrail version no matter what other permissions the user might have.    
****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModelStatement1",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}:{{1}}"
                }
            }
        },
        {
            "Sid": "InvokeFoundationModelStatement2",
            "Effect": "Deny",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringNotEquals": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}:{{1}}"
                }
            }
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
            ]
        }
    ]
}
```

**Example 2: Enforce the use of a specific guardrail and its DRAFT version**  
Use the following policy to enforce the use of a specific guardrail (`{{guardrail-id}}`) and its DRAFT version during model inference.    
****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModelStatement1",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
                }
            }
        },
        {
            "Sid": "InvokeFoundationModelStatement2",
            "Effect": "Deny",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringNotEquals": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
                }
            }
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
            ]
        }
    ]
}
```

**Example 3: Enforce the use of a specific guardrail and any of its numeric versions**  
Use the following policy to enforce the use of a specific guardrail (`{{guardrail-id}}`) and any of its numeric versions during model inference.    
****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModelStatement1",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "ArnLike": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}:*"
                }
            }
        },
        {
            "Sid": "InvokeFoundationModelStatement2",
            "Effect": "Deny",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "ArnNotLike": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}:*"
                }
            }
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
            ]
        }
    ]
}
```

**Example 4: Enforce the use of a specific guardrail and any of its versions**  
Use the following policy to enforce the use of a specific guardrail (`{{guardrail-id}}`) and any of its numeric versions (including the DRAFT version) during model inference.    
****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModelStatement1",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "ArnLike": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}*"
                }
            }
        },
        {
            "Sid": "InvokeFoundationModelStatement2",
            "Effect": "Deny",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "ArnNotLike": {
                    "bedrock:GuardrailIdentifier": "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}*"
                }
            }
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-id}}"
            ]
        }
    ]
}
```

**Example 5: Enforce the use of specific guardrail and version pairs**  
Use the following policy to allow model inference for only a set of guardrails and their respective versions.    
****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "InvokeFoundationModelStatement1",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringEquals": {
                    "bedrock:GuardrailIdentifier": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-1-id}}:{{1}}",
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-2-id}}:{{2}}",
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-3-id}}"
                    ]
                }
            }
        },
        {
            "Sid": "InvokeFoundationModelStatement2",
            "Effect": "Deny",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}::foundation-model/*"
            ],
            "Condition": {
                "StringNotEquals": {
                    "bedrock:GuardrailIdentifier": [
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-1-id}}:{{1}}",
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-2-id}}:{{2}}",
                        "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-3-id}}"
                    ]
                }
            }
        },
        {
            "Sid": "ApplyGuardrail",
            "Effect": "Allow",
            "Action": [
                "bedrock:ApplyGuardrail"
            ],
            "Resource": [
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-1-id}}",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-2-id}}",
                "arn:aws:bedrock:{{us-east-1}}:{{123456789012}}:guardrail/{{guardrail-3-id}}"
            ]
        }
    ]
}
```

**Limitations**  
If a user assumes an IAM role that has a specific guardrail configured using the `bedrock:GuardrailIdentifier` condition key:  
+ A user should not use the same role with additional permissions to invoke Bedrock APIs like `RetrieveAndGenerate` and `InvokeAgent` that make `InvokeModel` calls on behalf of the user. This can lead to access denied errors even when the guardrail is specified in the request because `RetrieveAndGenerate` and `InvokeAgent` make multiple `InvokeModel` calls, and some of these calls don't include a guardrail.
+ A user can bypass applying a guardrail in their prompt by using [guardrail input tags](guardrails-tagging.md). However, the guardrail is always applied on the response.
+ Since Amazon Bedrock Guardrails don't currently support resource-based policies for cross-account access, your guardrail must be in the same AWS account as the IAM role making the request.