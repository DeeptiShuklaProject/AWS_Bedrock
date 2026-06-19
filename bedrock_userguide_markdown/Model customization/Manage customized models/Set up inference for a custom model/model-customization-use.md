

# Set up inference for a custom model
<a name="model-customization-use"></a>

After you create a custom model, you can set up inference using one of the following options:
+ **Purchase Provisioned Throughput** – Purchase Provisioned Throughput for your model to set up dedicated compute capacity with guaranteed throughput for consistent performance and lower latency. 

  For more information about Provisioned Throughput, see [Increase model invocation capacity with Provisioned Throughput in Amazon Bedrock](prov-throughput.md). For more information about using custom models with Provisioned Throughput, see [Purchase Provisioned Throughput for a custom model](custom-model-use-pt.md).
+ **Deploy custom model for on-demand inference** – To set up on-demand inference, you deploy the model with a custom model deployment. After you deploy the model, you invoke it using the ARN for the custom model deployment. With on-demand inference, you only pay for what you use and you don't need to set up provisioned compute resources.

  For more information about deploying custom models for on-demand inference, see [Deploy a custom model for on-demand inference](deploy-custom-model-on-demand.md).

**Topics**
+ [Purchase Provisioned Throughput for a custom model](custom-model-use-pt.md)
+ [Deploy a custom model for on-demand inference](deploy-custom-model-on-demand.md)