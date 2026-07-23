# Chapter 28: AWS CloudTrail & AWS Config — Audit & Compliance

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
