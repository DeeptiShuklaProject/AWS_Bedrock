

# Delete an application inference profile
<a name="inference-profiles-delete"></a>

If you no longer need an application inference profile, you can delete it. You can only delete inference profiles through the Amazon Bedrock API.

To delete an inference profile, send a [DeleteInferenceProfile](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_DeleteInferenceProfiles.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and specify the Amazon Resource Name (ARN) or ID of the inference profile to delete in the `inferenceProflieIdentifier` field.