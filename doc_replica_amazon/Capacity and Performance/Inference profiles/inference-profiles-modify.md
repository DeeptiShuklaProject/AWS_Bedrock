

# Modify the tags for an application inference profile
<a name="inference-profiles-modify"></a>

After you create an application inference profile, you can still manage tags through the Amazon Bedrock API by submitting a [TagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_TagResource.html) or [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UntagResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and specifying the ARN of the application inference profile in the `resourceArn` field. To learn more about tagging, see [Tagging Amazon Bedrock resources](tagging.md).