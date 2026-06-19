

# Block denied topics to help remove harmful content
<a name="guardrails-denied-topics"></a>

You can specify a set of denied topics in a guardrail that are undesirable in the context of your generative AI application. For example, a bank might want its AI assistant to avoid conversations related to investment advice or cryptocurrencies. 

Model prompts and responses in natural language, as well as code-related content in Standard tier, are evaluated against each denied topic in your guardrail. If one of the denied topics is detected, your guardrail returns a blocked message.

Create a denied topic with the following parameters, which your guardrail uses to detect if a prompt or response belongs to the topic:
+ **Name** – The name of the topic. The name should be a noun or a phrase. Don't describe the topic in the name. For example:
  + **Investment Advice**
+ **Definition** – Up to 200 characters summarizing the topic content. The definition should describe the content of the topic and its subtopics.

  The following is an example topic definition that you can provide:

  **Investment advice is inquiries, guidance, or recommendations about the management or allocation of funds or assets with the goal of generating returns or achieving specific financial objectives.**
+ **Sample phrases** (optional) – A list of up to five sample phrases that refer to the topic. Each phrase can be up to 100 characters long. A sample is a prompt or continuation that shows what kind of content should be filtered out. For example:
  + **Is investing in the stocks better than bonds?**
  + **Should I invest in gold?**

## Best practices for creating denied topics
<a name="guardrails-denied-topics-best-practices"></a>
+ Define the topic in a crisp and precise manner. A clear and unambiguous topic definition can improve the accuracy of the topic's detection. For example, a topic to detect queries or statements associated with cryptocurrencies can be defined as **Question or information associated with investing, selling, transacting, or procuring cryptocurrencies**.
+ Don't include examples or instructions in the topic definition. For example, **Block all contents associated to cryptocurrency** is an instruction and not a definition of the topic. Such instructions must not be used as part of topic's definitions.
+ Don't define negative topics or exceptions. For example, **All contents except medical information** or **Contents not containing medical information** are negative definitions of a topic and must not be used.
+ Don't use denied topics to capture entities or words. For example, **Statement or questions containing the name of a person "X"** or **Statements with a competitor name Y**. The topic definitions represent a theme or a subject and guardrails evaluates an input contextually. Topic filtering should not be used to capture individual words or entity types. For more information, see [Remove PII from conversations by using sensitive information filters](guardrails-sensitive-filters.md), or [Remove a specific list of words and phrases from conversations with word filters](guardrails-word-filters.md) for these use cases.

## Add denied topics to your guardrail
<a name="guardrails-denied-topics-configure"></a>

You can add up to 30 denied topics to your guardrail by using the AWS Management Console or Amazon Bedrock API.

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Guardrails**, and then choose **Create guardrail**.

1. For **Provide guardrail details** page, do the following:

   1. In the **Guardrail details** section, provide a **Name** and optional **Description** for the guardrail.

   1. For **Messaging for blocked prompts**, enter a message that displays when your guardrail is applied. Select the **Apply the same blocked message for responses** checkbox to use the same message when your guardrail is applied on the response.

   1. (Optional) To enable [cross-Region inference](guardrails-cross-region.md) for your guardrail, expand **Cross-Region inference**, and then select **Enable cross-Region inference for your guardrail**. Choose a guardrail profile that defines the destination AWS Regions where guardrail inference requests can be routed.

   1. (Optional) By default, your guardrail is encrypted with an AWS managed key. To use your own customer-managed KMS key, expand **KMS key selection** and select the **Customize encryption settings (advanced)** checkbox.

      You can select an existing AWS KMS key or select **Create an AWS KMS key** to create a new one.

   1. (Optional) To add tags to your guardrail, expand **Tags**, and then, select **Add new tag** for each tag you define.

      For more information, see [Tagging Amazon Bedrock resources](tagging.md).

   1. Choose **Next**.

