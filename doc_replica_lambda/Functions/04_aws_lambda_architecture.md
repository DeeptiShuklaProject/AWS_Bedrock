# Section 4 – AWS Lambda Architecture

<a name="sec-4"></a>

Here are three common architectural patterns utilizing AWS Lambda:

### Architecture 1: Serverless API Backend
```
+----------------+      HTTP GET/POST      +-------------+      Proxy Event      +------------+      boto3 Write      +--------------+
| Client Browser | ──────────────────────► | API Gateway | ────────────────────► | AWS Lambda | ────────────────────► | DynamoDB     |
|                | ◄────────────────────── |             | ◄──────────────────── |            | ◄──────────────────── | (UsersTable) |
+----------------+      JSON Response      +-------------+     JSON Response     +------------+      Table Data       +--------------+
```

### Architecture 2: S3 Thumbnail Generator
```
+--------+     PutObject     +-----------------+     S3 Object Created     +------------+     Write Output     +-------------------+
| Client | ────────────────► | Source S3 Bucket| ────────────────────────► | AWS Lambda | ───────────────────► | Thumbnail Bucket  |
| Upload |                   | (uploads/)      |                           | (Pillow)   |                      | (thumbnails/)     |
+--------+                   +-----------------+                           +------------+                      +-------------------+
```

### Architecture 3: Infrastructure Scheduler
```
+----------------------+     Cron Trigger     +------------+     StopInstances API     +---------------+
| EventBridge Schedule | ───────────────────► | AWS Lambda | ────────────────────────► | EC2 Instances |
| (11:00 PM Daily)     |                      |            |                           | (Dev/Staging) |
+----------------------+                      +------------+                           +---------------+
```

---
