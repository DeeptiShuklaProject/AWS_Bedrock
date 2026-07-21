# 🎓 AWS Bedrock AgentCore: Skill Matrix & Learning Roadmap

Welcome to the **AWS Bedrock AgentCore** master skill index. This document serves as a live dashboard tracking the concepts, skills, and code templates learned across all 12 episodes of the series. 

---

## 📊 Learning Progress Dashboard

| Ep. | Episode Title | Core Skills Covered | Status | Quick Links |
| :---: | :--- | :--- | :---: | :---: |
| **01** | **Building Your First Production-Ready AI Agent** | MicroVM session isolation, CLI setup, Strands SDK integration | 🟢 Completed | [Summary](./summaries/01_summary.md) \| [Notes](./summaries/01_notes.md) \| [Questions](./summaries/01_questions.md) |
| **02** | **Build Your First Agentic AI App Step-by-Step** | MCP (Model Context Protocol), Swarms, Multi-Agent systems | 🟡 In Progress | [Summary](./summaries/02_summary.md) \| [Notes](./summaries/02_notes.md) \| [Questions](./summaries/02_questions.md) |
| **03** | **Runtime Deep Dive** | Firecracker MicroVM lifecycles, execution boundaries, limits | 🔴 Pending | [Summary](./summaries/03_summary.md) \| [Notes](./summaries/03_notes.md) \| [Questions](./summaries/03_questions.md) |
| **04** | **Gateway Deep Dive** | API exposure via AWS Lambda, SSE streaming, DB connectivity | 🔴 Pending | [Summary](./summaries/04_summary.md) \| [Notes](./summaries/04_notes.md) \| [Questions](./summaries/04_questions.md) |
| **05** | **Secure Your Agent Workflows** | Cognito/IAM integration, user identity propagation, Actor IDs | 🔴 Pending | [Summary](./summaries/05_summary.md) \| [Notes](./summaries/05_notes.md) \| [Questions](./summaries/05_questions.md) |
| **06** | **Browser Tool & Code Interpreter Tool** | Headless Chromium automation, Python code sandboxes | 🔴 Pending | [Summary](./summaries/06_summary.md) \| [Notes](./summaries/06_notes.md) \| [Questions](./summaries/06_questions.md) |
| **07** | **Memory Deep Dive** | Short-term vs. Long-term DynamoDB-backed memory persistence | 🔴 Pending | [Summary](./summaries/07_summary.md) \| [Notes](./summaries/07_notes.md) \| [Questions](./summaries/07_questions.md) |
| **08** | **Moving AI Agents from Prototype to Production** | Docker compilation via CodeBuild, ECR deployments, S3 pipelines | 🔴 Pending | [Summary](./summaries/08_summary.md) \| [Notes](./summaries/08_notes.md) \| [Questions](./summaries/08_questions.md) |
| **09** | **AgentCore Observability** | OpenTelemetry tracing, LLM prompt inspection, CloudWatch logs | 🔴 Pending | [Summary](./summaries/09_summary.md) \| [Notes](./summaries/09_notes.md) \| [Questions](./summaries/09_questions.md) |
| **10** | **AgentCore Evaluations** | Correctness evaluations, latency benchmarking, resilience testing | 🔴 Pending | [Summary](./summaries/10_summary.md) \| [Notes](./summaries/10_notes.md) \| [Questions](./summaries/10_questions.md) |
| **11** | **Control Agent-to-Tool Interactions** | IAM fine-grained control, safety guardrails, prompt filtering | 🔴 Pending | [Summary](./summaries/11_summary.md) \| [Notes](./summaries/11_notes.md) \| [Questions](./summaries/11_questions.md) |
| **12** | **Episodic Memory and Patterns** | Semantic vector search across sessions, context window optimization | 🔴 Pending | [Summary](./summaries/12_summary.md) \| [Notes](./summaries/12_notes.md) \| [Questions](./summaries/12_questions.md) |

---

