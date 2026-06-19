

# Remove PII from conversations by using sensitive information filters
<a name="guardrails-sensitive-filters"></a>

 Amazon Bedrock Guardrails helps detect sensitive information, such as personally identifiable information (PII), in input prompts or model responses using sensitive information filters. This filter supports only text output and will not detect PII information when models respond with tool\_use (function call) output parameters via supported APIs. This filter is a probabilistic machine learning (ML) based solution that is context-dependent and detects sensitive information based on the context within input prompts or model responses. You can configure by selecting from a set of built-in PIIs offered by Amazon Bedrock Guardrails specific to your use case or organization by defining it along with regular expressions (custom regex) that work based on pattern matching to block or mask PII data. 

Sensitive information detection works across both natural language and code domains, including code syntax, comments, string literals, and hybrid content. This helps identify PII embedded in code elements such as variable names, hardcoded credentials, or code documentation.

You can configure the following modes for handling sensitive information that guardrails detects:
+ **Block** — Sensitive information filter policies can block requests or responses that include sensitive information. Examples of such applications might include general questions and answers based on public documents. If sensitive information is detected in the prompt or response, the guardrail blocks all the content and returns a message that you configure.
+ **Mask** — Sensitive information filter policies can anonymize or redact information from model requests or responses. For example, guardrails mask PIIs while generating summaries of conversations between users and customer service agents. If sensitive information is detected in the model request or response, the guardrail masks it and replaces it with the PII type (for example, `{NAME}` or `{EMAIL}`).

Amazon Bedrock Guardrails offers the following PIIs to block or anonymize:
+ **General**
  + **ADDRESS**

    A physical address, such as "100 Main Street, Anytown, USA" or "Suite \#12, Building 123". An address can include information such as the street, building, location, city, state, country, county, zip code, precinct, and neighborhood. 
  + **AGE**

    An individual's age, including the quantity and unit of time. For example, in the phrase "I am 40 years old," Amazon Bedrock Guardrails recognizes "40 years" as an age. 
  + **NAME**

    An individual's name. This entity type does not include titles, such as Dr., Mr., Mrs., or Miss. Amazon Bedrock Guardrails does not apply this entity type to names that are part of organizations or addresses. For example, guardrails recognizes the "John Doe Organization" as an organization, and it recognizes "Jane Doe Street" as an address. 
  + **EMAIL**

    An email address, such as *marymajor@email.com*.
  + **PHONE**

    A phone number. This entity type also includes fax and pager numbers. 
  + **USERNAME**

    A user name that identifies an account, such as a login name, screen name, nick name, or handle. 
  + **PASSWORD**

    An alphanumeric string that is used as a password, such as "\**very20special\#pass\**". 
  + **DRIVER\_ID**

    The number assigned to a driver's license, which is an official document permitting an individual to operate one or more motorized vehicles on a public road. A driver's license number consists of alphanumeric characters. 
  + **LICENSE\_PLATE**

    A license plate for a vehicle is issued by the state or country where the vehicle is registered. The format for passenger vehicles is typically five to eight digits, consisting of upper-case letters and numbers. The format varies depending on the location of the issuing state or country. 
  + **VEHICLE\_IDENTIFICATION\_NUMBER**

    A Vehicle Identification Number (VIN) uniquely identifies a vehicle. VIN content and format are defined in the *ISO 3779* specification. Each country has specific codes and formats for VINs. 
