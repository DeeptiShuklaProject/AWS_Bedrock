

# Prompt injection security
<a name="prompt-injection"></a>

 As per the [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/), AWS is responsible for securing the underlying cloud infrastructure, including the hardware, software, networking, and facilities that run AWS services. However, customers are responsible for securing their applications, data, and resources deployed on AWS. 

In the context of Amazon Bedrock, AWS handles the security of the underlying infrastructure, including the physical data centers, networking, and the Amazon Bedrock service itself. However, the responsibility for secure application development and preventing vulnerabilities like prompt injection lies with the customer. 

Prompt injection is an application-level security concern, similar to SQL injection in database applications. Just as AWS services like Amazon RDS and Amazon Aurora provide secure database engines, but customers are responsible for preventing SQL injection in their applications. Amazon Bedrock provides a secure foundation for natural language processing, but customers must take measures to prevent prompt injection vulnerabilities in their code. Additionally, AWS provides detailed documentation, best practices, and guidance on secure coding practices for Bedrock and other AWS services. 

To protect against prompt injection and other security vulnerabilities when using Amazon Bedrock, customers should follow these best practices: 
+ **Input Validation** – Validate and sanitize all user input before passing it to the Amazon Bedrock API or tokenizer. This includes removing or escaping special characters and ensuring that input adheres to expected formats. 
+ **Secure Coding Practices** – Follow secure coding practices, such as using parameterized queries, avoiding string concatenation for input, and practicing the principle of least privilege when granting access to resources. 
+ **Security Testing** – Regularly test your applications for prompt injection and other security vulnerabilities using techniques like penetration testing, static code analysis, and dynamic application security testing (DAST). 
+ **Stay Updated** – Keep your Amazon Bedrock SDK, libraries, and dependencies up-to-date with the latest security patches and updates. Monitor AWS security bulletins and announcements for any relevant updates or guidance. AWS provides detailed documentation, blog posts, and sample code to help customers build secure applications using Bedrock and other AWS services. Customers should review these resources and follow the recommended security best practices to protect their applications from prompt injection and other vulnerabilities. 

You can use an Amazon Bedrock Guardrail to help protect against prompt injection attacks. For more information, see [Detect prompt attacks with Amazon Bedrock Guardrails](guardrails-prompt-attack.md).

When creating an Amazon Bedrock agent, use the following techniques to help protect against prompt injection attacks. 
+ Associate a guardrail with the agent. For more information, see [Implement safeguards for your application by associating a guardrail with your agent](agents-guardrail.md).
+ Use [advanced prompts](https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html) to enable the default pre-processing prompt. Every agent has a default pre-processing prompt that you can enable. This is a lightweight prompt that uses a foundation model to determine if user input is safe to be processed. You can use its default behavior or fully customize the prompt to include any other classification categories. Optionally, you can author your own foundation model response parser in an [AWS Lambda](https://docs.aws.amazon.com/bedrock/latest/userguide/lambda-parser.html) function to implement your own custom rules. 

  For more information, see [How Amazon Bedrock Agents works](agents-how.md).
+ Update the system prompt by using advanced prompt features. Newer models differentiate between system and user prompts. If you use system prompts in an agent, we recommend that you clearly define the scope of what the agent can and cannot do. Also, check the model provider's own documentation for model specific guidance. To find out which serverless models in Amazon Bedrock support system prompts, see [Inference request parameters and response fields for foundation models](model-parameters.md). 