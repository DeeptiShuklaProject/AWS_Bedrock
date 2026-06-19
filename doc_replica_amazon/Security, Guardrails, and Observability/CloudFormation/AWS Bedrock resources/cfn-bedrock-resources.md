

# `AWS::Bedrock` resources
<a name="cfn-bedrock-resources"></a>

The `AWS::Bedrock` namespace contains the Amazon Bedrock control-plane resources that you create through `bedrock` and : agents, knowledge bases, flows, guardrails, and prompts.

## Amazon Bedrock and CloudFormation templates
<a name="working-with-templates"></a>

To provision and configure resources for Amazon Bedrock and related services, you must understand [CloudFormation templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html). Templates are formatted text files in JSON or YAML. These templates describe the resources that you want to provision in your CloudFormation stacks. If you're unfamiliar with JSON or YAML, you can use CloudFormation Designer to help you get started with CloudFormation templates. For more information, see [What is CloudFormation Designer?](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/working-with-templates-cfn-designer.html) in the *AWS CloudFormation User Guide*.

Amazon Bedrock supports creating the following resources in CloudFormation.
+ [AWS::Bedrock::Agent](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html)
+ [AWS::Bedrock::AgentAlias](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html)
+ [AWS::Bedrock::ApplicationInferenceProfile](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-applicationinferenceprofile.html)
+ [AWS::Bedrock::AutomatedReasoningPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-automatedreasoningpolicy.html)
+ [AWS::Bedrock::AutomatedReasoningPolicyVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-automatedreasoningpolicyversion.html)
+ [AWS::Bedrock::DataSource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html)
+ [AWS::Bedrock::Flow](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-flow.html)
+ [AWS::Bedrock::FlowVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-flowversion.html)
+ [AWS::Bedrock::FlowAlias](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-flowalias.html)
+ [AWS::Bedrock::Guardrail](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-guardrail.html)
+ [AWS::Bedrock::GuardrailVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-guardrailversion.html)
+ [AWS::Bedrock::KnowledgeBase](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html)
+ [AWS::Bedrock::Prompt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-prompt.html)
+ [AWS::Bedrock::PromptVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-promptversion.html)

For more information, including examples of JSON and YAML templates for [Amazon Bedrock agents](agents.md) or [Amazon Bedrock knowledge bases](knowledge-base.md), see the [Amazon Bedrock resource type reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Bedrock.html) in the *AWS CloudFormation User Guide*.