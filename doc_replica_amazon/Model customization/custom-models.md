

# Customize your model to improve its performance for your use case
<a name="custom-models"></a>

Model customization is the process of providing training data to a model to improve its performance for specific use-cases. You can customize Amazon Bedrock foundation models to improve their performance and create a better customer experience. Amazon Bedrock currently provides the following customization methods.
+ **Supervised fine-tuning**

  Provide *labeled* data to train a model to improve performance on specific tasks. By providing a training dataset of labeled examples, the model learns to associate what types of outputs should be generated for certain types of inputs. The model parameters are adjusted in the process and the model's performance is improved for the tasks represented by the training dataset.

  For more information about using supervised fine-tuning, see [Customize a model with fine-tuning in Amazon Bedrock](custom-model-fine-tuning.md).
+ **Reinforcement fine-tuning**

  Reinforcement fine-tuning improves foundation model alignment with your specific use case through feedback-based learning. Instead of providing labeled input-output pairs, you define reward functions that evaluate response quality. The model learns iteratively by receiving feedback scores from these reward functions.

  You can upload your training prompt datasets or provide existing Bedrock invocation logs. You can define reward functions using AWS Lambda to evaluate response quality. Amazon Bedrock automates the training workflow and provides real-time metrics to monitor model learning progress.

  For more information about using reinforcement fine-tuning, see [Customize a model with reinforcement fine-tuning in Amazon Bedrock](reinforcement-fine-tuning.md).
+ **Distillation**

  Use distillation to transfer knowledge from a larger more intelligent model (known as teacher) to a smaller, faster, and cost-efficient model (known as student). Amazon Bedrock automates the distillation process by using the latest data synthesis techniques to generate diverse, high-quality responses from the teacher model, and fine-tunes the student model. 

  To use distillation, you select a teacher model whose accuracy you want to achieve for your use case, and a student model to fine-tune. Then, you provide use case-specific prompts as input data. Amazon Bedrock generates responses from the teacher model for the given prompts, and then uses the responses to fine-tune the student model. You can optionally provide labeled input data as prompt-response pairs. 

  For more information about using distillation see [Customize a model with distillation in Amazon Bedrock](model-distillation.md).

For information about model customization quotas, see [Amazon Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) in the AWS General Reference.

**Note**  
You are charged for model training based on the number of tokens processed by the model (number of tokens in training data corpus × number of epochs) and model storage charged per month per model. For more information, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).