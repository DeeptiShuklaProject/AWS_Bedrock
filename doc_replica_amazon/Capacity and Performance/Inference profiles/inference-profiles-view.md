

# View information about an inference profile
<a name="inference-profiles-view"></a>

You can view information about cross Region inference profiles or application inference profiles that you've created. To learn how to view information about an inference profile, choose the tab for your preferred method, and then follow the steps:

------
#### [ Console ]

**To view information about a cross Region (system-defined) inference profile**

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. Select **Cross-Region inference** from the left navigation pane. Then, in the **Cross-Region inference** section, choose an inference profile.

1. View the details of the inference profile in the **Inference profile details** section and the Regions that it encompasses in the **Models** section.

**Note**  
You can't view application inference profiles in the Amazon Bedrock console.

------
#### [ API ]

To get information about an inference profile, send a [GetInferenceProfile](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetInferenceProfile.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp) and specify the Amazon Resource Name (ARN) or ID of the inference profile in the `inferenceProfileIdentifier` field.

To list information about the inference profiles that you can use, send a [ListInferenceProfiles](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListInferenceProfiles.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). You can specify the following optional parameters:


****  

| Field | Short description | 
| --- | --- | 
| maxResults | The maximum number of results to return in a response. | 
| nextToken | If there are more results than the number you specified in the maxResults field, the response returns a nextToken value. To see the next batch of results, send the nextToken value in another request. | 

------