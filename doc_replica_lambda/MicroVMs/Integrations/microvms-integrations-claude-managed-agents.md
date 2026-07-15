

# Using Lambda MicroVMs as a sandbox for Claude Managed Agents
<a name="microvms-integrations-claude-managed-agents"></a>

AWS Lambda MicroVMs is a managed sandbox provider in self-hosted sandboxes for Claude Managed Agents; keeping sensitive files, packages, and services in infrastructure you control. Anthropic hosts the agent loop and Claude model, while the Lambda MicroVM is where your tool calls run. With this pattern, you control the execution environment – what is installed, what network access is available, and what resources the agent can reach.

Each MicroVM is a Firecracker-isolated virtual machine with snapshot-based sub-second startup, runs for up to 8 hours, and can be terminated when the session ends. Sessions never share state. You get the security boundary of a VM with the operational model of serverless – no clusters to manage, no idle capacity to pay for. You can orchestrate MicroVMs with AWS services to implement the self-hosted sandbox spec as described below. Review the [Claude Managed Agents Self-Hosted Sandboxes on Lambda MicroVMs](https://github.com/aws-samples/sample-lambda-microvm-claude-managed-agents) reference sample for more detail.

## How it works
<a name="microvms-integrations-claude-how-it-works"></a>

A control plane launches one MicroVM per Claude session:

1. A session reaches the running state and Anthropic sends a `session.status_run_started` webhook to an endpoint in your account.

1. A launcher Lambda function verifies the webhook signature, then calls `RunMicroVM`.

1. Your code on the MicroVM claims the session, executes tool calls (bash, read, write, edit, glob, grep) in `/workspace`, and posts results back to Anthropic.

1. The MicroVM is suspended or terminated when the session ends.

Your Anthropic organization API key never reaches AWS compute. The launcher only passes an AWS Secrets Manager reference to your Anthropic environment key; the MicroVM's execution role allows the code to read it at runtime.

## Key properties
<a name="microvms-integrations-claude-properties"></a>


| Property | Benefit | 
| --- | --- | 
| Firecracker isolation | Hardware-virtualized boundary per session | 
| Snapshot-based boot | Resume from Firecracker snapshot in sub-second to single-digit seconds | 
| IAM via IMDSv2 | Uses short-term, least privilege credentials | 
| Stateful duration | Can run up to 8 hours with full disk and memory access | 
| Pay-per-session | MicroVMs are terminated when sessions are complete, which ends billing | 

## Prerequisites
<a name="microvms-integrations-claude-prereqs"></a>
+ An AWS account with permissions for Amazon Simple Storage Service (Amazon S3), AWS Identity and Access Management (IAM), Secrets Manager, , AWS WAF, Lambda, and Lambda MicroVMs
+ A Claude Managed Agents agent with a `self_hosted` environment
+ An environment key and webhook signing secret from the Claude Console

## Deploying the reference implementation
<a name="microvms-integrations-claude-deploy"></a>

![Architecture diagram showing the Claude Self-Hosted Sandboxes on Lambda MicroVMs reference implementation](http://docs.aws.amazon.com/lambda/latest/dg/images/microvms-claude-managed-agents-architecture.png)


The [Claude Managed Agents Self-Hosted Sandboxes on Lambda MicroVMs](https://github.com/aws-samples/sample-lambda-microvm-claude-managed-agents) repository provides a minimal, working deployment. It includes:
+ A CloudFormation stack (Amazon API Gateway, launcher Lambda function, Secrets Manager secrets, Amazon S3 bucket, IAM roles)
+ A MicroVM image (`Dockerfile`, Node.js EnvironmentWorker, lifecycle hooks)
+ A deploy script and verification script

Deployment steps:

1. Deploy the CloudFormation stack.

1. Store the environment key and signing secret in the created Secrets Manager secrets.

1. Build the MicroVM image.

1. Register the stack's webhook URL in the Claude Console.

1. Verify by creating a session.

For detailed instructions, see the repository README.

## Networking
<a name="microvms-integrations-claude-networking"></a>

Lambda MicroVMs have public internet access by default – no configuration is needed to reach `api.anthropic.com`.

To access private resources like an Amazon Aurora database or Amazon ElastiCache cluster, or to apply your own network restrictions, attach a VPC egress connector at launch time. See [Working with egress network connectors](microvms-networking.md#microvms-networking-connectors).

## Idle policy
<a name="microvms-integrations-claude-idle-policy"></a>

Set `suspendedDurationSeconds: 0` and `autoResumeEnabled: false` for per-session MicroVMs. Set `maximumDurationInSeconds` as a ceiling for stuck sessions (max 28,800 s).

```
{
  "maxIdleDurationSeconds": 120,
  "suspendedDurationSeconds": 0,
  "autoResumeEnabled": false
}
```

## Monitoring
<a name="microvms-integrations-claude-monitoring"></a>

**Application logs** – Review application logs in CloudWatch Logs:

```
aws logs tail /aws/lambda-microvms/claude-worker --follow
```

**Running MicroVMs** – List the running MicroVMs in your account:

```
aws lambda-microvms list-microvms \
  --image-identifier claude-worker \
  --query 'items[].[microvmId,state,startedAt]' --output table
```

## Troubleshooting
<a name="microvms-integrations-claude-troubleshooting"></a>


| Symptom | Cause | 
| --- | --- | 
| Webhook returns 401 | Signing secret mismatch or stale delivery | 
| No MicroVM launches | Webhook not registered for session.status\_run\_started, or launcher Lambda function execution role missing RunMicroVM permission | 
| MicroVM terminates immediately | /run hook timeout – raise runTimeoutInSeconds | 
| Worker exits immediately | Outbound HTTPS to api.anthropic.com blocked | 
| Image build fails S3\_\* | Build role or bucket misconfiguration | 