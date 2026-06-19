

# Supported Regions for cross-Region guardrail inference
<a name="guardrails-cross-region-support"></a>

Cross-Region inference with Amazon Bedrock Guardrails lets you seamlessly manage unplanned traffic bursts by using compute across different AWS Regions for your guardrail policy evaluations.

When [creating](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html) or [modifying](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-edit.html) a guardrail, you specify a guardrail profile that supports a set of source and destination Regions:
+ **Source Region** – A Region where you make the guardrail inference request.
+ **Destination Region** – A Region where the Amazon Bedrock service can route the guardrail inference request.

The guardrail profiles that you can use depend on the source Region where your guardrail resides.

## Available guardrail profiles
<a name="available-guardrail-profiles"></a>

Expand one of the following sections to see information about a guardrail profile, the source Regions from which it can be used, and the destination Regions to which it can route requests.

### US Guardrail v1:0
<a name="guardrail-profiles-us-guardrail"></a>

To use a guardrail profile in the US geographic boundary, specify the following guardrail profile ID or Amazon Resource Name (ARN) in one of the source Regions:

**Guardrail profile ID**  

```
us.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/us.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| us-east-1 | us-east-1<br />us-east-2<br />us-west-2 | 
| us-east-2 | us-east-1<br />us-east-2<br />us-west-2 | 
| us-west-1 | us-east-1<br />us-east-2<br />us-west-1<br />us-west-2 | 
| us-west-2 | us-east-1<br />us-east-2<br />us-west-2 | 

### US-GOV Guardrail v1:0
<a name="guardrail-profiles-us-gov-guardrail"></a>

To use a guardrail profile in the AWS GovCloud (US) geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
us-gov.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws-us-gov:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/us-gov.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| us-gov-east-1 | us-gov-east-1<br />us-gov-west-1 | 
| us-gov-west-1 | us-gov-east-1<br />us-gov-west-1 | 

### EU Guardrail v1:0
<a name="guardrail-profiles-eu-guardrail"></a>

To use a guardrail profile in the EU geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
eu.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/eu.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| eu-central-1 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| eu-west-1 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| eu-west-3 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| eu-north-1 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| eu-south-1 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| eu-south-2 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2 | 
| il-central-1 | eu-central-1<br />eu-west-1<br />eu-west-3<br />eu-north-1<br />eu-south-1<br />eu-south-2<br />il-central-1 | 

### UK Guardrail v1:0
<a name="guardrail-profiles-uk-guardrail"></a>

To use a guardrail profile in the UK geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
uk.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/uk.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| eu-west-2 | eu-west-2 | 

### AU Guardrail v1:0
<a name="guardrail-profiles-au-guardrail"></a>

To use a guardrail profile in the Australia geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
au.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/au.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| ap-southeast-2 | ap-southeast-2 | 

### CA Guardrail v1:0
<a name="guardrail-profiles-ca-guardrail"></a>

To use a guardrail profile in the Canada geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
ca.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/ca.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| ca-central-1 | ca-central-1<br />ca-west-1 | 

### APAC Guardrail v1:0
<a name="guardrail-profiles-apac-guardrail"></a>

To apply a guardrail cross-region in the APAC geographic boundary, specify the following guardrail profile ID or ARN in one of the source Regions:

**Guardrail profile ID**  

```
apac.guardrail.v1:0
```

**Guardrail profile ARN**  

```
arn:aws:bedrock:{{source-region}}:{{account-id}}:guardrail-profile/apac.guardrail.v1:0
```

The following table shows the source Regions from which you can call the guardrail profile and the destination Regions to which the requests can be routed:


| Source Region | Destination Regions | 
| --- | --- | 
| ap-south-1 | ap-south-1<br />ap-northeast-3<br />ap-northeast-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-northeast-1 | 
| ap-northeast-2 | ap-south-1<br />ap-northeast-3<br />ap-northeast-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-northeast-1 | 
| ap-southeast-1 | ap-south-1<br />ap-northeast-3<br />ap-northeast-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-northeast-1 | 
| ap-southeast-2 | ap-south-1<br />ap-northeast-3<br />ap-northeast-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-northeast-1 | 
| ap-southeast-3 | ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-3<br />ap-southeast-4<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3 | 
| ap-southeast-4 | ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-4<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3 | 
| ap-northeast-1 | ap-south-1<br />ap-northeast-3<br />ap-northeast-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-northeast-1 | 
| ap-east-2 | ap-east-2<br />ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-3<br />ap-southeast-4<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3 | 
| ap-southeast-5 | ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-3<br />ap-southeast-4<br />ap-southeast-5<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3 | 
| ap-southeast-7 | ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-3<br />ap-southeast-4<br />ap-southeast-7<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3 | 
| me-central-1 | ap-south-1<br />ap-south-2<br />ap-southeast-1<br />ap-southeast-2<br />ap-southeast-3<br />ap-southeast-4<br />ap-northeast-1<br />ap-northeast-2<br />ap-northeast-3<br />me-central-1 | 