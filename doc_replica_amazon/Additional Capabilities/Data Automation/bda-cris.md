

# Cross Region support required for Bedrock Data Automation
<a name="bda-cris"></a>

BDA requires users to use cross Region inference support when processing files. With cross-Region inference, Amazon Bedrock Data Automation will automatically select the optimal Region within your geography (as shown in the table below) to process your inference request, maximizing available compute resources and model availability, and providing the best customer experience. There's no additional cost for using cross-Region inference. Cross-Region inference requests are kept within the AWS Regions that are part of the geography where the data originally resides. For example, a request made within the US is kept within the AWS Regions in the US. Although the data remains stored only in the source Region, when using cross-Region inference, your requests and output results may move outside of your primary Region. All data will be encrypted while transmitted across Amazon's secure network. 

The following table includes the ARNs for different inference profiles. Replace account id with the account id you're using.


| Source Region | Amazon Resource Name (ARN) | Supported Regions | 
| --- | --- | --- | 
| US East (N. Virginia) | arn:aws:bedrock:us-east-1:{{account id}}:data-automation-profile/us.data-automation-v1 | us-east-1<br />us-east-2<br />us-west-1<br />us-west-2 | 
| US West (Oregon) | arn:aws:bedrock:us-west-2:{{account id}}:data-automation-profile/us.data-automation-v1 | us-east-1<br />us-east-2<br />us-west-1<br />us-west-2 | 
| Europe (Frankfurt) | arn:aws:bedrock:eu-central-1:{{account id}}:data-automation-profile/eu.data-automation-v1 | eu-central-1<br />eu-north-1<br />eu-south-1<br />eu-south-2<br />eu-west-1<br />eu-west-3 | 
| Europe (Ireland) | arn:aws:bedrock:eu-west-1:{{account id}}:data-automation-profile/eu.data-automation-v1 | eu-central-1<br />eu-north-1<br />eu-south-1<br />eu-south-2<br />eu-west-1<br />eu-west-3 | 
| Europe (London) | arn:aws:bedrock:eu-west-2:{{account id}}:data-automation-profile/eu.data-automation-v1 | eu-west-2 | 
| Asia Pacific (Mumbai) | arn:aws:bedrock:ap-south-1:{{account id}}:data-automation-profile/apac.data-automation-v1 | ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3<br />ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-4 | 
| Asia Pacific (Sydney) | arn:aws:bedrock:ap-southeast-2:{{account id}}:data-automation-profile/apac.data-automation-v1 | ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3<br />ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-4 | 
| AWS GovCloud (US-West) | arn:aws:bedrock:gov-cloud:{{account id}}:data-automation-profile/us-gov.data-automation-v1 | us-gov-west-1 | 

Below is an example IAM policy for processing documents with CRIS enabled for `us-east-1` or `us-west-2`.

```
{"Effect": "Allow",
 "Action": ["bedrock:InvokeDataAutomationAsync"],
 "Resource": [
  "arn:aws:bedrock:us-east-1:{{account_id}}:data-automation-profile/us.data-automation-v1",
  "arn:aws:bedrock:us-east-2:{{account_id}}:data-automation-profile/us.data-automation-v1",
  "arn:aws:bedrock:us-west-1:{{account_id}}:data-automation-profile/us.data-automation-v1",
  "arn:aws:bedrock:us-west-2:{{account_id}}:data-automation-profile/us.data-automation-v1"]}
```