1. When you get to the **Add denied topics** page, choose **Add denied topic** and do the following:

   1. Enter a **Name** for the topic.

   1. For **Definition**, define the topic. For guidelines on how to define a denied topic, see [Block denied topics to help remove harmful content](#guardrails-denied-topics).

   1. (Optional) For **Input**, specify whether guardrail evaluation is enabled for model prompts. If enabled, choose which action you want your guardrail. **Block** is enabled by default. For more information, see [Options for handling harmful content detected by Amazon Bedrock Guardrails](guardrails-harmful-content-handling-options.md).

   1. (Optional) For **Output**, specify whether guardrail evaluation is enabled for model responses. If enabled, choose which action you want your guardrail to take on responses. **Block** is enabled by default. For more information, see [Options for handling harmful content detected by Amazon Bedrock Guardrails](guardrails-harmful-content-handling-options.md).

   1. (Optional) Expand **Add sample phrases** and enter a phrase that's representative of prompts or responses related to this topic. You can enter up to five phrases. For each phrase you include, select **Add phrase**.

   1. For **Denied topics tier**, choose the safeguard tier that you want your guardrail to use for blocking topics in prompts and responses. For more information, see [Safeguard tiers for guardrails policies](guardrails-tiers.md).

   1. When you're done configuring the denied topic, select **Confirm**.

   1. Repeat the previous steps to create additional denied topics.

   1. Choose **Next** to configure other policies as needed or **Skip to Review and create** to finish creating your guardrail.

1. Review the settings for your guardrail.

   1. Select **Edit** in any section you want to make changes to.

   1. When you're done configuring policies, select **Create** to create the guardrail.

------
#### [ API ]

Add denied topics to your guardrail by sending a [CreateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateGuardrail.html) request. Here's what the request format looks like:

```
POST /guardrails HTTP/1.1
Content-type: application/json

{
   "blockedInputMessaging": "string",
   "blockedOutputsMessaging": "string",
   "topicPolicyConfig": {
      "topicsConfig": [ 
         { 
            "definition": "string",
            "examples": [ "string" ],
            "inputAction": "BLOCK | NONE",
            "inputEnabled": true,
            "name": "string",
            "outputAction": "BLOCK | NONE",
            "outputEnabled": true,
            "type": "DENY"
         },
      "tierConfig": { 
         "tierName": "CLASSIC | STANDARD"
      },
      ]
   },
   "crossRegionConfig": { 
      "guardrailProfileIdentifier": "string"
   },
   "description": "string",
   "name": "string"
}
```
+ Specify messages for when the guardrail successfully blocks a prompt or a model response in the `blockedInputMessaging` and `blockedOutputsMessaging` fields.
+ Specify topics for the guardrail to deny in the `topicPolicyConfig` object. Each item in the `topicsConfig` list pertains to one topic.
  + Specify a `name` and `definition` for the topic that should be denied.
  + Specify `DENY` in the `type` field.
  + Specify the action to take when the topic is detected in prompts using `inputAction` or responses using `outputAction`. Choose `BLOCK` to block content and replace with blocked messaging, or `NONE` to take no action but return detection information. For more information, see [Options for handling harmful content detected by Amazon Bedrock Guardrails](guardrails-harmful-content-handling-options.md).
  + Set `inputEnabled` and `outputEnabled` to control whether guardrail evaluation is enabled for model prompts and responses.
  + (Optional) In the `examples` list, specify up to five sample phrases that you are representative of prompts or responses related to this topic.
+ (Optional) Specify a safeguard tier for your guardrail in the `tierConfig` object. Options include `STANDARD` and `CLASSIC` tiers. 

  For more information, see [Safeguard tiers for guardrails policies](guardrails-tiers.md).
+ (Optional) To enable [cross-Region inference](guardrails-cross-region.md), specify a guardrail profile in the `crossRegionConfig` object. This is required when using the `STANDARD` tier.
+ Specify a `name` and `description` for the guardrail.

The response format looks like this:

```
HTTP/1.1 202
Content-type: application/json

{
   "createdAt": "string",
   "guardrailArn": "string",
   "guardrailId": "string",
   "version": "string"
}
```

------