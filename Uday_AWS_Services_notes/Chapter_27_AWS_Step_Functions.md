# Chapter 27: AWS Step Functions — Serverless Workflow Orchestration

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
