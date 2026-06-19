

# Tagging Amazon Bedrock resources
<a name="tagging"></a>

To help you manage your Amazon Bedrock resources, you can assign metadata to each resource as tags. A tag is a label that you assign to an AWS resource. Each tag consists of a key and a value.

Tags enable you to categorize your AWS resources in different ways, for example, by purpose, owner, or application. For best practices and restrictions on tagging, see [Tagging your AWS resources](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html).

Tags help you to do the following:
+ Identify and organize your AWS resources. Many AWS resources support tagging, so you can assign the same tag to resources in different services to indicate that the resources are the same.
+ Allocate costs. You activate tags on the AWS Billing and Cost Management dashboard. AWS uses the tags to categorize your costs and deliver a monthly cost allocation report to you. For more information, see [Use cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) in the *AWS Billing and Cost Management User Guide*.
+ Control access to your resources. You can use tags with Amazon Bedrock to create policies to control access to Amazon Bedrock resources. These policies can be attached to an IAM role or user to enable tag-based access control.

**Topics**
+ [Tag resources on the `bedrock-runtime` endpoint](#tagging-runtime)
+ [Tag resources on the `bedrock-mantle` endpoint](#tagging-mantle)

## Tag resources on the `bedrock-runtime` endpoint
<a name="tagging-runtime"></a>

Resources created through the `bedrock-runtime` control plane (such as agents, knowledge bases, custom models, provisioned throughput, and flows) are tagged using dedicated tagging API operations.

### Use the console
<a name="tagging-console"></a>

You can add, modify, and remove tags at any time while creating or editing a supported resource.

### Use the API
<a name="tagging-api"></a>

To carry out tagging operations, you need the Amazon Resource Name (ARN) of the resource on which you want to carry out a tagging operation. There are two sets of tagging operations, depending on the resource for which you are adding or managing tags.

The following table summarizes the different use cases and the tagging operations to use for them:


****  

| Use case | Resource created with [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock.html) API operation | Resource created with [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) API operation | Resource created with Amazon Bedrock Data Automation API | 
| --- | --- | --- | --- | 
| Tag a resource |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/tagging.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/tagging.html)  |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/tagging.html)  | 
| Untag a resource | Make an [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_UntagResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). | Make an [UntagResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UntagResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). | Make an UntagResource request with an Amazon Bedrock Data Automation Build time Endpoint. | 
| List tags for a resource | Make a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListTagsForResource.html) request with an [Amazon Bedrock control plane endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#br-cp). | Make a [ListTagsForResource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_ListTagsForResource.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt). | Make a ListTagsForResource request with an Amazon Bedrock Data Automation Build time Endpoint. | 

**Note**  
When viewing these operations in CloudTrail, you can identify the specific resource being tagged by checking the request parameters in the event details.

Choose a tab to see code examples in an interface or language.

------
#### [ AWS CLI ]

Add two tags to an agent. Separate key/value pairs with a space.

```
aws bedrock-agent tag-resource \
    --resource-arn "arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345" \
    --tags key=department,value=billing key=facing,value=internal
```

Remove the tags from the agent. Separate keys with a space.

```
aws bedrock-agent untag-resource \
    --resource-arn "arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345" \
    --tag-keys key=department facing
```

List the tags for the agent.

```
aws bedrock-agent list-tags-for-resource \
    --resource-arn "arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345"
```

------
#### [ Python (Boto) ]

Add two tags to an agent.

```
import boto3

bedrock = boto3.client(service_name='bedrock-agent')

tags = [
    {
        'key': 'department',
        'value': 'billing'
    },
    {
        'key': 'facing',
        'value': 'internal'
    }
]

bedrock.tag_resource(resourceArn='arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345', tags=tags)
```

Remove the tags from the agent.

```
bedrock.untag_resource(
    resourceArn='arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345', 
    tagKeys=['department', 'facing']
)
```

List the tags for the agent.

```
bedrock.list_tags_for_resource(resourceArn='arn:aws:bedrock:us-east-1:123456789012:agent/AGENT12345')
```

------

## Tag resources on the `bedrock-mantle` endpoint
<a name="tagging-mantle"></a>

The `bedrock-mantle` endpoint supports tagging projects, customized models, and reservations. Unlike the `bedrock-runtime` control plane, `bedrock-mantle` does not expose dedicated `TagResource`, `UntagResource`, or `ListTagsForResource` API operations. Instead, you set and read tags inline through the resource APIs.

### Setting tags
<a name="tagging-mantle-setting"></a>


****  

| Action | API call | Tag fields | 
| --- | --- | --- | 
| Create a project with tags | POST /v1/organization/projects | tags | 
| Add or remove tags on an existing project | POST /v1/organization/projects/{project\_id} | add\_tags, remove\_tag\_keys, tags | 
| Create a customized model with tags | Customized-model create endpoint | tags | 
| Update tags on a customized model | Customized-model update endpoint | add\_tags, remove\_tag\_keys | 
| Create a reservation with tags | Reservation create endpoint | tags | 
| Update tags on a reservation | Reservation update endpoint | add\_tags, remove\_tag\_keys | 

Tags are returned inline on Get and List responses for these resources.

### IAM actions
<a name="tagging-mantle-iam"></a>

Although there are no dedicated tagging endpoints, the following IAM actions are evaluated when you set, change, or read tags on `bedrock-mantle` resources. You can write IAM policies using these action names and the `aws:RequestTag`, `aws:TagKeys`, and `aws:ResourceTag` condition keys to control tag-based access.
+ `bedrock-mantle:TagResource`
+ `bedrock-mantle:UntagResource`
+ `bedrock-mantle:ListTagsForResource`

### Example
<a name="tagging-mantle-example"></a>

The following example creates a project with two tags using `curl`:

```
curl -X POST https://bedrock-mantle.us-east-1.api.aws/v1/organization/projects \
    -H "Authorization: Bearer $BEDROCK_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "billing-experiments",
      "tags": {
        "department": "billing",
        "facing": "internal"
      }
    }'
```

The following example adds one tag and removes another from an existing project:

```
curl -X POST https://bedrock-mantle.us-east-1.api.aws/v1/organization/projects/proj_abc123 \
    -H "Authorization: Bearer $BEDROCK_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "add_tags": { "owner": "alice" },
      "remove_tag_keys": ["facing"]
    }'
```