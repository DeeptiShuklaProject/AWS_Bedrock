

# Setting up reward functions for open-weight models
<a name="reward-functions-open-weight"></a>

Reward functions evaluate response quality and provide feedback signals for model training. You can set up reward functions using custom Lambda functions. Choose the approach that matches your task requirements.

## Custom Lambda functions for reward evaluation
<a name="rft-custom-lambda-functions"></a>

You can set up reward functions using custom Lambda functions. Within your Lambda function, you have flexibility in how you implement the evaluation logic:
+ **Objective tasks** – For objective tasks like code generation or math reasoning, use verifiable rule-based graders that check correctness against known standards or test cases.
+ **Subjective tasks** – For subjective tasks like instruction following or chatbot interactions, call Amazon Bedrock foundation models as judges within your Lambda function to evaluate response quality based on your criteria.

Your Lambda function can implement complex logic, integrate external APIs, perform multi-step calculations, or combine multiple evaluation criteria depending on your task requirements.

**Note**  
When using custom Lambda functions:  
Increase the Lambda timeout from default 3 seconds to maximum 15 minutes for complex evaluations.
The Lambda execution role needs permissions to invoke the Lambda function as described in [Lambda permissions for reward functions](rft-open-weight-access-security.md#openai-fine-tuning-lambda-permissions).

## Lambda function implementation details
<a name="rft-lambda-implementation-open-weight"></a>

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