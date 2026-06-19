

# Service quotas for managed knowledge bases
<a name="kb-managed-quotas"></a>

Your AWS account has default quotas, formerly referred to as limits, for managed Amazon Bedrock knowledge bases. To view service quotas for Amazon Bedrock, do one of the following:
+ Follow the steps at [Viewing service quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html) and select **Amazon Bedrock** as the service.
+ Refer to [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) in the AWS General Reference.

The following quotas apply specifically to managed knowledge bases:


**Managed knowledge base quotas**  

| Quota | Default value | 
| --- | --- | 
| Maximum managed knowledge bases per account, per Region | 1,000 | 
| Maximum data sources per knowledge base | 200 | 
| Maximum concurrent ingestion jobs per knowledge base | 50 | 
| Maximum raw data storage per knowledge base | 10 TB | 
| Maximum query input characters per Retrieve or AgenticRetrieveStream request (English text) | 10,000 | 
| Maximum Retrieve or AgenticRetrieveStream requests per minute | 300 | 

To request adjustable quota increases, follow the steps at [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html), or contact your AWS account team.