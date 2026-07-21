# AWS Bedrock AgentCore & Strands: Episode-by-Episode Summary

This document provides a highly detailed technical breakdown of the 12-part **AWS Show & Tell: Amazon Bedrock AgentCore Deep Dive Series**. Each section contains a link to the original YouTube video, a link to the corresponding local transcript file, and a comprehensive summary of key concepts, architectures, and demo implementations.

---

## 🛠️ Episode-by-Episode Technical Breakdowns

### 1. Building Your First Production-Ready AI Agent
* **Original Video**: [AWS Show & Tell - Episode 1](https://www.youtube.com/watch?v=wzIQDPFQx30)
* **Local Transcript**: [01_building_your_first_production_ready_ai_agent.txt](./transcripts/01_building_your_first_production_ready_ai_agent.txt)
* **Detailed Summary**:
  * Introduces the core philosophy of **Amazon Bedrock AgentCore**: decoupling agent orchestration frameworks (like AWS Strands, LangGraph, or CrewAI) from their secure, scalable deployment in the cloud.
  * Details the **AgentCore Runtime** infrastructure, which packages the agent code into a Docker image, pushes it to ECR, and deploys it in serverless microVMs (powered by AWS Firecracker) for hardware-level session isolation.
  * Covers default runtime thresholds: up to 100MB payloads, 8-hour execution times, and fast container cold starts.
  * Shows how to quickly adapt a local Strands agent for AgentCore by initializing the `BedrockAgentCoreApp` wrapper and using CLI commands: `agentcore configure`, `launch`, and `invoke`.

---

### 2. Build Your First Agentic AI App Step-by-Step
* **Original Video**: [AWS Show & Tell - Episode 2](https://www.youtube.com/watch?v=aijS9fWB854)
* **Local Transcript**: [02_build_your_first_agentic_ai_app_step_by_step.txt](./transcripts/02_build_your_first_agentic_ai_app_step_by_step.txt)
* **Detailed Summary**:
  * Walks through the development of a multi-agent **Personal Assistant** using the open-source **AWS Strands SDK** and the Model Context Protocol (MCP).
  * Discusses architectural patterns for multi-agent systems, including swarms, hierarchical supervisor-agent setups, graphs, and structured workflows.
  * Explains the **Model Context Protocol (MCP)** standard for unifying tool definitions and data sources.
  * Shows the step-by-step assembly of three sub-agents:
    * **Calendar Assistant**: Leverages a built-in current time tool to manage scheduling.
    * **Search Assistant**: Connects to the internet via a local Perplexity MCP server.
    * **Code Assistant**: Generates, executes, and debugging code using out-of-the-box sandbox tools.

---

### 3. Runtime Deep Dive
* **Original Video**: [AWS Show & Tell - Episode 3](https://www.youtube.com/watch?v=wizEw5a4gvM)
* **Local Transcript**: [03_runtime_deep_dive.txt](./transcripts/03_runtime_deep_dive.txt)
* **Detailed Summary**:
  * Explains the lower-level mechanics of **AgentCore Runtime** container lifecycle management and security.
  * Breaks down **Session Isolation**: every user session is mapped directly to an isolated microVM. This hard security boundary prevents any possibility of data/memory leaks between concurrent users.
  * Discusses state persistence: in-memory state and local files are preserved in the microVM as long as the session stays active (up to 8 hours).
  * Details timeouts and limits: 15-minute synchronous request timeout, 60-minute streaming limit, and 500 default concurrent sessions limit. Shows how Dockerfiles are auto-generated and compiled via AWS CodeBuild.

---

### 4. Gateway Deep Dive
* **Original Video**: [AWS Show & Tell - Episode 4](https://www.youtube.com/watch?v=atWXM5lziY8)
* **Local Transcript**: [04_gateway_deep_dive.txt](./transcripts/04_gateway_deep_dive.txt)
* **Detailed Summary**:
  * Focuses on the **AgentCore Gateway** for exposing enterprise internal databases, microservices, and legacy APIs to external agents.
  * Explains how Gateway acts as a secure, managed broker, wrapping private targets (like AWS Lambda functions) and exposing them as standardized MCP servers.
  * Details the usage of HTTP Server-Sent Events (SSE) for maintaining live streaming channels between agents and the gateway.
  * Demonstrates querying customer profiles and warranty statuses from DynamoDB tables using Lambda function targets mapped to the gateway.

---

### 5. Secure Your Agent Workflows
* **Original Video**: [AWS Show & Tell - Episode 5](https://www.youtube.com/watch?v=wv2doVDF7KQ)
* **Local Transcript**: [05_secure_your_agent_workflows.txt](./transcripts/05_secure_your_agent_workflows.txt)
* **Detailed Summary**:
  * Explains user identity propagation and authentication using **AgentCore Identity**.
  * Shows how to configure **Amazon Cognito** as the identity provider (IDP) and authenticate requests via JWT bearer tokens passed in headers.
  * Discusses **Actor ID propagation**: passing the authenticated user's context downstream so that tools and databases can enforce granular row-level security (e.g., verifying that a user can only access their own records).

---

### 6. Browser Tool and Code Interpreter Tool
* **Original Video**: [AWS Show & Tell - Episode 6](https://www.youtube.com/watch?v=z3lAJ-Nf_lk)
* **Local Transcript**: [06_browser_tool_and_code_interpreter_tool.txt](./transcripts/06_browser_tool_and_code_interpreter_tool.txt)
* **Detailed Summary**:
  * Demonstrates the secure, sandboxed execution of complex actions using out-of-the-box AgentCore tools.
  * **Browser Tool**: Deploys a headless Chromium instance inside a secure container sandbox. The agent can use it to automate web tasks, take page screenshots, click elements, and scrape legacy web portals.
  * **Code Interpreter**: Runs an isolated Python execution environment. The agent dynamically generates Python code to solve math problems, format complex data tables, and analyze uploaded Excel/CSV files.

---

### 7. Memory Deep Dive
* **Original Video**: [AWS Show & Tell - Episode 7](https://www.youtube.com/watch?v=-N4v6-kJgwA)
* **Local Transcript**: [07_memory_deep_dive.txt](./transcripts/07_memory_deep_dive.txt)
* **Detailed Summary**:
  * Explains the distinction between short-term session state and automated long-term persistent personalization.
  * **Short-Term Memory**: Keeps track of conversational turns and state within a single session run.
  * **Long-Term Memory**: Automatically summarizes conversations, extracts user preferences, and persists user profile summaries across multiple sessions over time.
  * Details the integration with DynamoDB behind the scenes for saving and retrieving memory objects.

---

### 8. Moving AI Agents from Prototype to Production
* **Original Video**: [AWS Show & Tell - Episode 8](https://www.youtube.com/watch?v=WyGK8UcAxKo)
* **Local Transcript**: [08_moving_ai_agents_from_prototype_to_production.txt](./transcripts/08_moving_ai_agents_from_prototype_to_production.txt)
* **Detailed Summary**:
  * Focuses on the production deployment lifecycle, CI/CD, and scaling.
  * Shows how the AgentCore SDK zips the project files, uploads them to S3, and triggers AWS CodeBuild to compile and push Docker images to ECR.
  * Discusses auto-scaling of the serverless runtime and monitoring the deployment via trailing CloudWatch log streams.

---

### 9. AgentCore Observability
* **Original Video**: [AWS Show & Tell - Episode 9](https://www.youtube.com/watch?v=wWQgawUPr1k)
* **Local Transcript**: [09_agentcore_observability.txt](./transcripts/09_agentcore_observability.txt)
* **Detailed Summary**:
  * Covers tracing and logging of agent actions to debug behaviors and inspect LLM prompts/responses.
  * Demonstrates integration with **OpenTelemetry** to export trace metrics to AWS CloudWatch or third-party APM platforms (like Arize, Datadog, or Honeycomb).
  * Shows how to inspect latency, token usage, tool selection pathways, and routing decisions.

---

### 10. AgentCore Evaluations
* **Original Video**: [AWS Show & Tell - Episode 10](https://www.youtube.com/watch?v=i0h7xA8cqYs)
* **Local Transcript**: [10_agentcore_evaluations.txt](./transcripts/10_agentcore_evaluations.txt)
* **Detailed Summary**:
  * Details systematic testing of agent behavior before deploying to production.
  * Shows how to set up and run the evaluation suite to measure correctness, response latency, and reliability.
  * Covers prompt template validation, tool selection accuracy, and testing how the agent handles extreme user inputs and load.

---

### 11. Control Agent-to-Tool Interactions
* **Original Video**: [AWS Show & Tell - Episode 11](https://www.youtube.com/watch?v=q_9htaugcgI)
* **Local Transcript**: [11_control_agent_to_tool_interactions.txt](./transcripts/11_control_agent_to_tool_interactions.txt)
* **Detailed Summary**:
  * Focuses on safety filters, guardrails, and access policies.
  * Explains how to use IAM policies to restrict which S3 buckets, Cognito directories, or DynamoDB tables an agent has access to.
  * Covers configuring input/output guardrails to prevent prompt injections, block toxic content, and safeguard sensitive data leakage.

---

### 12. Episodic Memory and Patterns
* **Original Video**: [AWS Show & Tell - Episode 12](https://www.youtube.com/watch?v=1EEIGsKIjGA)
* **Local Transcript**: [12_episodic_memory_and_patterns.txt](./transcripts/12_episodic_memory_and_patterns.txt)
* **Detailed Summary**:
  * Explains the **Episodic Memory** cognitive pattern for optimizing LLM context window limits.
  * Shows how the agent performs semantic vector searches on historical sessions to retrieve only relevant past episodes, rather than stuffing the entire raw chat history into the context window.
  * Focuses on keeping token costs low and maintaining high reasoning performance.
