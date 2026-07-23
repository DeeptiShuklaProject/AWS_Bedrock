import os

notes_dir = r"c:\Users\nishu\workspace\wscs_bedrock\Uday_AWS_Services_notes"

chapters = {}

# Chapter 22: Route 53
chapters["Chapter_22_Amazon_Route_53.md"] = """# Chapter 22: Amazon Route 53 — Highly Available DNS Service

---

## 1. Service Overview

### What is Amazon Route 53?
Amazon Route 53 is a highly available and scalable cloud Domain Name System (DNS) web service designed to route end-user requests to internet applications running on AWS or on-premises infrastructure.

### Key Routing Policies
- **Simple Routing**: Standard 1:1 DNS query response.
- **Weighted Routing**: Distribute traffic across resources based on specified relative weights.
- **Latency Routing**: Route requests to the AWS region that provides the lowest network latency.
- **Failover Routing**: Active-Passive disaster recovery failover based on Route 53 health check status.
- **Geolocation & Geoproximity**: Route traffic based on user geographic location or physical proximity.

---

## 2. Learning Objectives
1. Configure Hosted Zones, Alias records, and Routing Policies.
2. Implement DNS failover architectures.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        user["User Browser"]
        r53["Amazon Route 53"]
        primary["Primary Region (ALB / EC2)"]
        secondary["Secondary DR Region (S3 / ALB)"]

        user -->|DNS Query| r53
        r53 -->|Active (Healthy)| primary
        r53 -.->|Failover (Unhealthy)| secondary
    end
```

---

## 10. Code Examples

### Python (Boto3)
```python
import boto3

route53 = boto3.client('route53')

response = route53.create_hosted_zone(
    Name='example.com',
    CallerReference='unique-req-001'
)
print("Hosted Zone ID:", response['HostedZone']['Id'])
```

### AWS CLI
```bash
aws route53 create-hosted-zone --name example.com --caller-reference unique-req-001
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["Amazon Route 53"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: DNS Resolution Failure During Regional Outage
### Incident Summary
Secondary region failed to receive traffic during primary region outage due to unconfigured health checks on Alias records.

### Root Cause Analysis
Alias records did not evaluate target health (`EvaluateTargetHealth=False`), preventing automatic failover.

---

## 26. Cheat Sheet
| Record Type | Description |
| :--- | :--- |
| **A Record** | Maps hostname to IPv4 address |
| **Alias Record** | AWS-specific smart routing record to ALB/CloudFront/S3 without DNS lookup cost |

---

## 27. Chapter Summary
Route 53 powers global DNS routing and automated disaster recovery failover.
"""

# Chapter 23: CloudFormation
chapters["Chapter_23_AWS_CloudFormation.md"] = """# Chapter 23: AWS CloudFormation — Infrastructure as Code

---

## 1. Service Overview

### What is AWS CloudFormation?
AWS CloudFormation is an Infrastructure as Code (IaC) service that allows you to model, provision, and manage AWS and third-party resources by declaring them in JSON or YAML templates.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        developer["DevOps / CI/CD"]
        cfn["AWS CloudFormation Engine"]
        stack["AWS Stack Resources (VPC, EC2, RDS)"]

        developer -->|Submit YAML Template| cfn
        cfn -->|Provision Resources| stack
    end
```

---

## 10. Code Examples

### CloudFormation (YAML)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Enterprise Web Server Stack
Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-0c55b159cbfafe1f0
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["AWS CloudFormation"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: Stack Update Rollback Failed (`DELETE_FAILED`)
### Incident Summary
CloudFormation stack update failed and stuck in `UPDATE_ROLLBACK_FAILED` due to non-empty S3 bucket.

### Resolution
Manually empty the S3 bucket or skip the resource during rollback via `--resources-to-skip`.

---

## 27. Chapter Summary
CloudFormation enables consistent, repeatable, automated infrastructure deployments.
"""

# Chapter 24: CodePipeline
chapters["Chapter_24_AWS_CodePipeline.md"] = """# Chapter 24: AWS CodePipeline — Continuous Delivery Service

---

## 1. Service Overview
AWS CodePipeline is a fully managed continuous delivery service that automates release pipelines for fast and reliable application and infrastructure updates.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        source["Source (GitHub / S3)"]
        pipeline["AWS CodePipeline"]
        build["Build & Test (CodeBuild)"]
        deploy["Deploy (ECS / Lambda)"]

        source --> pipeline
        pipeline --> build
        build --> deploy
    end
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["AWS CodePipeline"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: Pipeline Execution Blocked on Artifact Encryption Key
### Cause
CodeBuild phase could not decrypt S3 artifact due to missing KMS key permission.

---

## 27. Chapter Summary
CodePipeline automates CI/CD workflows from source code check-in to production deployment.
"""

