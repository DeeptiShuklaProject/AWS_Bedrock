

# Connect to your knowledge base through AgentCore Gateway
<a name="kb-gateway-target"></a>

AgentCore Gateway lets you expose your Amazon Bedrock managed knowledge base as a tool using the Model Context Protocol (MCP). After you add a knowledge base target to a gateway, any MCP-compatible client can query the knowledge base as a standard MCP tool. The connector exposes two tools:
+ `AgenticRetrieveStream` — a multi-step, streaming agentic retrieval that plans, retrieves iteratively, and streams back results and an optional synthesized, citation-backed answer.
+ `Retrieve` — a single search that returns the most relevant passages with source references.

The gateway acts as an intermediary that handles authentication, parameter injection, and schema subsetting. As an administrator, you bind the knowledge base and control which parameters are exposed to the calling agent and which are hidden with preconfigured defaults.

**Note**  
Knowledge base gateway targets are supported only for managed knowledge bases, and only with IAM-based outbound authentication (the `GATEWAY_IAM_ROLE` credential provider type).

**Prerequisites**
+ A managed knowledge base, and its knowledge base ID.
+ An AgentCore Gateway and a gateway service role with permission to retrieve from the knowledge base (`bedrock:Retrieve` on the knowledge base ARN).

For complete instructions — including creating the gateway target with the AWS SDK or AWS CLI, configuring the gateway service role and trust policy, controlling which retrieval parameters the agent can set, invoking the tools, and the full input and response schemas — see [Amazon Bedrock Managed Knowledge Bases as Connector Target](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html) in the *Amazon Bedrock AgentCore Developer Guide*.

## Invoke with Strands Agents
<a name="kb-gateway-target-invoke-strands"></a>

If you have an existing agent built with the [Strands Agents SDK](https://strandsagents.com/latest/) and the [AgentCore starter toolkit](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-toolkit.html), you can connect it to your knowledge base gateway target by switching the MCP client to use SigV4 authentication against the gateway endpoint.

Install the `mcp-proxy-for-aws` package:

```
pip install mcp-proxy-for-aws
```

Then update your MCP client to point to the gateway URL with IAM authentication:

```
from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

GATEWAY_URL = "{{https://your-gateway-url/mcp}}"

def get_streamable_http_mcp_client() -> MCPClient:
    """Returns an MCP Client with SigV4 auth for AgentCore Gateway."""
    return MCPClient(lambda: aws_iam_streamablehttp_client(
        endpoint=GATEWAY_URL,
        aws_region="{{us-west-2}}",
        aws_service="bedrock-agentcore",
    ))
```

The key changes from a standard MCP client setup are:
+ Replace `streamablehttp_client` from the `mcp` package with `aws_iam_streamablehttp_client` from `mcp-proxy-for-aws`.
+ Set the `endpoint` to your AgentCore Gateway URL.
+ Specify `aws_service="bedrock-agentcore"` for SigV4 signing.

Once connected, the knowledge base tools are auto-discovered through `tools/list` and available to the agent without additional configuration.