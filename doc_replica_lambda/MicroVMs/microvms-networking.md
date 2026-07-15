

# Networking
<a name="microvms-networking"></a>

You configure network access for your AWS Lambda MicroVMs by associating Network Connector resources with your MicroVM at run time. Network connectors are specified when you call `run-microvm` and cannot be changed while a MicroVM is running.

## Overview
<a name="microvms-networking-overview"></a>

Each MicroVM can have independent ingress (inbound) and egress (outbound) network configurations:
+ **Ingress network connectors** enable inbound connectivity. Clients connect to a service-managed HTTPS endpoint, and Lambda forwards traffic to ports you configure within the MicroVM. Ingress connectors are AWS-managed – you reference them by ARN when running a MicroVM.
+ **Egress network connectors** enable outbound traffic. By default, MicroVMs have public internet access. You can create a customer-managed VPC egress connector to route outbound traffic through your VPC instead.

A single connector can be reused across many MicroVMs – this is the intended usage pattern.

## Inbound connectivity
<a name="microvms-networking-inbound"></a>

Each Lambda MicroVM is reachable at a unique HTTPS endpoint URL, assigned when you call `run-microvm`. Clients send requests to this endpoint over HTTPS. Lambda routes each request to a port inside your MicroVM, where your application receives it.

By default, requests received at the endpoint are routed to port 8080 inside the MicroVM. To route to a different port, see [Port routing](#microvms-networking-port-routing).

The following protocols are supported on the inbound endpoint:
+ HTTP/1.1
+ HTTP/2
+ WebSockets
+ gRPC
+ Server-Sent Events (SSE)

**Note**  
Traffic between your client and the MicroVM endpoint is always encrypted with TLS. Your application can serve requests over either HTTP or HTTPS internally.

### Port routing
<a name="microvms-networking-port-routing"></a>

Lambda selects the target port inside your MicroVM using the following order of priority:

1. **`X-aws-proxy-port` header** – For standard HTTP requests, include this header with the target port number.

1. **WebSocket subprotocol** – If your WebSocket client can't set custom headers, specify the target port as a subprotocol named `lambda-microvms.port.{{N}}`, where {{N}} is the port number. You provide subprotocols when you open the WebSocket connection. For an example, see [Protocols](microvms-launching.md#microvms-launching-websocket).

1. **Default (8080)** – If neither is specified, requests route to port 8080.

**Important**  
The target port must be within the `allowedPorts` defined in the authentication token. Requests to unauthorized ports receive a 403 Forbidden response.

### Authentication
<a name="microvms-networking-auth"></a>

All requests to a MicroVM endpoint require a valid authentication token in the `X-aws-proxy-auth` header. You generate tokens using `create-microvm-auth-token`. Each token is an encrypted JWE (JSON Web Encryption) string scoped to:
+ A specific MicroVM (identified by ID).
+ A set of allowed ports (single port, range, or all ports).
+ An expiration time (configured at token creation).

The following example creates a token and uses it to send an authenticated request:

```
aws lambda-microvms create-microvm-auth-token \
  --microvm-identifier {{microvm-id}} \
  --expiration-in-minutes 30 \
  --allowed-ports '[{"port":8080}]'
```

```
curl 'https://{{microvm-endpoint}}' \
  -H 'X-aws-proxy-auth: {{TOKEN}}' \
  -H 'X-aws-proxy-port: 8080'
```

For a complete walkthrough of creating tokens and connecting to a MicroVM, including WebSocket connections, see [Connecting to a MicroVM](microvms-launching.md#microvms-launching-connecting).

### Error responses
<a name="microvms-networking-errors"></a>

The following HTTP status codes are returned by the MicroVM endpoint when it cannot process or deliver a request to your application. These responses come from the endpoint, not from your application.


| Code | Status | Cause and resolution | 
| --- | --- | --- | 
| 400 | Bad Request | Malformed request, or an invalid port header or WebSocket subprotocol. Verify the format. | 
| 403 | Forbidden | Missing, expired, or invalid token; or the requested port is not in the token's allowedPorts. Generate a new token, or use an allowed port. | 
| 429 | Too Many Requests | Rate limit exceeded (account-level or per-MicroVM). Retry with exponential backoff. | 
| 500 | Internal Server Error | An internal error occurred. Retry the request. | 
| 502 | Bad Gateway | Application not responding, or auto-resume did not succeed within the maximum number of retry attempts. See [Auto-resume](microvms-launching.md#microvms-launching-auto-resume). | 

### Request headers
<a name="microvms-networking-headers"></a>

The `X-aws-proxy-*` header namespace is reserved by Lambda for request metadata, such as the authentication token (`X-aws-proxy-auth`) and target port (`X-aws-proxy-port`). Lambda removes `X-aws-proxy-*` headers before forwarding the request to your application.

### Request/response bandwidth
<a name="microvms-networking-bandwidth"></a>

Each Lambda MicroVM has a request/response bandwidth that scales linearly with its size. This bandwidth applies to all traffic through the MicroVM endpoint, both inbound requests and outbound responses.


| MicroVM size (baseline) | Max bandwidth | 
| --- | --- | 
| 0.5 GB, 0.25 vCPU | 1 MB/s (8 Mbps) | 
| 1 GB, 0.5 vCPU | 2 MB/s (16 Mbps) | 
| 2 GB, 1 vCPU | 4 MB/s (32 Mbps) | 
| 4 GB, 2 vCPU | 8 MB/s (64 Mbps) | 
| 8 GB, 4 vCPU | 16 MB/s (128 Mbps) | 

If you experience increased request latency due to network saturation, either reduce your request concurrency or payload size, or select a larger MicroVM size to increase the available bandwidth.

### HTTP/2 support
<a name="microvms-networking-http2"></a>

Lambda MicroVMs supports HTTP/2 on the inbound endpoint. Lambda negotiates the protocol through ALPN (Application-Layer Protocol Negotiation) during the TLS handshake, preferring HTTP/2 and falling back to HTTP/1.1. An HTTP/2-capable client uses it automatically.

To use HTTP/2 between the endpoint and your application inside the MicroVM:
+ **Your application serves TLS** – Lambda negotiates HTTP/2 with your application through ALPN, falling back to HTTP/1.1 if HTTP/2 isn't supported.
+ **Your application serves plaintext HTTP** – Include the `X-aws-proxy-force-h2: true` header in your request to use HTTP/2 on the connection to your application.

## Outbound connectivity
<a name="microvms-networking-outbound"></a>

By default, Lambda MicroVMs have public internet access on the egress path. To connect MicroVMs with resources in your private VPCs – such as RDS, ElastiCache, internal APIs, and on-premises systems through Direct Connect or VPN – create a Lambda Network Connector with your VPC configuration.

When using VPC egress, outbound traffic is subject to security group rules and network ACLs governing traffic in your VPC.

## Working with egress network connectors
<a name="microvms-networking-connectors"></a>

Egress network connectors route outbound traffic from your MicroVM through your VPC. You create a connector once, then reference it by ARN when starting MicroVMs through the `run-microvm` command.

### Prerequisites
<a name="microvms-networking-connectors-prereqs"></a>

Before creating a network connector, you need an IAM role that allows Lambda to create elastic network interfaces (ENIs) in your VPC. The role requires the following permissions:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CreateENI",
      "Effect": "Allow",
      "Action": "ec2:CreateNetworkInterface",
      "Resource": [
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:subnet/*",
        "arn:aws:ec2:*:*:security-group/*"
      ]
    },
    {
      "Sid": "TagENI",
      "Effect": "Allow",
      "Action": "ec2:CreateTags",
      "Resource": "arn:aws:ec2:*:*:network-interface/*",
      "Condition": {
        "StringEquals": {
          "ec2:ManagedResourceOperator": "network-connectors.lambda.amazonaws.com"
        }
      }
    }
  ]
}
```

### Creating a network connector
<a name="microvms-networking-connectors-create"></a>

Create a connector by specifying your VPC subnets, security groups, and network protocol (`IPv4` or `DualStack`):

```
aws lambda-core create-network-connector \
  --name my-connector \
  --configuration '{
    "VpcEgressConfiguration": {
      "SubnetIds": ["{{subnet-xxx}}"],
      "SecurityGroupIds": ["{{sg-xxx}}"],
      "NetworkProtocol": "IPv4",
      "AssociatedComputeResourceTypes": ["MicroVm"]
    }
  }' \
  --operator-role arn:aws:iam::{{123456789012}}:role/NetworkConnectorOperatorRole
```

### Network connector states
<a name="microvms-networking-connectors-states"></a>

A connector must be in `ACTIVE` state before you can reference it in `run-microvm`.


| State | Description | 
| --- | --- | 
| PENDING | Connector is being created (underlying ENIs are being provisioned). | 
| ACTIVE | Connector is ready to use. | 
| INACTIVE | Connector is temporarily inactive. | 
| FAILED | Provisioning or update failed. Check StateReason. | 
| DELETING | Connector is being deleted; ENIs are being cleaned up. | 
| DELETE\_FAILED | Deletion failed. | 

### Running a MicroVM with a network connector
<a name="microvms-networking-connectors-run"></a>

Reference the connector ARN when running a MicroVM:

```
aws lambda-microvms run-microvm \
  --image-identifier arn:aws:lambda:us-east-1:{{123456789012}}:microvm-image:my-microvm-image \
  --egress-network-connectors {{connector-arn}} \
  --idle-policy '{"maxIdleDurationSeconds":900,"suspendedDurationSeconds":1800,"autoResumeEnabled":false}'
```

**Note**  
Before you update or delete a connector, ensure all MicroVMs using it have terminated. Modifying a connector that is actively in use can cause network connectivity issues for running MicroVMs.