+ **Finance**
  + **CREDIT\_DEBIT\_CARD\_CVV**

    A three-digit card verification code (CVV) that is present on VISA, MasterCard, and Discover credit and debit cards. For American Express credit or debit cards, the CVV is a four-digit numeric code. 
  + **CREDIT\_DEBIT\_CARD\_EXPIRY**

    The expiration date for a credit or debit card. This number is usually four digits long and is often formatted as *month/year* or *MM/YY*. Amazon Bedrock Guardrails recognizes expiration dates such as *01/21*, *01/2021*, and *Jan 2021*. 
  + **CREDIT\_DEBIT\_CARD\_NUMBER**

    The number for a credit or debit card. These numbers can vary from 13 to 16 digits in length. However, Amazon Bedrock also recognizes credit or debit card numbers when only the last four digits are present. 
  + **PIN**

    A four-digit personal identification number (PIN) with which you can access your bank account. 
  + **INTERNATIONAL\_BANK\_ACCOUNT\_NUMBER**

    An International Bank Account Number has specific formats in each country. For more information, see [www.iban.com/structure](https://www.iban.com/structure).
  + **SWIFT\_CODE**

    A SWIFT code is a standard format of Bank Identifier Code (BIC) used to specify a particular bank or branch. Banks use these codes for money transfers such as international wire transfers.

    SWIFT codes consist of eight or 11 characters. The 11-digit codes refer to specific branches, while eight-digit codes (or 11-digit codes ending in 'XXX') refer to the head or primary office.
+ **IT**
  + **IP\_ADDRESS**

    An IPv4 address, such as *198.51.100.0*. 
  + **MAC\_ADDRESS**

    A *media access control* (MAC) address is a unique identifier assigned to a network interface controller (NIC). 
  + **URL**

    A web address, such as *www.example.com*. 
  + **AWS\_ACCESS\_KEY**

    A unique identifier that's associated with a secret access key; you use the access key ID and secret access key to sign programmatic AWS requests cryptographically. 
  + **AWS\_SECRET\_KEY**

    A unique identifier that's associated with an access key. You use the access key ID and secret access key to sign programmatic AWS requests cryptographically. 
+ **USA specific**
  + **US\_BANK\_ACCOUNT\_NUMBER**

    A US bank account number, which is typically 10 to 12 digits long. 
  + **US\_BANK\_ROUTING\_NUMBER**

    A US bank account routing number. These are typically nine digits long, 
  + **US\_INDIVIDUAL\_TAX\_IDENTIFICATION\_NUMBER**

    A US Individual Taxpayer Identification Number (ITIN) is a nine-digit number that starts with a "9" and contain a "7" or "8" as the fourth digit. An ITIN can be formatted with a space or a dash after the third and forth digits. 
  + **US\_PASSPORT\_NUMBER**

    A US passport number. Passport numbers range from six to nine alphanumeric characters. 
  + **US\_SOCIAL\_SECURITY\_NUMBER**

    A US Social Security Number (SSN) is a nine-digit number that is issued to US citizens, permanent residents, and temporary working residents. 
+ **Canada specific**
  + **CA\_HEALTH\_NUMBER**

    A Canadian Health Service Number is a 10-digit unique identifier, required for individuals to access healthcare benefits. 
  + **CA\_SOCIAL\_INSURANCE\_NUMBER**

    A Canadian Social Insurance Number (SIN) is a nine-digit unique identifier, required for individuals to access government programs and benefits.

    The SIN is formatted as three groups of three digits, such as *123-456-789*. A SIN can be validated through a simple check-digit process called the [Luhn algorithm](https://www.wikipedia.org/wiki/Luhn_algorithm).
+ **UK Specific**
  + **UK\_NATIONAL\_HEALTH\_SERVICE\_NUMBER**

    A UK National Health Service Number is a 10-17 digit number, such as *485 777 3456*. The current system formats the 10-digit number with spaces after the third and sixth digits. The final digit is an error-detecting checksum.
  + **UK\_NATIONAL\_INSURANCE\_NUMBER**

    A UK National Insurance Number (NINO) provides individuals with access to National Insurance (social security) benefits. It is also used for some purposes in the UK tax system.

    The number is nine digits long and starts with two letters, followed by six numbers and one letter. A NINO can be formatted with a space or a dash after the two letters and after the second, forth, and sixth digits.
  + **UK\_UNIQUE\_TAXPAYER\_REFERENCE\_NUMBER**

    A UK Unique Taxpayer Reference (UTR) is a 10-digit number that identifies a taxpayer or a business. 
+ **Custom**
  + **Regex filter**

    You can use regular expressions to define patterns for a guardrail to recognize and act upon such as serial number, booking ID, or other custom patterns.

**Note**  
The PII model performs more effectively when it is provided with sufficient context. To enhance its accuracy, include more contextual information and avoid submitting single words or short phrases to the model. Since PII can be context-dependent (for example. a string of digits might represent an AWS KMS key or a user ID depending on the surrounding information), providing comprehensive context is crucial for accurate identification. 

**Note**  
PII masking applies only to content that is sent to the inference model (input prompts) and content that is returned from the inference model (model responses). It does not apply to the following:  
**Model invocation logs** — If you enabled [Monitor model invocation using CloudWatch Logs and Amazon S3](model-invocation-logging.md), the `input` field in Amazon CloudWatch Logs always contains the original, unmodified request regardless of guardrail intervention. To protect sensitive information in your logs, use [Amazon CloudWatch log data protection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html).
**Guardrails trace output** — The `match` field in [GuardrailPiiEntityFilter](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GuardrailPiiEntityFilter.html) that is returned in API responses (such as the `trace` object of the Converse API) contains the original PII value, not the masked output. This behavior is by design so that your application can use the detection result for its own logic.

**Note**  
A custom regex filter of sensitive information filters does not support a regex lookaround match. 

## Configure sensitive information policy for your guardrail
<a name="guardrails-sensitive-information-policy-configure"></a>

You can configure sensitive information policies for your guardrail by using the AWS Management Console or Amazon Bedrock API.

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Guardrails**, and then choose **Create guardrail**.

1. For **Provide guardrail details** page, do the following:

   1. In the **Guardrail details** section, provide a **Name** and optional **Description** for the guardrail.

   1. For **Messaging for blocked prompts**, enter a message that displays when your guardrail is applied. Select the **Apply the same blocked message for responses** checkbox to use the same message when your guardrail is applied on the response.

   1. (Optional) To enable [cross-Region inference](guardrails-cross-region.md) for your guardrail, expand **Cross-Region inference**, and then select **Enable cross-Region inference for your guardrail**. Choose a guardrail profile that defines the destination AWS Regions where guardrail inference requests can be routed.

   1. (Optional) By default, your guardrail is encrypted with an AWS managed key. To use your own customer-managed KMS key, expand **KMS key selection** and select the **Customize encryption settings (advanced)** checkbox.

      You can select an existing AWS KMS key or select **Create an AWS KMS key** to create a new one.

   1. (Optional) To add tags to your guardrail, expand **Tags**, and then, select **Add new tag** for each tag you define.

      For more information, see [Tagging Amazon Bedrock resources](tagging.md).

   1. Choose **Next**.

1. On the **Add sensitive information filters page** page, do the following to configure filters to block or mask sensitive information:

   1. In the **PII types** section, configure the personally identifiable information (PII) categories to block, mask, or take no action (detect mode). You have the following options:
      + To add all PII types, select the dropdown arrow next to **Add PII type**. Then select the guardrail behavior to apply to them.
**Warning**  
If you specify a behavior, any existing behavior that you configured for PII types will be overwritten.
      + To delete a PII type, select the trash can icon (![Trash can icon representing a delete action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/trash.png)).
      + To delete rows that contain errors, select **Delete all** and then select **Delete all rows with error**
      + To delete all PII types, select **Delete all** and then select **Delete all rows**
      + To search for a row, enter an expression in the search bar.
      + To show only rows with errors, select the dropdown menu labeled **Show all** and select **Show errors only**.
      + To configure the size of each page in the table or the column display in the table, select the settings icon (![Gear icon representing settings or configuration options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/settings.png)). Set your preferences and then select **Confirm**.

   1. In the **Regex patterns** section, use regular expressions to define patterns for the guardrail to filter. You have the following options:
      + To add a pattern, select **Add regex pattern**. Configure the following fields:    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html)
      + To edit a pattern, select the three dots icon in the same row as the topic in the **Actions** column. Then select **Edit**. After you are finished editing, select **Confirm**.
      + To delete a pattern or patterns, select the checkboxes for the patterns to delete. Select **Delete** and then select **Delete selected**.
      + To delete all the patterns, select **Delete** and then select **Delete all**.
      + To search for a pattern, enter an expression in the search bar.
      + To configure the size of each page in the table or the column display in the table, select the settings icon (![Gear icon representing settings or configuration options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/settings.png)). Set your preferences and then select **Confirm**.

   1. When you finish configuring sensitive information filters, select **Next** or **Skip to review and create**.

------
#### [ API ]

To create a guardrail with sensitive information policies, send a [CreateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateGuardrail.html) request. The request format is as follows:

```
POST /guardrails HTTP/1.1
Content-type: application/json

{
    "blockedInputMessaging": "string",
    "blockedOutputsMessaging": "string",
    "sensitiveInformationPolicyConfig": {
        "piiEntitiesConfig": [{
            "type": "ADDRESS | EMAIL | PHONE | NAME | SSN | ...",
            "action": "BLOCK | ANONYMIZE | NONE",
            "inputAction": "BLOCK | ANONYMIZE | NONE",
            "inputEnabled": true,
            "outputAction": "BLOCK | ANONYMIZE | NONE",
            "outputEnabled": true
        }],
        "regexesConfig": [{
            "name": "string",
            "pattern": "string",
            "action": "BLOCK | ANONYMIZE | NONE",
            "description": "string",
            "inputAction": "BLOCK | ANONYMIZE | NONE",
            "inputEnabled": true,
            "outputAction": "BLOCK | ANONYMIZE | NONE",
            "outputEnabled": true
        }]
    },
    "description": "string",
    "kmsKeyId": "string",
    "name": "string",
    "tags": [{
        "key": "string",
        "value": "string"
    }],
    "crossRegionConfig": {
        "guardrailProfileIdentifier": "string"
    }
}
```
+ Specify a `name` and `description` for the guardrail.
+ Specify messages for when the guardrail successfully blocks a prompt or a model response in the `blockedInputMessaging` and `blockedOutputsMessaging` fields.
+ Configure sensitive information policies in the `sensitiveInformationPolicyConfig` object:
  + Use `piiEntitiesConfig` array to configure predefined PII entity types:
    + Specify the PII entity type in the `type` field. Valid values include `ADDRESS`, `EMAIL`, `PHONE`, `NAME`, `US_SOCIAL_SECURITY_NUMBER`, among others.
    + Specify the action to take when the PII entity is detected in the `action` field. Choose `BLOCK` to block content, `ANONYMIZE` to mask the content, or `NONE` to take no action but return detection information.
    + (Optional) Use `inputAction`, `inputEnabled`, `outputAction`, and `outputEnabled` to configure different behaviors for prompts and responses.
  + Use `regexesConfig` array to define custom patterns to detect:
    + Specify a `name` for the regex pattern (1-100 characters).
    + Define the regular expression `pattern` to detect (1-500 characters).
    + Specify the `action` to take when the pattern is detected. Choose `BLOCK` to block content, `ANONYMIZE` to mask the content, or `NONE` to take no action but return detection information.
    + (Optional) Provide a `description` for the regex pattern (1-1000 characters).
    + (Optional) Use `inputAction`, `inputEnabled`, `outputAction`, and `outputEnabled` to configure different behaviors for prompts and responses.
+ (Optional) Attach any tags to the guardrail. For more information, see [Tagging Amazon Bedrock resources](tagging.md).
+ (Optional) For security, include the ARN of a KMS key in the `kmsKeyId` field.
+ (Optional) To enable [cross-Region inference](guardrails-cross-region.md), specify a guardrail profile in the `crossRegionConfig` object.

The response format is as follows:

```
HTTP/1.1 202
Content-type: application/json

{
    "createdAt": "string",
    "guardrailArn": "string",
    "guardrailId": "string",
    "version": "string"
}
```

------