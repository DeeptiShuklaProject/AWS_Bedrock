# Chapter 25: Amazon EventBridge — Event-Driven Serverless Bus

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
