

# Subscribe to a model
<a name="bedrock-marketplace-subscribe-to-a-model"></a>

To use a model from Amazon Bedrock Marketplace, you subscribe to the model. If you're using a publicly available model, such as a HuggingFace model, you don't need a subscription. Models can be publicly available or proprietary. When you subscribe to a model, you review and accept the prices and EULAs of the model provider.

**Note**  
Subscription is not required before first invocation due to auto-enablement, Amazon Bedrock automatically initiates the subscription process in the background. API calls may succeed temporarily while the subscription is being finalized. However, if subscription fails, subsequent requests will fail, see [Request access to models](model-access.md).

**To subscribe to a model**

1. Sign in to the AWS Management Console using an IAM role with Amazon Bedrock permissions.

1. In the search bar, specify "Amazon Bedrock" and choose the **Amazon Bedrock** from the dropdown list.

1. From the navigation pane, choose Model Catalog.

1. Specify **Model Collection** = **Bedrock Marketplace** to load Amazon Bedrock Marketplace models.

   1. Alternatively, you can search for the model name directly in the search bar.

1. Choose the model card to open the **Model Detail** page.

1. Choose **View Subscription Options** to open the subscription modal.

1. Review the offers and the cost.

1. Review the legal terms and conditions.

1. Choose **Subscribe**.

The subscription process is usually complete within 10-15 minutes but can vary based on the requirements of the provider.

The costs are for the software costs only. You will be billed a separate SageMaker AI infrastructure cost for the instance type and number of instances that you select.