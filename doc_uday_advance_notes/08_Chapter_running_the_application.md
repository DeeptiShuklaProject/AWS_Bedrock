# 08_Chapter_running_the_application

## 🎯 Learning Objectives
In this chapter, you will learn how to:
- Initialize the agent's deployment settings using the CLI.
- Launch the agent container locally and in the cloud.
- Invoke the active agent endpoint and test response generation.
- Troubleshoot execution issues during local and cloud runs.

### Importance of This Chapter
Running the agent locally enables quick debugging, while deploying to the cloud runtime tests performance under real-world network and security conditions.

---

## 📦 Technical Terms Explained

> **📦 Technical Term Explained**
>
> **Term:** Deployment
>
> **Simple Explanation:** Deployment is the process of packaging your application and moving it to a hosting environment (like a server or cloud service) where it can run and be accessed by users.
>
> **Why do we need it?** It moves your code from a local environment to a public or private server, making it accessible to external services and users.
>
> **Where is it used?** In CI/CD pipelines or deployment commands that compile container images and push them to ECR.

---

> **📦 Technical Term Explained**
>
> **Term:** Endpoint
>
> **Simple Explanation:** An endpoint is a specific URL or web address exposed by a service that clients use to send requests and access resources.
>
> **Why do we need it?** It serves as the interface that client applications call to communicate with your agent.
>
> **Where is it used?** Configured in API gateways or compute runtimes to route user traffic.

---

> **📦 Technical Term Explained**
>
> **Term:** Model Invocation
>
> **Simple Explanation:** Model Invocation is the act of sending a prompt or input payload to a foundation model API and receiving its generated completion response.
>
> **Why do we need it?** It is the core execution step where the agent requests reasoning, text generation, or decision-making from the LLM.
>
> **Where is it used?** In your agent's execution loops when communicating with Bedrock APIs.

---

## 🛠️ Step-by-Step Invocation Workflow

Follow these three commands to run and deploy your agent.

### Step 1: Configure the Agent Metadata
Before deploying, initialize the deployment configuration:
```bash
agent-core configure -e src/main.py
```
- **Why this command is required:** Launches the interactive wizard to set up ECR repositories, generate the Dockerfile, and create the deployment configuration.
- **Expected Output:**
  ```text
  Configuration saved to: bedrock_agent_core.yaml
  Generated build assets and Dockerfile.
  Ready to deploy.
  ```

---

### Step 2: Deploy and Launch the Container
To compile the Docker image and deploy it to the serverless runtime:
- **Cloud Run (Triggers AWS CodeBuild):**
  ```bash
  agent-core launch
  ```
- **Local Test Run (Using local Docker/Podman):**
  ```bash
  agent-core launch --local
  ```
- **Expected Output:**
  ```text
  Initiating CodeBuild process...
  Uploaded assets to S3.
  Docker build complete. Pushed image to ECR.
  Agent Endpoint Created: arn:aws:agentcore:us-east-1:123456789012:agent/aws-agent
  ```

---

### Step 3: Invoke the Live Agent
To send a prompt and verify the response:
```bash
agent-core invoke --prompt "Hello, agent! How are you?"
```
- **Why this command is required:** Sends a POST request payload containing the prompt to the active agent endpoint.
- **Expected Output:**
  ```text
  Invoking agent: aws_show_and_tell_agent
  Response (Streaming):
  Hi there! I am your Bedrock AgentCore assistant. How can I help you today?
  Session ID: session-98765-abcde
  ```

---

## 📝 Practical Exercise
Run `agent-core configure -e src/main.py` in your terminal, complete the setup wizard, and check that `bedrock_agent_core.yaml` is created.

---

## 🔄 Chapter Recap
- We configured the agent using the interactive setup wizard.
- We deployed the agent using the launch command.
- We verified the deployment by invoking the endpoint.
- We are ready to walk through the Python code in detail.
