

# Identity-based policy examples for Amazon Bedrock Agents
<a name="security_iam_id-based-policy-examples-agent"></a>

Select a topic to see example IAM policies that you can attach to an IAM role to provision permissions for actions in [Automate tasks in your application using AI agents](agents.md).

**Topics**
+ [Required permissions for Amazon Bedrock Agents](#iam-agents-ex-all)
+ [Allow users to view information about and invoke an agent](#security_iam_id-based-policy-examples-perform-actions-agent)
+ [Control access to service tiers](#security_iam_id-based-policy-examples-service-tiers)

## Required permissions for Amazon Bedrock Agents
<a name="iam-agents-ex-all"></a>

For an IAM identity to use Amazon Bedrock Agents, you must configure it with the necessary permissions. You can attach the [AmazonBedrockFullAccess](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonBedrockFullAccess) policy to grant the proper permissions to the role.

To restrict permissions to only actions that are used in Amazon Bedrock Agents, attach the following identity-based policy to an IAM role:

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AgentPermissions",
            "Effect": "Allow",
            "Action": [  
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel",
                "bedrock:TagResource", 
                "bedrock:UntagResource", 
                "bedrock:ListTagsForResource", 
                "bedrock:CreateAgent", 
                "bedrock:UpdateAgent", 
                "bedrock:GetAgent", 
                "bedrock:ListAgents", 
                "bedrock:DeleteAgent",
                "bedrock:CreateAgentActionGroup", 
                "bedrock:UpdateAgentActionGroup", 
                "bedrock:GetAgentActionGroup", 
                "bedrock:ListAgentActionGroups", 
                "bedrock:DeleteAgentActionGroup",
                "bedrock:GetAgentVersion",
                "bedrock:ListAgentVersions", 
                "bedrock:DeleteAgentVersion",
                "bedrock:CreateAgentAlias", 
                "bedrock:UpdateAgentAlias",               
                "bedrock:GetAgentAlias",
                "bedrock:ListAgentAliases",
                "bedrock:DeleteAgentAlias",
                "bedrock:AssociateAgentKnowledgeBase",
                "bedrock:DisassociateAgentKnowledgeBase",
                "bedrock:ListAgentKnowledgeBases",
                "bedrock:GetKnowledgeBase",
                "bedrock:ListKnowledgeBases",
                "bedrock:PrepareAgent",
                "bedrock:InvokeAgent",
                "bedrock:AssociateAgentCollaborator",
                "bedrock:DisassociateAgentCollaborator",
                "bedrock:GetAgentCollaborator",
                "bedrock:ListAgentCollaborators",
                "bedrock:UpdateAgentCollaborator"
            ],
            "Resource": "*"
        }
    ]   
}
```

------

You can further restrict permissions by omitting [actions](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-actions) or specifying [resources](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-resources) and [condition keys](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies-conditionkeys). An IAM identity can call API operations on specific resources. For example, the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) operation can only be used on agent resources and the [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) operation can only be used on alias resources. For API operations that aren't used on a specific resource type (such as [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html)), specify \* as the `Resource`. If you specify an API operation that can't be used on the resource specified in the policy, Amazon Bedrock returns an error.

## Allow users to view information about and invoke an agent
<a name="security_iam_id-based-policy-examples-perform-actions-agent"></a>

The following is a sample policy that you can attach to an IAM role to allow it to view information about or edit an agent with the ID {{AGENT12345}} and to interact with its alias with the ID {{ALIAS12345}}. For example, you could attach this policy to a role that you want to only have permissions to troubleshoot an agent and update it.

------
#### [ JSON ]

****  

```
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "GetAndUpdateAgent",
            "Effect": "Allow",
            "Action": [
                "bedrock:GetAgent",
                "bedrock:UpdateAgent"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:agent/AgentId"
        },
        {
            "Sid": "InvokeAgent",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent"
            ],
            "Resource": "arn:aws:bedrock:us-east-1:123456789012:agent-alias/AgentId/AgentAliasId"
        }
    ]
}
```

------

## Control access to service tiers
<a name="security_iam_id-based-policy-examples-service-tiers"></a>

Amazon Bedrock service tiers provide different levels of processing priority and pricing for inference requests. By default, all service tiers (priority, default, and flex) are available to users with proper Bedrock permissions, following an allowlist approach where access is granted unless explicitly restricted.

However, organizations may want to control which service tiers their users can access to manage costs or enforce usage policies. You can implement access restrictions by using IAM policies with the `bedrock:ServiceTier` condition key to deny access to specific service tiers. This approach allows you to maintain granular control over which team members can use premium service tiers like "priority" or cost-optimized tiers like "flex".

The following example shows an identity-based policy that denies access to all service tiers. This type of policy is useful when you want to prevent users from specifying any service tier, forcing them to use the system default behavior:

```
{
    "Version": "2012-10-17", 		 	 	 
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "bedrock:InvokeModel",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "bedrock:ServiceTier": ["reserved", "priority", "default", "flex"]
                }
            }
        }
    ]
}
```

You can customize this policy to deny access to only specific service tiers by modifying the `bedrock:ServiceTier` condition values. For example, to deny only the premium "priority" tier while allowing "default" and "flex", you would specify only `["priority"]` in the condition. This flexible approach allows you to implement usage policies that align with your organization's cost management and operational requirements. For more information about service tiers, see [Service tiers for optimizing performance and cost](service-tiers-inference.md).