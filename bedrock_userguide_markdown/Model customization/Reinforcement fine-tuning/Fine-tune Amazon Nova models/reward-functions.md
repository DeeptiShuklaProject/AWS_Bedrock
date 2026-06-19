

# Setting up reward functions for Amazon Nova models
<a name="reward-functions"></a>

Reward functions evaluate response quality and provide feedback signals for model training. You can set up reward functions using custom Lambda functions or Amazon Bedrock-hosted foundation models as judges. Guided templates are available to simplify reward function creation for common tasks like instruction following and format validation. Choose the approach that matches your task requirements.

## Reinforcement Learning via Verifiable Rewards (RLVR)
<a name="rft-rlvr"></a>

RLVR optimizes models for objective tasks such as code generation or math reasoning using verifiable rule-based graders or ready-to-use templates.

You have two options for RLVR (Custom Code):

### Option 1: Use console-provided templates
<a name="w2aac17c25c17c17b5b7b1"></a>

Amazon Bedrock console provides sample templates for grader Lambda functions:
+ Mathematical reasoning with ground truth verification
+ Format validation and constraint checking
+ Generic grader Lambda template with boilerplate code

Follow the instructions in the provided template on the **Create RFT job** page in the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock).

### Option 2: Bring your own Lambda function
<a name="w2aac17c25c17c17b5b7b3"></a>

Create custom reward functions using your own Lambda ARN for complex logic, external APIs, multi-step calculations, or combining multiple evaluation criteria.

**Note**  
If you bring your own Lambda function, keep the following in mind:  
Increase the Lambda timeout from default 3 seconds to maximum 15 minutes for complex evaluations.
The Lambda execution role needs permissions to invoke models as described in [Access and security for Amazon Nova models](rft-access-security.md).

## Reinforcement Learning via AI Feedback (RLAIF)
<a name="rft-rlaif"></a>

RLAIF optimizes models for subjective tasks such as instruction following or chatbot interactions using AI-based judges with ready-to-use templates.

**For RLAIF (Model as Judge):**
+ Select an Amazon Bedrock hosted base Model as Judge
+ Configure instructions for evaluation
+ Define evaluation criteria and scoring guidelines

Available LLM-as-Judge prompt templates in the Amazon Bedrock console:
+ Instruction following (Judge model training)
+ Summarization (Multi-turn dialogs)
+ Reasoning evaluation (CoT for specialized domains)
+ RAG faithfulness (Context-grounded Q&A)

**Note**  
The console's **Model as Judge** option automatically converts your configuration into a Lambda function during training.

## Lambda function implementation details
<a name="rft-lambda-implementation"></a>

When implementing custom Lambda reward functions, your function must accept and return data in the following format.

------
#### [ Input structure ]

```
[{
  "id": "123",
  "messages": [
    {
      "role": "user",
      "content": "Do you have a dedicated security team?"
    },
    {
      "role": "assistant",
      "content": "As an AI developed by Amazon, I don not have a dedicated security team..."
    }
  ],
  "metadata": {
    "reference_answer": {
      "compliant": "No",
      "explanation": "As an AI developed by Company, I do not have a traditional security team..."
    },
    "my_key": "sample-001"
  }
}]
```

------
#### [ Output structure ]

```
[{
  "id": "123",
  "aggregate_reward_score": 0.85,
  "metrics_list": [
    {
      "name": "accuracy",
      "value": 0.9,
      "type": "Reward"
    },
    {
      "name": "policy_compliance",
      "value": 0.8,
      "type": "Metric"
    }
  ]
}]
```

------

**Design guidelines**
+ **Rank responses** – Give the best answer a clearly higher score
+ **Use consistent checks** – Evaluate task completion, format adherence, safety, and reasonable length
+ **Maintain stable scaling** – Keep scores normalized and non-exploitable