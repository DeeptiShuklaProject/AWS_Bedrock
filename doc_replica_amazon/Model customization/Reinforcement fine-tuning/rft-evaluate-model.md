

# Evaluate your RFT model
<a name="rft-evaluate-model"></a>

After your reinforcement fine-tuning job completes successfully, you can evaluate your custom model's performance using multiple assessment methods. Amazon Bedrock provides built-in evaluation tools to help you compare your RFT model against the base model and validate improvements.

**Topics**
+ [Evaluation methods](#rft-evaluation-methods)
+ [Setting up inference for evaluation](#rft-setup-inference-evaluation)
+ [Evaluation best practices](#rft-evaluation-best-practices)

## Evaluation methods
<a name="rft-evaluation-methods"></a>

Amazon Bedrock offers several ways to assess your RFT model performance.

### Validation metrics
<a name="rft-validation-metrics"></a>

If you upload a validation dataset, you will see two additional graphs in training metrics.
+ **Validation rewards** - Shows how well your model generalizes beyond training examples. Lower scores than training rewards are normal and expected.
+ **Validation episode lengths** - Average response length on unseen validation data. Shows how efficiently your model responds to new inputs compared to the training examples.

### Test in Playground
<a name="rft-test-playground"></a>

Use the Test in Playground feature for quick, ad-hoc evaluations. To use the Test in Playground feature, inference needs to be set up. For more information, see [Setting up inference for evaluation](#rft-setup-inference-evaluation).

This interactive tool allows you to:
+ Test prompts directly with your RFT model
+ Compare responses side-by-side between your custom model and the base model
+ Evaluate response quality improvements in real-time
+ Experiment with different prompts to assess model capabilities

### Bedrock Model Evaluation
<a name="rft-model-evaluation"></a>

Use Amazon Bedrock's Model Evaluation to assess your RFT model using your own datasets. This provides comprehensive performance analysis with standardized metrics and benchmarks. Here are some examples of the Amazon Bedrock Model Evaluation benefits.
+ Systematic evaluation using custom test datasets
+ Quantitative performance comparisons
+ Standardized metrics for consistent assessment
+ Integration with existing Amazon Bedrock evaluation workflows

## Setting up inference for evaluation
<a name="rft-setup-inference-evaluation"></a>

Before evaluating your RFT model, set up inference using one of these options:

### On-demand inference
<a name="rft-on-demand-inference"></a>

Create a custom model on-demand deployment for flexible, pay-per-use evaluation. This option includes token-based pricing that charges based on the number of tokens processed during inference.

## Evaluation best practices
<a name="rft-evaluation-best-practices"></a>
+ **Compare systematically** - Always evaluate your RFT model against the base model using the same test prompts and evaluation criteria.
+ **Use diverse test cases** - Include various prompt types and scenarios that represent your real-world use cases.
+ **Validate reward alignment** - Ensure your model improvements align with the reward functions used during training.
+ **Test edge cases** - Evaluate model behavior on challenging or unusual inputs to assess robustness.
+ **Monitor response consistency** - Check that your model provides consistent quality across multiple runs with similar prompts.