## 🛠️ Key Technical Competencies (Episode-by-Episode Skill Map)

### 🔹 Episode 01: Production-Ready Agents & CLI Setup
* **Skills Learned**:
  - How to bridge the "Prototype to Production" gap using isolated containerized runtimes.
  - Initializing `BedrockAgentCoreApp` wrappers in Python for any orchestrator.
  - Setting up the local toolkit and deploying code serverlessly via `agentcore launch`.
* **Code Sandbox**:
  ```python
  from bedrock_agent_core import BedrockAgentCoreApp
  app = BedrockAgentCoreApp()
  
  @app.invoke
  def invoke(payload, context):
      return agent.run(payload.get("prompt"), session_id=context.session_id)
  ```

### 🔹 Episode 02: Strands & Model Context Protocol (MCP)
* **Skills Learned**:
  - Designing multi-agent topologies (supervisor pattern, swarm, graph).
  - Building and running standard **MCP (Model Context Protocol)** servers.
  - Integrating custom search APIs (Perplexity) and scheduling engines.

### 🔹 Episode 03: AgentCore Runtime Lifecycle
* **Skills Learned**:
  - Architecting serverless systems with AWS Firecracker microVMs.
  - Managing payload constraints (100MB inputs) and handling long-running executions (up to 8 hours).
  - Fine-tuning container configurations and handling concurrent session load.

### 🔹 Episode 04: AgentCore Gateway Patterns
* **Skills Learned**:
  - Connecting agent flows to internal databases (e.g., DynamoDB) through managed API gateways.
  - Wrapping AWS Lambda functions as MCP endpoints.
  - Implementing Server-Sent Events (SSE) for asynchronous telemetry.

### 🔹 Episode 05: Enterprise Identity & Propagation
* **Skills Learned**:
  - Configuring secure OIDC/Cognito user token flows.
  - Propagating `Actor ID` across microservices to enable granular security controls.
  - Enforcing row-level access permissions on persistent agent memory.

### 🔹 Episode 06: Native Tool Sandboxing
* **Skills Learned**:
  - Orchestrating headless browser tools (Chromium) inside containers for scraping.
  - Executing user-generated scripts dynamically in sandboxed Code Interpreters.

### 🔹 Episode 07: State & Memory Architecture
* **Skills Learned**:
  - Storing conversational turns in DynamoDB-backed short-term session state.
  - Executing automated summary jobs to maintain a persistent user profile across separate conversations.

### 🔹 Episode 08: Production CI/CD Pipelines
* **Skills Learned**:
  - Automating container builds with AWS CodeBuild and pushing images to AWS ECR.
  - Tracking cloud-native application deployments using logs.

### 🔹 Episode 09: System Observability & Tracing
* **Skills Learned**:
  - Exporting telemetry metrics to external observability platforms using OpenTelemetry.
  - Tracking input/output tokens and tracing LLM execution routes.

### 🔹 Episode 10: AI Evaluations & Testing
* **Skills Learned**:
  - Establishing benchmark test suites to evaluate agent correctness.
  - Running automated user simulation tests to find routing failures.

### 🔹 Episode 11: Security Policies & Guardrails
* **Skills Learned**:
  - Deploying AWS IAM policies to restrict AWS service interaction.
  - Setting up Amazon Bedrock Guardrails to prevent prompt injections.

### 🔹 Episode 12: Advanced Episodic Memory
* **Skills Learned**:
  - Querying session histories using vector database embeddings.
  - Designing context-window management routines to prune historical messages.

---

## 📖 How to Update & Maintain This Project
1. **Watch the episode** / **Review the transcript** inside the `/transcripts/` folder.
2. **Fill in the templates**: Open the corresponding files inside the `/summaries/` directory (e.g. `02_notes.md`, `02_questions.md`) and document the detailed notes and Q&A.
3. **Update this Skill Matrix**: Change the Status emoji in the **Learning Progress Dashboard** (e.g., change 🔴/🟡 to 🟢) to reflect your progress!
