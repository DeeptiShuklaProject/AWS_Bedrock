# Module 19 - Cloud Integration (AWS)

## Learning Objectives
* Deploy containerized workloads to AWS, push images to Amazon ECR, configure Amazon ECS, and manage Fargate tasks.

## Prerequisites
* **Prerequisites**: Module 18

---

## Detailed Explanation
### 1. Amazon ECR (Elastic Container Registry)
A secure, managed Docker registry provided by AWS.
* **Authentication CLI Command**:
  ```bash
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
  ```
* **Tagging & Pushing**:
  ```bash
  docker tag my-app:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
  docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
  ```

### 2. Amazon ECS (Elastic Container Service)
AWS's native container orchestrator. It runs containers using two launch types:
* **EC2 Launch Type**: You manage the underlying virtual machines.
* **Fargate Launch Type (Serverless)**: AWS manages the server provisioning, and you pay only for the vCPU and memory allocated to the tasks.

### 3. Deploying using Task Definitions
A Task Definition is a blueprint for your application (similar to docker-compose). It configures ports, images, environment variables, IAM roles, and logging (CloudWatch).

---

## Hands-on Exercise
### Hands-on Exercise: CLI login to ECR
Write out the command block to authenticate your local Docker daemon with an AWS ECR repository using your IAM credentials.

## Assignment
Design a CloudFormation or Terraform manifest snippet that creates an ECR repository.

---

## Quiz

### Q1: What is AWS Fargate?
- A serverless engine to run containers without managing VMs
- An image compression utility
- A local virtual machine editor
- A database system

*Answer*: **A serverless engine to run containers without managing VMs**

### Q2: Which service stores Docker images on AWS?
- Amazon ECR
- Amazon ECS
- Amazon S3
- AWS CodeBuild

*Answer*: **Amazon ECR**

---

## Interview Preparation

### Q: What is the difference between ECS Task Definition and an ECS Service?
*Answer*: A Task Definition is the blueprint detailing container images, ports, and volumes. An ECS Service handles orchestration details, keeping a specified number of task instances running and attaching them to load balancers.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Exposing AWS IAM Access Keys inside Docker image environment files.
* **Troubleshooting**: If ECS tasks fail with 'Pending' state indefinitely, check if your VPC has Internet Gateways or NAT Gateways configuration to pull the image from ECR.

## Best Practices & Tips
* Assign IAM roles (Task Execution Role) directly to tasks instead of granting broad permissions to EC2 host instances.

---

## Summary & Cheat Sheet
| CLI Tool | Command Purpose |
|---|---|
| `aws ecr` | Manage registries and authentication |
| `docker push` | Upload image to remote ECR URL |

---

## References & Further Reading
* AWS ECS Developer Guide.
