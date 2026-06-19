

# Best practices for cost attribution
<a name="cost-mgmt-best-practices"></a>

The following recommendations apply across the cost attribution mechanisms described in this chapter ([IAM principal attribution](cost-mgmt-iam-principal-tracking.md), [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Projects](cost-mgmt-projects.md), [Workspaces](cost-mgmt-workspaces.md), and [Per-request metadata tagging](cost-mgmt-request-metadata.md)). They are written for teams that need accurate, durable cost attribution across many users, applications, and environments.

## Choose the right mechanism for the question you are answering
<a name="cost-mgmt-best-practices-choose"></a>

Each mechanism is optimized for a different question. Pick based on the answer you need.
+ **Per-user or per-team dollars on your bill.** Use [IAM principal attribution](cost-mgmt-iam-principal-tracking.md). The caller identity is captured automatically on every `bedrock-runtime` call, and you can layer on principal or session tags for team, department, or cost center.
+ **Per-application or per-workload dollars.** Use [Application inference profiles](cost-mgmt-application-inference-profiles.md) on `bedrock-runtime`, or [Projects](cost-mgmt-projects.md) and [Workspaces](cost-mgmt-workspaces.md) on `bedrock-mantle`. These resources carry cost allocation tags that flow to AWS Cost Explorer and CUR 2.0.
+ **Per-prompt token usage and cost.** Use [Per-request metadata tagging](cost-mgmt-request-metadata.md) with your [model invocation logs](model-invocation-logging.md). Each call is recorded as a separate log entry with its own token counts, and you can slice by any tag you set on the request.
+ **Both invoice-accurate dollars and per-prompt detail.** Combine the two. Many teams run IAM principal attribution for native per-user/team dollars in CUR, and request metadata for the per-prompt token detail in their invocation logs.

## Design tags for analytics, not noise
<a name="cost-mgmt-best-practices-tagging"></a>
+ **Use stable, low-cardinality keys for analytics.** Keys such as `team`, `environment`, `feature`, `application`, or `costCenter` aggregate cleanly in AWS Cost Explorer and CUR. They produce a small set of distinct values that make filtering and grouping useful.
+ **Reserve high-cardinality values for request metadata.** Per-request identifiers such as session ID, trace ID, or experiment ID belong in [request metadata](cost-mgmt-request-metadata.md) only. They are appropriate for log analytics, but they bloat the cost-allocation-tag space if applied as resource or principal tags.
+ **Standardize tag keys and values across teams.** Agree on a small, organization-wide set of tag keys and a controlled vocabulary for values (for example, environments are `production`, `staging`, `development`, not free-form). Inconsistent tags fragment your reports.
+ **Activate cost allocation tags promptly.** Tags do not appear in AWS Cost Explorer or CUR until you activate them as cost allocation tags in the AWS Billing console, and activation is not retroactive. Activate tags as soon as you start using them, and allow up to 24 hours for new tags to appear.

## Enforce tagging in a shared layer, not on every developer
<a name="cost-mgmt-best-practices-enforcement"></a>

Per-call tagging mechanisms (request metadata, session tags) are opt-in. Amazon Bedrock does not reject calls that omit them. Relying on individual developers to set tags consistently across services produces gaps that are difficult to fix later.
+ **Stamp tags in a shared client wrapper or LLM gateway.** A single layer that all Amazon Bedrock traffic passes through is the most reliable place to set [request metadata](cost-mgmt-request-metadata.md) and AWS STS session tags on every call. This guarantees coverage without per-team discipline.
+ **Lean on automatically captured signals where possible.** IAM principal attribution captures the caller's identity automatically on every `bedrock-runtime` call, with no per-call code. Pair it with session tags from your IdP for user and team attribution that requires no enforcement.
+ **Restrict the call path with SCPs or IAM policies.** If you require all Amazon Bedrock traffic to flow through a tagging gateway, use service control policies or IAM policies to deny direct Amazon Bedrock access from outside that role. This makes the gateway the only call path, and therefore the only place tags need to be set.
+ **Cache assumed-role credentials when re-assuming per user.** If your gateway re-assumes a Amazon Bedrock role per user or tenant to vary identity in billing, cache the resulting credentials for the session lifetime. Calling `sts:AssumeRole` on every request can exceed AWS STS rate quotas.

## Treat tag values as log content
<a name="cost-mgmt-best-practices-data-handling"></a>
+ **Do not put sensitive data in request metadata or session tags.** Request metadata values are written to your [model invocation logs](model-invocation-logging.md), and session tags surface in CUR 2.0. Do not place personally identifiable information (PII), credentials, secrets, or regulated data in tag values. If you need to attribute by user, use a stable internal identifier (for example, a hashed user ID) rather than an email address.
+ **Stay within the tag limits.** Request metadata is limited to 16 entries per request, with 256 characters per key and per value. IAM principals support up to 50 tags. Resource tags on projects, workspaces, and application inference profiles follow the standard AWS tagging limits.

## Combine mechanisms for full coverage
<a name="cost-mgmt-best-practices-combining"></a>

The native methods ([IAM principal attribution](cost-mgmt-iam-principal-tracking.md), [Application inference profiles](cost-mgmt-application-inference-profiles.md), [Projects](cost-mgmt-projects.md), [Workspaces](cost-mgmt-workspaces.md)) deliver invoice-accurate aggregated dollars in AWS Cost Explorer and CUR. [Per-request metadata tagging](cost-mgmt-request-metadata.md) delivers per-prompt token detail in your invocation logs. They are complementary, and most production deployments benefit from running both.

A typical setup looks like this:
+ Enable [IAM principal attribution](cost-mgmt-iam-principal-tracking.md) for native per-user and per-team dollars in your billing tools, with no per-call code.
+ Tag [application inference profiles](cost-mgmt-application-inference-profiles.md) (for `bedrock-runtime`) or [projects](cost-mgmt-projects.md) and [workspaces](cost-mgmt-workspaces.md) (for `bedrock-mantle`) for application-level dollars.
+ Enable [model invocation logging](model-invocation-logging.md) and stamp [request metadata](cost-mgmt-request-metadata.md) in your shared client or gateway for per-prompt detail.
+ Reconcile log-derived costs against CUR periodically at the model and usage-type grain to confirm your token-rate-card calculations match your invoice.