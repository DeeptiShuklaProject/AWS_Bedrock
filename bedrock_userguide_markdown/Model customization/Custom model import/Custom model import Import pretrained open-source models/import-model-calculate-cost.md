

# Calculate the cost of running a custom model
<a name="import-model-calculate-cost"></a>

You are charged for running inference with custom models that you import into Amazon Bedrock. Use the following information to estimate the cost of running a custom model.

A Custom Model Unit (CMU) is an abstract view of the hardware use that Amazon Bedrock needs to host a a single copy of your custom model. A model copy represents a single instance of your imported model that is ready to serve inference requests. Amazon Bedrock determines the number of custom model units that a model copy needs when you import the custom model. As inference demand changes, Amazon Bedrock can increase or decrease the number of running model copies that are running. 

You can use CMUs to estimate the cost of running your custom model by using the following formula.

*Total cost = Number of running model copies × Number of CMUs per copy × billing rate per CMU per min × ((Number of 5-min windows)/60)*
+ *Number of running model copies *– Get from the `ModelCopy` metric in Amazon CloudWatch.
+ *Number of CMUs per copy * – Get the value from the model details page in the Amazon Bedrock details page. Alternatively, call the [GetImportedModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetImportedModel.html) operation and get the number of CMUs per copy from the `customModelUnitsPerModelCopy` field.
+ *Billing rate per CMU per min* – Get the custom model units version from the model details page in the Amazon Bedrock console. Alternatively, call the [GetImportedModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetImportedModel.html) operation and get the custom model units version from the `customModelUnitsVersion` field.

  Then, get the billing rate (**Price per Custom Model Unit per min\***) for the model version (**Custom Model Unit version**) on the **Custom Model Import** section of the [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) page.

Billing is charged over 5-minute billing windows from the first successful inference call. 

For more information, see [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).