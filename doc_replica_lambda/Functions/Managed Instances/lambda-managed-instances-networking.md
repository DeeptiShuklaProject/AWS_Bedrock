

# Networking for Lambda Managed Instances
<a name="lambda-managed-instances-networking"></a>

When running Lambda Managed Instances functions, you need to configure network connectivity to enable your functions to access resources outside the VPC. This includes AWS services such as Amazon S3 and DynamoDB. The connectivity is also needed for transmitting telemetry data to CloudWatch Logs and X-Ray.

## Connectivity options
<a name="lambda-managed-instances-connectivity-options"></a>

There are three primary approaches for configuring VPC connectivity, each with different trade-offs for cost, security, and complexity.

## Public subnet with an internet gateway
<a name="lambda-managed-instances-public-subnet-igw"></a>

This option uses a public subnet with direct internet access through an internet gateway. You can choose between IPv4 and IPv6 configurations.

### IPv4 with internet gateway
<a name="lambda-managed-instances-ipv4-igw"></a>

**To configure IPv4 connectivity with an internet gateway**

1. Create or use an existing public subnet with an IPv4 CIDR block.

1. Attach an internet gateway to your VPC.

1. Update the route table to route `0.0.0.0/0` traffic to the internet gateway.

1. Ensure resources have public IPv4 addresses or Elastic IP addresses assigned.

1. Configure security groups to allow outbound traffic on the required ports.

This configuration provides bidirectional connectivity, allowing both outbound connections from your functions and inbound connections from the internet.

### IPv6 with internet gateway
<a name="lambda-managed-instances-ipv6-igw"></a>

**To configure IPv6 connectivity with an internet gateway**

1. Enable IPv6 on your VPC.

1. Create or use an existing public subnet with an IPv6 CIDR block assigned.

1. Attach an internet gateway to your VPC (the same internet gateway can handle both IPv4 and IPv6).

1. Update the route table to route `::/0` traffic to the internet gateway.

1. Verify that the AWS services you need to access support IPv6 in your Region.

1. Configure security groups to allow outbound traffic on the required ports.

This configuration provides bidirectional connectivity using IPv6 addressing.

### IPv6 with egress-only internet gateway
<a name="lambda-managed-instances-ipv6-egress-only"></a>

**To configure IPv6 connectivity with an egress-only internet gateway**

1. Enable IPv6 on your VPC.

1. Create or use an existing public subnet with an IPv6 CIDR block assigned.

1. Attach an egress-only internet gateway to your VPC.

1. Update the route table to route `::/0` traffic to the egress-only internet gateway.

1. Verify that the AWS services you need to access support IPv6 in your Region.

1. Configure security groups to allow outbound traffic on the required ports.

This configuration provides outbound-only connectivity, preventing inbound connections from the internet while allowing your functions to initiate outbound connections.

## VPC endpoints
<a name="lambda-managed-instances-vpc-endpoints"></a>

VPC endpoints enable you to privately connect your VPC to supported AWS services without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection. Traffic between your VPC and the AWS service does not leave the Amazon network.

**To configure VPC endpoints**

1. Open the Amazon VPC console at [console.aws.amazon.com/vpc/](http://console.aws.amazon.com/vpc/).

1. In the navigation pane, choose **Endpoints**.

1. Choose **Create endpoint**.

1. For **Service category**, choose **AWS services**.

1. For **Service name**, select the service endpoint you need (for example, `com.amazonaws.region.s3` for Amazon S3).

1. For **VPC**, select your VPC.

1. For **Subnets**, select the subnets where you want to create endpoint network interfaces. For high availability, select subnets in multiple Availability Zones.

1. For **Security groups**, select the security groups to associate with the endpoint network interfaces. The security groups must allow inbound traffic from your function's security group on the required ports.

1. Choose **Create endpoint**.

Repeat these steps for each AWS service that your functions need to access.

## Private subnet with NAT gateway
<a name="lambda-managed-instances-private-subnet-nat"></a>

This option uses a NAT gateway to provide internet access for resources in private subnets while keeping the resources private.

**To configure a private subnet with NAT gateway**

1. Create a public subnet (if one doesn't already exist) with a CIDR block.

1. Attach an internet gateway to your VPC.

1. Create a NAT gateway in the public subnet and assign an Elastic IP address.

1. Update the public subnet route table to add a route: `0.0.0.0/0` → internet gateway.

1. Create or use an existing private subnet with a CIDR block.

1. Update the private subnet route table to add a route: `0.0.0.0/0` → NAT gateway.

1. Configure security groups to allow outbound traffic on the required ports.

For high availability, deploy one NAT gateway in each Availability Zone and configure route tables per Availability Zone to use the local NAT gateway. This prevents cross-AZ data transfer charges and improves resilience.

## Choosing a connectivity option
<a name="lambda-managed-instances-choosing-connectivity"></a>

Consider the following factors when choosing a connectivity option:

**Public subnet with internet gateway**
+ Simplest configuration with lowest cost
+ Suitable for development and testing environments
+ Resources can receive inbound connections from the internet (security consideration)
+ Supports both IPv4 and IPv6

**VPC endpoints**
+ Highest security, traffic stays within the AWS network
+ Lower latency compared to internet routing
+ Recommended for production environments with strict security requirements
+ Higher cost per endpoint, per Availability Zone, and per GB processed
+ Requires an endpoint in each Availability Zone for high availability

**Private subnet with NAT gateway**
+ Resources remain private with no inbound internet access
+ Standard enterprise architecture pattern
+ Supports all IPv4 internet traffic
+ Moderate cost with NAT gateway hourly and data processing charges
+ Supports IPv4 only

## Next steps
<a name="lambda-managed-instances-networking-next-steps"></a>
+ Learn about [capacity providers for Lambda Managed Instances](lambda-managed-instances-capacity-providers.md)
+ Understand [scaling for Lambda Managed Instances](lambda-managed-instances-scaling.md)
+ Review runtime-specific guides for [Java](lambda-managed-instances-java-runtime.md), [Node.js](lambda-managed-instances-nodejs-runtime.md), and [Python](lambda-managed-instances-python-runtime.md)
+ Understand [security and permissions for Lambda Managed Instances](lambda-managed-instances-security.md)