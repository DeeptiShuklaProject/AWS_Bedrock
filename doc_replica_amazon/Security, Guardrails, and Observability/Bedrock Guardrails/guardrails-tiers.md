

# Safeguard tiers for guardrails policies
<a name="guardrails-tiers"></a>

Amazon Bedrock Guardrails provides *safeguard tiers* for specific policies. Safeguard tiers have distinct performance characteristics and [language support](guardrails-supported-languages.md) for different application requirements and use cases.

Choosing a tier gives you control over when to adopt new capabilities or maintain consistency with your current guardrails setup.

The following guardrails policies support safeguard tiers:
+ Content filters ([text](guardrails-content-filters.md)) and [prompt attacks](guardrails-prompt-attack.md)
+ [Denied topics](guardrails-denied-topics.md)

## Available safeguard tiers
<a name="guardrails-available-tiers"></a>

Amazon Bedrock Guardrails provides the following safeguard tiers:

**Standard tier**  
Provides more robust performance compared to Classic tier and has more comprehensive language and code-related prompt support. For example, protection against prompt attacks performs more consistently and reliably with Standard tier. Guardrails with Standard tier also use [cross-Region inference](guardrails-cross-region.md). Standard tier supported with content filters and denied topics provides protection against harmful content introduced within code elements including comments, variable and function names, and string literals.

**Classic tier**  
Provides established guardrails functionality supporting English, French, and Spanish languages.

## Key differences between safeguard tiers
<a name="guardrails-tiers-key-differences"></a>

Understanding the differences between safeguard tiers helps you choose the right option for your application:


| Feature | Standard tier | Classic tier | 
| --- | --- | --- | 
| Content filter and prompt attacks | More robust than Classic tier | Established performance | 
| Denied topics | Maximum of 1,000 characters per definition | Maximum of 200 characters per definition | 
| Language support | [Extensive language support](guardrails-supported-languages.md) | English, French, Spanish | 
| Cross-Region inference | Supported | Not supported | 
| Prompt leakage detection | Supported | Not supported | 
| Coding use case support | Enhanced support for content filters, prompt attacks, and denied topics when handling code-related prompts and responses | N/A | 

## Choosing a safeguard tier for your use case
<a name="guardrails-choosing-a-tier"></a>

Determining the safeguard tier to use for your guardrail policies depends on your application requirements.

For example, consider Standard tier when:
+ Your application handles multiple languages
+ You need higher accuracy and performance for content filters, prompt attacks, and denied topics

Alternatively, you might still use Classic tier when:
+ Your application primarily uses English, French, or Spanish content
+ You need time before migrating from an existing guardrails implementation to Standard tier

## Migrating your guardrail to Standard tier
<a name="guardrails-tiers-migration"></a>

To configure an existing guardrail with Standard tier, do the following:

1. [Modify your guardrail](guardrails-edit.md) to use Standard tier and [cross-Region inference](guardrails-cross-region.md). 

1. (Recommended) Consider rolling out your updated guardrail using a phased approach by starting with noncritical workloads.

## Supported Regions for safeguard tiers
<a name="guardrails-tiers-regions"></a>

Safeguard tiers are supported in the following [AWS Regions](guardrails-supported.md) where Amazon Bedrock Guardrails is available:
+ US East (N. Virginia)
+ US East (Ohio)
+ US West (N. California)
+ US West (Oregon)
+ Canada (Central)
+ Europe (Frankfurt)
+ Europe (Stockholm)
+ Europe (Milan)
+ Europe (Spain)
+ Europe (Ireland)
+ Europe (London)
+ Europe (Paris)
+ Asia Pacific (Taipei)
+ Asia Pacific (Tokyo)
+ Asia Pacific (Seoul)
+ Asia Pacific (Mumbai)
+ Asia Pacific (Singapore)
+ Asia Pacific (Sydney)
+ Asia Pacific (Jakarta)
+ Asia Pacific (Melbourne)
+ Asia Pacific (Malaysia)
+ Asia Pacific (Thailand)
+ Middle East (UAE)
+ Israel (Tel Aviv)
+ AWS GovCloud (US-West)