# Chapter 25: EventBridge
chapters["Chapter_25_Amazon_EventBridge.md"] = """# Chapter 25: Amazon EventBridge — Event-Driven Serverless Bus

---

## 1. Service Overview
Amazon EventBridge is a serverless event bus service that makes it easy to connect applications using data from your own applications, integrated Software-as-a-Service (SaaS) applications, and AWS services.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        publisher["Event Producer (S3 / SaaS)"]
        bus["EventBridge Event Bus"]
        rule["Filter Rule"]
        target["Target (Lambda / SQS)"]

        publisher --> bus
        bus --> rule
        rule --> target
    end
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["Amazon EventBridge"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: Events Dropped Due to Invalid Event Pattern Match
### Cause
JSON payload field casing mismatch in EventBridge rule pattern.

---

## 27. Chapter Summary
EventBridge simplifies event-driven decoupling across cloud applications.
"""

# Chapter 26: SQS & SNS
chapters["Chapter_26_Amazon_SQS_and_Amazon_SNS.md"] = """# Chapter 26: Amazon SQS & Amazon SNS — Messaging & Notification

---

## 1. Service Overview
Amazon SQS (Simple Queue Service) provides message queuing for decoupling distributed components. Amazon SNS (Simple Notification Service) provides pub/sub messaging for high-throughput fan-out notifications.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        publisher["Publisher"]
        sns["SNS Topic"]
        sqs1["SQS Queue A"]
        sqs2["SQS Queue B"]
        worker1["Worker A"]
        worker2["Worker B"]

        publisher --> sns
        sns --> sqs1
        sns --> sqs2
        sqs1 --> worker1
        sqs2 --> worker2
    end
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["Amazon SQS & SNS"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: SQS Message Poison Pill Loops
### Cause
Failed message returned to queue indefinitely without Dead-Letter Queue (DLQ) configured.

---

## 27. Chapter Summary
SQS and SNS form the core of asynchronous messaging and fan-out decoupling on AWS.
"""

# Chapter 27: Step Functions
chapters["Chapter_27_AWS_Step_Functions.md"] = """# Chapter 27: AWS Step Functions — Serverless Workflow Orchestration

---

## 1. Service Overview
AWS Step Functions is a visual workflow service that helps developers build distributed applications, automate processes, orchestrate microservices, and create data pipelines using AWS services.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        trigger["Trigger (API / Event)"]
        sfn["Step Functions State Machine"]
        task1["Lambda Task 1"]
        choice["Choice State"]
        task2["Lambda Task 2"]

        trigger --> sfn
        sfn --> task1
        task1 --> choice
        choice --> task2
    end
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["AWS Step Functions"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: Workflow Execution Stuck in Running State
### Cause
Task state missing explicit timeout constraint (`TimeoutSeconds`).

---

## 27. Chapter Summary
Step Functions coordinates multi-step microservice workflows with built-in state management and error handling.
"""

# Chapter 28: CloudTrail & Config
chapters["Chapter_28_AWS_CloudTrail_and_AWS_Config.md"] = """# Chapter 28: AWS CloudTrail & AWS Config — Audit & Compliance

---

## 1. Service Overview
AWS CloudTrail records API calls and user activity across your AWS infrastructure. AWS Config continuously monitors and records AWS resource configurations and evaluates compliance against desired rules.

---

## 7. Internal Architecture

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        api["AWS API Request"]
        trail["AWS CloudTrail"]
        config["AWS Config"]
        s3["Secure Audit S3 Bucket"]

        api --> trail
        api --> config
        trail --> s3
        config --> s3
    end
```

---

## 17. Architecture Patterns

```mermaid
graph LR
    subgraph aws["AWS Cloud"]
        client["Client Application"]
        gateway["API Gateway / Entry"]
        core["AWS CloudTrail & AWS Config"]
        storage["DynamoDB / S3 Storage"]

        client --> gateway
        gateway --> core
        core --> storage
    end
```

---

# Production Incident War Room

## Incident 1: Unregistered Security Group Ingress Rule Not Auto-Remediated
### Cause
AWS Config Remediation Execution IAM Role missing EC2 revoke permissions.

---

## 27. Chapter Summary
CloudTrail and Config provide continuous governance, auditing, security visibility, and compliance enforcement across enterprise AWS environments.
"""

for fname, fcontent in chapters.items():
    fpath = os.path.join(notes_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(fcontent)
    print(f"Written {fname}")

print("All chapters 22-28 generated.")
