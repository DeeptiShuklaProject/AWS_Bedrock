

# Custom model hyperparameters
<a name="custom-models-hp"></a>

The following reference content covers the hyperparameters that are available for training each Amazon Bedrock custom model.

A hyperparameter is a parameter that controls the training process, such as the learning rate or epoch count. You set hyperparameters for custom model training when you [submit](model-customization-submit.md) the fine tuning job with the Amazon Bedrock console or by calling the [CreateModelCustomizationJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateModelCustomizationJob.html) API operation.

## Amazon Nova Understanding model customization hyperparameters
<a name="cm-hp-nova-mm"></a>

The Amazon Nova Lite, Amazon Nova Micro, and Amazon Nova Pro models support the following three hyperparameters for model customization. For more information, see [Customize your model to improve its performance for your use case](custom-models.md).

 For information about fine tuning Amazon Nova models, see [Fine-tuning Amazon Nova models](https://docs.aws.amazon.com/nova/latest/userguide/customize-fine-tune.html).

The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Type | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | integer | 1 | 5 | 2 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | float | 1.00E-6 | 1.00E-4 | 1.00E-5 | 
| Learning rate warmup steps | learningRateWarmupSteps | The number of iterations over which the learning rate is gradually increased to the specified rate | integer | 0 | 100 | 10 | 

The default epoch number is 2, which works for most cases. In general, larger data sets require fewer epochs to converge, while smaller data sets require more epochs to converge. A faster convergence might also be achieved by increasing the learning rate, but this is less desirable because it might lead to training instability at convergence. We recommend starting with the default hyperparameters, which are based on our assessment across tasks of different complexity and data sizes.

The learning rate will gradually increase to the set value during warm up. Therefore, we recommend that you avoid a large warm up value when the training sample is small because the learning rate might never reach the set value during the training process. We recommend setting the warmup steps by dividing the dataset size by 640 for Amazon Nova Micro, 160 for Amazon Nova Lite, and 320 for Amazon Nova Pro.

## Amazon Nova Canvas model customization hyperparameters
<a name="cm-hp-nova-canvas"></a>

The Amazon Nova Canvas model supports the following hyperparameters for model customization.


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | 
| Batch size | batchSize | Number of samples processed before updating model parameters | 8 | 192 | 8 | 
| Steps | stepCount | Number of times the model is exposed to each batch | 10 | 20,000 | 500 | 
| Learning rate | learningRate | Rate at which model parameters are updated after each batch | 1.00E-7 | 1.00E-4 | 1.00E-5 | 

## Amazon Titan text model customization hyperparameters
<a name="cm-hp-titan-text"></a>

Amazon Titan Text Premier model supports the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Type | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | integer | 1 | 5 | 2 | 
| Batch size (micro) | batchSize | The number of samples processed before updating model parameters | integer | 1 | 1 | 1 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | float | 1.00E-07 | 1.00E-05 | 1.00E-06 | 
| Learning rate warmup steps | learningRateWarmupSteps | The number of iterations over which the learning rate is gradually increased to the specified rate | integer | 0 | 20 | 5 | 

Amazon Titan Text models, such as Lite and Express, support the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Type | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | integer | 1 | 10 | 5 | 
| Batch size (micro) | batchSize | The number of samples processed before updating model parameters | integer | 1 | 64 | 1 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | float | 0.0 | 1 | 1.00E-5 | 
| Learning rate warmup steps | learningRateWarmupSteps | The number of iterations over which the learning rate is gradually increased to the specified rate | integer | 0 | 250 | 5 | 

## Amazon Titan Image Generator G1 models customization hyperparameters
<a name="cm-hp-titan-image"></a>

The Amazon Titan Image Generator G1 model supports the following hyperparameters for model customization.

**Note**  
`stepCount` has no default value and must be specified. `stepCount` supports the value `auto`. `auto` prioritizes model performance over training cost by automatically determining a number based on the size of your dataset. Training job costs depend on the number that `auto` determines. To understand how job cost is calculated and to see examples, see [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | 
| Batch size | batchSize | Number of samples processed before updating model parameters | 8 | 192 | 8 | 
| Steps | stepCount | Number of times the model is exposed to each batch | 10 | 40,000 | N/A | 
| Learning rate | learningRate | Rate at which model parameters are updated after each batch | 1.00E-7 | 1 | 1.00E-5 | 

## Amazon Titan Multimodal Embeddings G1 customization hyperparameters
<a name="cm-hp-titan-mm"></a>

The Amazon Titan Multimodal Embeddings G1 model supports the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).

**Note**  
`epochCount` has no default value and must be specified. `epochCount` supports the value `Auto`. `Auto` prioritizes model performance over training cost by automatically determining a number based on the size of your dataset. Training job costs depend on the number that `Auto` determines. To understand how job cost is calculated and to see examples, see [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Type | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | integer | 1 | 100 | N/A | 
| Batch size | batchSize | The number of samples processed before updating model parameters | integer | 256 | 9,216 | 576 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | float | 5.00E-8 | 1 | 5.00E-5 | 

## Anthropic Claude 3 model customization hyperparameters
<a name="cm-hp-anth-claude-3"></a>

Anthropic Claude 3 models support the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing).


****  

| Console Name | API Name | Definition | Default | Minimum | Maximum | 
| --- | --- | --- | --- | --- | --- | 
| Epoch count | epochCount | The maximum number of iterations through the entire training dataset | 2 | 1 | 10 | 
| Batch size  | batchSize | Number of samples processed before updating model parameters | 32 | 4 | 256 | 
| Learning rate multiplier | learningRateMultiplier | Multiplier that influences the learning rate at which model parameters are updated after each batch | 1 | 0.1 | 2 | 
| Early stopping threshold | earlyStoppingThreshold | Minimum improvement in validation loss required to prevent premature termination of the training process | 0.001 | 0 | 0.1 | 
| Early stopping patience | earlyStoppingPatience | Tolerance for stagnation in the validation loss metric before stopping the training process | 2 | 1 | 10 | 

## Cohere Command model customization hyperparameters
<a name="cm-hp-cohere-command"></a>

The Cohere Command and Cohere Command Light models support the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing). For more information, see [Customize your model to improve its performance for your use case](custom-models.md).

 For information about fine tuning Cohere models, see the Cohere documentation at [https://docs.cohere.com/docs/fine-tuning](https://docs.cohere.com/docs/fine-tuning).

**Note**  
The `epochCount` quota is adjustable.


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Type | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | integer | 1 | 100 | 1 | 
| Batch size | batchSize | The number of samples processed before updating model parameters | integer | 8 | 8 (Command)32 (Light) | 8 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch. If you use a validation dataset, we recommend that you don't provide a value for learningRate. | float | 5.00E-6 | 0.1 | 1.00E-5 | 
| Early stopping threshold | earlyStoppingThreshold | The minimum improvement in loss required to prevent premature termination of the training process | float | 0 | 0.1 | 0.01 | 
| Early stopping patience | earlyStoppingPatience | The tolerance for stagnation in the loss metric before stopping the training process | integer | 1 | 10 | 6 | 
| Evaluation percentage | evalPercentage | The percentage of the dataset allocated for model evaluation, if you don't provide a separate validation dataset | float | 5 | 50 | 20 | 

## Meta Llama 3.1 model customization hyperparameters
<a name="cm-hp-meta-llama31"></a>

The Meta Llama 3.1 8B and 70B models support the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing). For more information, see [Customize your model to improve its performance for your use case](custom-models.md).

 For information about fine tuning Meta Llama models, see the Meta documentation at [https://ai.meta.com/llama/get-started/\#fine-tuning](https://ai.meta.com/llama/get-started/#fine-tuning).

**Note**  
The `epochCount` quota is adjustable.


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | 1 | 10 | 5 | 
| Batch size | batchSize | The number of samples processed before updating model parameters | 1 | 1 | 1 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | 5.00E-6 | 0.1 | 1.00E-4 | 

## Meta Llama 3.2 model customization hyperparameters
<a name="cm-hp-meta-llama32"></a>

The Meta Llama 3.2 1B, 3B, 11B, and 90B models support the following hyperparameters for model customization. The number of epochs you specify increases your model customization cost by processing more tokens. Each epoch processes the entire training dataset once. For information about pricing, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing). For more information, see [Customize your model to improve its performance for your use case](custom-models.md).

 For information about fine tuning Meta Llama models, see the Meta documentation at [https://ai.meta.com/llama/get-started/\#fine-tuning](https://ai.meta.com/llama/get-started/#fine-tuning).


****  

| Hyperparameter (console) | Hyperparameter (API) | Definition | Minimum | Maximum | Default | 
| --- | --- | --- | --- | --- | --- | 
| Epochs | epochCount | The number of iterations through the entire training dataset | 1 | 10 | 5 | 
| Batch size | batchSize | The number of samples processed before updating model parameters | 1 | 1 | 1 | 
| Learning rate | learningRate | The rate at which model parameters are updated after each batch | 5.00E-6 | 0.1 | 1.00E-4 | 