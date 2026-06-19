

# Customize a model with reinforcement fine-tuning in Amazon Bedrock
<a name="reinforcement-fine-tuning"></a>

Reinforcement fine-tuning is a model customization technique in Amazon Bedrock that improves foundation model performance by teaching models what constitutes a "good" response through feedback signals called rewards. Unlike traditional fine-tuning methods that depend on labeled datasets, reinforcement fine-tuning uses a feedback-driven approach that iteratively optimizes the model to maximize these rewards.

## Reinforcement fine-tuning applications and scenarios
<a name="reinforcement-fine-tuning-when"></a>

Use reinforcement fine-tuning when you can define clear, measurable success criteria for evaluating response quality. Reinforcement fine-tuning excels in domains where output quality can be objectively measured, especially when multiple valid responses exist or when optimal responses are difficult to define upfront. It's ideal for:
+ Mathematical problem-solving and code generation (using rule-based graders for objective evaluation)
+ Scientific reasoning and structured data analysis
+ Subjective tasks like instruction following, content moderation, and creative writing (using AI-based judges)
+ Tasks requiring step-by-step reasoning or multi-turn problem solving
+ Scenarios with multiple valid solutions where some are clearly better than others
+ Applications balancing multiple objectives (accuracy, efficiency, style)
+ Applications requiring iterative improvement, personalization, or adherence to complex business rules
+ Scenarios where success can be verified programmatically through execution results or performance metrics
+ Cases where collecting high-quality labeled examples is expensive or impractical

## Benefits of reinforcement fine-tuning
<a name="reinforcement-fine-tuning-benefits"></a>
+ **Improved model performance** – Reinforcement fine-tuning improves model accuracy by up to 66% on average compared to base models. This enables optimization for price and performance by fine-tuning smaller, faster, and more efficient model variants.
+ **Ease of use** – Amazon Bedrock automates the complexity of reinforcement fine-tuning, making it accessible to developers building AI applications. You can fine-tune models using your uploaded datasets or existing API invocation logs. You can define reward functions that grade model outputs with custom code using Lambda or model-as-a-judge grader, with built-in templates that help with quick setup.
+ **Security and compliance** – Your proprietary data never leaves AWS's secure, governed environment during the customization process.

## Supported models for reinforcement fine-tuning
<a name="rft-supported-models"></a>

The following table shows the foundation models that you can customize with reinforcement fine-tuning:


**Supported models for reinforcement fine-tuning**  

| Provider | Model | Model ID | Region name | Region | 
| --- | --- | --- | --- | --- | 
| Amazon | Nova 2 Lite | amazon.nova-2-lite-v1:0:256k | US East (N. Virginia) | us-east-1 | 
| OpenAI | gpt-oss-20B | openai.gpt-oss-20b | US West (Oregon) | us-west-2 | 
| Qwen | Qwen3 32B | qwen.qwen3-32b | US West (Oregon) | us-west-2 | 

## How reinforcement fine-tuning works
<a name="rft-how-it-works"></a>

Amazon Bedrock fully automates the reinforcement fine-tuning workflow. The model receives prompts from your training dataset and generates several responses per prompt. These responses are then scored by a reward function. Amazon Bedrock uses the prompt-response pairs with scores to train the model through policy-based learning using Group Relative Policy Optimization (GRPO). The training loop continues until it reaches the end of your training data or you stop the job at a chosen checkpoint, producing a model optimized for the metric that matters to you.

## Reinforcement fine-tuning best practices
<a name="rft-best-practices"></a>
+ **Start small** – Begin with 100-200 examples, validate reward function correctness, and scale gradually based on results
+ **Pre fine-tuning evaluation** – Test baseline model performance before reinforcement fine-tuning. If rewards are consistently 0 percent, use supervised fine-tuning first to establish basic capabilities. If rewards are greater than 95 percent, reinforcement fine-tuning might be unnecessary
+ **Monitor training** – Track average reward scores and distribution. Watch for overfitting (training rewards increase while validation rewards decrease). Look for concerning patterns such as rewards plateauing below 0.15, increasing reward variance over time, and declining validation performance
+ **Optimize reward functions** – Execute within seconds (not minutes), minimize external API calls, use efficient algorithms, implement proper error handling, and take advantage of Lambda's parallel scaling
+ **Iteration strategy** – If rewards aren't improving, adjust reward function design, increase dataset diversity, add more representative examples, and verify reward signals are clear and consistent

**Topics**
+ [Reinforcement fine-tuning applications and scenarios](#reinforcement-fine-tuning-when)
+ [Benefits of reinforcement fine-tuning](#reinforcement-fine-tuning-benefits)
+ [Supported models for reinforcement fine-tuning](#rft-supported-models)
+ [How reinforcement fine-tuning works](#rft-how-it-works)
+ [Reinforcement fine-tuning best practices](#rft-best-practices)
+ [Fine-tune Amazon Nova models with reinforcement fine-tuning](rft-nova-models.md)
+ [Fine-tune open-weight models using OpenAI-compatible APIs](fine-tuning-openai-apis.md)
+ [Evaluate your RFT model](rft-evaluate-model.md)