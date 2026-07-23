# Chapter 24: AWS CodePipeline — Continuous Delivery Service

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
