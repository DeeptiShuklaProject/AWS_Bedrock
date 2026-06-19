

# Capacity and Performance
<a name="capacity-limits-cost-optimization"></a>

Amazon Bedrock offers flexible capacity options to match your workload requirements and budget. Understanding the differences between on-demand tiers (Flex, Priority, Standard), reserved tier, batch processing, and cross-region inference helps you optimize both performance and cost.

## Capacity Options
<a name="capacity-options"></a>


| Capacity Type | Use Case | Key Characteristics | 
| --- | --- | --- | 
| On-Demand: Flex | Sporadic, low-volume workloads |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 
| On-Demand: Standard | Regular production workloads |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 
| On-Demand: Priority | High-priority, latency-sensitive apps |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 
| Reserved Tier | Consistent, high-volume workloads |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 
| Batch | Large-scale, non-time-sensitive processing |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 
| Cross-Region Inference | High availability, traffic bursting |  [See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html)  | 

## Limits & Quotas
<a name="limits-quotas"></a>

### On-Demand Limits (by tier)
<a name="on-demand-limits"></a>


| Tier | RPM Range | TPM Range | Throttling Risk | 
| --- | --- | --- | --- | 
| Flex | 10-100 | 5K-50K | High | 
| Standard | 100-500 | 50K-150K | Medium | 
| Priority | 500-1000\+ | 150K-300K\+ | Low | 
+ Burst capacity: Available across all tiers for short spikes
+ Soft limits: Increasable via service quota requests
+ Model-specific: Actual limits vary by foundation model

### Reserved Tier Limits
<a name="reserved-tier-limits"></a>
+ Minimum commitment: 1 model unit
+ Maximum units: Account and region-specific
+ Input/output token limits: Based on purchased units
+ No RPM throttling within purchased capacity

### Batch Processing Limits
<a name="batch-processing-limits"></a>
+ Job size: Up to 10,000 records per batch
+ File size: Maximum 200 MB input file
+ Processing time: 24-hour completion window
+ Concurrent jobs: Region-specific quotas

### Cross-Region Inference
<a name="cross-region-inference-limits"></a>
+ Inherits on-demand tier limits per region
+ No additional quota overhead
+ Automatic routing (no manual limit management)

## Choosing a Tier
<a name="cost-optimization"></a>

### Decision Framework
<a name="decision-framework"></a>


| Scenario | Recommended Option | Why | 
| --- | --- | --- | 
| Development/testing | Flex | Lowest cost, acceptable for non-production | 
| Standard production | Standard | Best cost-performance balance | 
| Critical user-facing apps | Priority | Reliability and performance over cost | 
| Steady high-volume load | Reserved Tier | 30-50% savings with commitment | 
| Bulk data processing | Batch | 50% discount, non-urgent workloads | 
| Mission-critical uptime | Cross-Region Inference | Availability > cost | 

### Optimization Strategies
<a name="optimization-strategies"></a>

**Choose the Right On-Demand Tier**
+ Start with Standard for most workloads
+ Downgrade to Flex for dev/test environments
+ Upgrade to Priority only when throttling impacts users
+ Monitor CloudWatch throttle metrics to inform decisions

**Transition to Reserved Tier**
+ When consistent load exceeds 40% of on-demand costs
+ Calculate break-even: (Monthly on-demand cost) vs (Reserved commitment)
+ Use 1-month commitment initially
+ Reserved tier can work alongside any on-demand tier

**Use Batch for**
+ Training data generation
+ Content moderation backlogs
+ Report generation
+ Data enrichment pipelines

**Combine Approaches**
+ Reserved tier for baseline traffic
+ Standard on-demand for moderate bursts
+ Priority on-demand for critical peak periods
+ Batch for offline processing
+ Cross-region for failover only

**Cost Monitoring**
+ Compare tier costs: Flex < Standard < Priority
+ Track tokens per request (optimize prompts)
+ Use CloudWatch metrics for use and throttling
+ Set billing alarms for unexpected spikes
+ Review reserved tier use monthly
+ Evaluate tier upgrades only when throttling occurs