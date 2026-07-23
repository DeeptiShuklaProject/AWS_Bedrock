# Chapter 26: Amazon SQS & Amazon SNS — Messaging & Notification

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
