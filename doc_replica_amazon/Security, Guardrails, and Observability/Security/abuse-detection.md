

# Amazon Bedrock abuse detection
<a name="abuse-detection"></a>

As part of providing the Service, Amazon Bedrock may use automated abuse detection mechanisms to detect activity that violates our, or third-party model providers', terms of service or use policies.

Amazon Bedrock uses a zero operator access (ZOA) data security model. This means no operators of the service can access model input or output. Also, Amazon Bedrock uses a zero data retention (ZDR) data security model. This means that by default, Amazon Bedrock does not store model inputs or outputs.

However, for specific abuse detection purposes related to the following models, we may be required to store inputs and outputs:
+ For OpenAI GPT-5.4 and GPT-5.5, classifier-flagged traffic will be retained for up to 30 days for automated offline abuse detection.
+ For Anthropic Claude Fable 5, inputs and outputs will be retained for up to 30 days. In order to use Claude Fable 5, as required by Anthropic, you must opt in to sharing retained traffic with Anthropic for abuse detection and potential human review.

Retained inputs and outputs are stored and processed by AWS and are not shared with third-party model providers, unless you opt in to sharing with the model provider. If cross-region inference is enabled for these models, retained inputs and outputs are stored in destination regions (i.e., the region where your inference request is processed). For these models, eligible customers may request full ZDR through their AWS account team.

You are responsible for the content you (and your end users) upload to Amazon Bedrock. To help stop the dissemination of child sexual abuse material ("CSAM"), Amazon Bedrock may use automated abuse detection mechanisms (such as hash matching technology or classifiers) to detect apparent CSAM. If Amazon Bedrock detects apparent CSAM in your image inputs, Amazon Bedrock will block the request and return a `ValidationException` (HTTP 400) error in the API response. Amazon Bedrock may store and review the flagged input or output exclusively to determine if it is CSAM and may also file a report with the National Center for Missing and Exploited Children (NCMEC) or a relevant authority. We take CSAM seriously and will continue to review our detection, blocking, and reporting mechanisms. You might be required by applicable laws to take additional actions, and you are responsible for those actions.

If an abuse detection mechanism identifies potential violations, we may request information about your use of Amazon Bedrock and compliance with relevant terms and policies. These requests are sent to the email address associated with your AWS account, so ensure that your account contact information is current and monitored. AWS may suspend your access to any model or Amazon Bedrock if you fail to comply with applicable terms or policies or are non-responsive.

Contact your AWS account team or AWS Support if you have additional questions.