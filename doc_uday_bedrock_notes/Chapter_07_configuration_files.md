# Chapter_07_configuration_files

## 1. Introduction
Separating configuration settings from application source code is key to building reusable, secure enterprise applications.

### What is it?
Configuration Files are structured text documents ('.env', 'bedrock_agent_core.yaml', 'pyproject.toml') used to store operational parameters, environment settings, entrypoint references, and access keys separately from application source code.

### Why is it important?
Hardcoding parameters like database names, API endpoints, or secret keys directly inside Python code creates severe security vulnerabilities and prevents the same application from running in different environments (such as testing or production). Storing settings in configuration files decouples environment parameters from codebase logic.

### How does it work?
At startup, the application reads parameters from local '.env' environment files using helper tools like 'python-dotenv' and parses project settings from 'bedrock_agent_core.yaml'. These configuration values are injected into runtime memory, configuring database targets, logging levels, and IAM roles without modifying source code.

### Key Responsibilities
- Store secret access credentials locally in '.env' files while keeping them out of Git repositories.
- Declare deployment metadata, entrypoint paths, and execution role ARNs in YAML files.
- Centralize build settings, project metadata, and package dependencies in 'pyproject.toml'.
- Enable seamless transitions between local development, testing, and cloud production environments.

---

## 2. Learning Objectives
By the end of this chapter, you will be able to:
- In this chapter, you will learn how to:
- - Configure local environment variables in a `.env` file.
- - Manage dependencies and metadata in a `pyproject.toml` file.
- - Configure deployment settings in `bedrock_agent_core.yaml`.
- - Enforce security best practices for project configurations.

---

## 3. Prerequisites
* Successful project setup and dependency synchronization from Chapter 6.
* Familiarity with YAML, TOML, and INI configuration formats.

---

## 4. Background Theory
The Twelve-Factor App methodology dictates that configuration parameters (endpoints, resource names, access keys) must be kept separate from application code. This ensures the same codebase can run in development, testing, and production without changes. Committing sensitive keys to source code repos poses severe security risks; env files store local secrets, pyproject.toml defines dependencies, and bedrock_agent_core.yaml configures deployment settings.

---

## 5. Core Concepts
**📦 Technical Term: Environment Variables**

* **Simple Explanation:** Variables defined in the execution environment that configure runtime settings.
* **Why it exists:** Separates secret credentials from the codebase.
* **Where is it used:** AWS access keys loaded from a local `.env` file.

**📦 Technical Term: Metadata File**

* **Simple Explanation:** A settings file declaring parameters like execution entry points and IAM roles.
* **Why it exists:** Configures how the service runs and scales the application container.
* **Where is it used:** The parameters defined in `bedrock_agent_core.yaml`.

**📦 Technical Term: pyproject.toml**

* **Simple Explanation:** The configuration file used to declare build options and packages.
* **Why it exists:** Centralizes python tool settings and dependencies.
* **Where is it used:** Managing packaging options.

---

## 6. Internal Mechanics
1. The application boots and imports `os` and `dotenv`.
2. The dotenv helper reads variables from the local `.env` file and injects them into the shell environment.
3. The YAML parser parses `bedrock_agent_core.yaml` to configure agent parameters.
4. If validation succeeds, the runtime assumes the declared IAM execution role and starts the agent container.

---

## 7. Architecture Overview
The following architectural details outline the components and relationship schemas active in this module:

```mermaid
graph TD
    YAML[bedrock_agent_core.yaml] -->|Parses config| App[AgentCore Application]
    App -->|Connects to| IAM[IAM Role ARN]
    App -->|Invokes| Model[Model Target]
    App -->|Saves state to| Table[DynamoDB Table]
```

---

## 8. Installation & Setup
Verify that your YAML configuration file parses correctly by running:
```bash
python -c "import yaml; print(yaml.safe_load(open('bedrock_agent_core.yaml')))"
```

---

## 9. Configuration
### 1. Environment File `.env`
```ini
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1
```

### 2. Metadata File `bedrock_agent_core.yaml`
```yaml
version: "1.0"
agent:
  name: "bedrock-agent-core-sample"
  entry_point: "src/main.py"
  memory_id: "agentcore-memory-table"
  execution_role_arn: "arn:aws:iam::123456789012:role/AgentCoreExecutionRole"
```

---

## 10. Hands-on Examples

In this section, we analyze the hands-on code implementations for **Configuration Files** step-by-step, explaining the architecture, syntax choices, logic flow, and production patterns across all three implementation tiers.

---

### 1. Simple Implementation Tier Walkthrough

```python
yaml
# Folder Location: agentcore-samples/bedrock_agent_core.yaml

agent_name: "aws_show_and_tell_agent"
entry_point: "src/main.py"
runtime_settings:
  python_version: "3.11"
  execution_role_arn: "arn:aws:iam::123456789012:role/AgentCoreExecutionRole"
  memory_id: "agentcore-memory-user-db-987"
```

#### Code Logic & Syntax Breakdown:
* **Package Imports (`from bedrock_agent_core import ...`)**:
  - Brings in the core `BedrockAgentCoreApp` engine. This class handles runtime container startup, manages the microVM event loop, and deserializes incoming JSON API invocations.
* **Application Instance (`app = BedrockAgentCoreApp()`)**:
  - Instantiates the primary application object `app`. This object serves as the main registry for invocation routes, memory session hooks, and tool bindings.
* **Invocation Decorator (`@app.invoke`)**:
  - A Python decorator that registers the function immediately below as the primary entrypoint for Bedrock AgentCore runtime triggers.
* **Handler Signature (`def handler(payload, context):`)**:
  - **`payload`**: A Python dictionary holding client parameters, user prompt strings, and input arguments.
  - **`context`**: A metadata object containing active runtime details such as `session_id`, `actor_id`, and AWS IAM execution identities.
* **Return Payload (`return {"statusCode": 200, "response": ...}`)**:
  - Constructs a standard HTTP response dictionary. The `statusCode: 200` communicates success to the API Gateway, and `response` delivers the agent payload back to the client.

---

### 2. Intermediate Implementation Tier Walkthrough

```python
# Python script to parse and validate YAML metadata configuration fields
import yaml

def validate_yaml():
    try:
        with open("bedrock_agent_core.yaml", "r") as f:
            config = yaml.safe_load(f)
        agent_cfg = config.get("agent", {})
        print("Agent Name:", agent_cfg.get("name"))
        print("Entrypoint:", agent_cfg.get("entry_point"))
        if not agent_cfg.get("execution_role_arn"):
            print("WARNING: execution_role_arn is missing!")
    except FileNotFoundError:
        print("bedrock_agent_core.yaml file was not found.")

if __name__ == "__main__":
    validate_yaml()
```

#### Code Logic & Syntax Breakdown:
* **System Logging Setup (`import logging` & `logger = logging.getLogger(...)`)**:
  - Configures structured logging via Python's standard `logging` module.
  - In production, log messages emitted by `logger.info()` stream into Amazon CloudWatch Logs for real-time monitoring and debugging.
* **Safe Parameter Extraction (`payload.get(...)`)**:
  - Uses `payload.get("prompt", "")` to safely retrieve user queries. Using `.get()` with a default fallback (`""`) prevents `KeyError` exceptions if optional fields are missing.
* **Runtime Session Inspection (`getattr(context, ...)`)**:
  - Inspects the `context` object for `session_id`. Using `getattr()` ensures compatibility when testing locally without a live AWS microVM context.
* **Operational Telemetry (`logger.info(...)`)**:
  - Emits formatted log entries containing session parameters and query strings to track execution flow.

---

### 3. Advanced Production Tier Walkthrough

```python
# Structured configuration manager class for loading and validating configurations
import os
import yaml
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.agent_config = {}
        self.load_yaml_config()

    def load_yaml_config(self):
        path = "bedrock_agent_core.yaml"
        if os.path.exists(path):
            with open(path, "r") as f:
                self.agent_config = yaml.safe_load(f).get("agent", {})

    def validate(self):
        errors = []
        if not os.getenv("AWS_ACCESS_KEY_ID"):
            errors.append("Missing AWS_ACCESS_KEY_ID in environment.")
        if not self.agent_config.get("execution_role_arn"):
            errors.append("Missing execution_role_arn in bedrock_agent_core.yaml.")
        
        if errors:
            print("[CONFIG ERROR] Validation failed:")
            for err in errors:
                print(f"- {err}")
            return False
        print("[CONFIG OK] Configuration parameters validated successfully.")
        return True

if __name__ == "__main__":
    cfg = ConfigManager()
    cfg.validate()
```

#### Code Logic & Syntax Breakdown:
* **Defensive Error Trapping (`try: ... except Exception as e:`)**:
  - Wraps the entire invocation handler inside a `try-except` block to catch unhandled errors gracefully, preventing container crashes in multi-tenant runtime environments.
* **Input Parameter Validation (`if not prompt:`)**:
  - Inspects inbound arguments before executing core agent logic. If mandatory parameters are missing, it short-circuits execution and returns a structured `statusCode: 400` (Bad Request) payload.
* **Environment Overrides (`os.getenv(...)`)**:
  - Reads system environment variables (e.g., `APP_ENV`) to dynamically adapt behavior across `development`, `staging`, and `production` environments without modifying codebase files.
* **Sanitized Production Error Response**:
  - Logs internal error details using `logger.error(...)` while returning a clean, safe `statusCode: 500` response to prevent internal stack traces from leaking to client callers.

---

### Summary Sequence of Execution

```
[Incoming Invocation] ──► [Bedrock AgentCore Runtime]
                                  │
                                  ▼
                      [Route to @app.invoke Handler]
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
       [Input Validated (200)]        [Input Missing (400)]
                   │                             │
                   ▼                             ▼
       [Execute Agent Core Logic]     [Return Error Payload]
                   │
                   ▼
       [Deliver JSON to Client]
```

---

## 11. Security Considerations
Never commit credentials or private keys to version control. In production, load secrets dynamically from AWS Secrets Manager or Systems Manager Parameter Store rather than using static local files.

---

## 12. Performance Optimization
Cache configuration parameters in memory to avoid repeated disk reads during execution loops.

---

## 13. Common Mistakes
* Committing the `.env` file to Git, exposing access keys in the commit history.
* Defining invalid YAML syntax (like mixed tabs and spaces), causing parser crashes during startup.

---

## 14. Troubleshooting
Below is the diagnostic reference table for identifying and resolving issues:

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| yaml.scanner.ScannerError | Invalid YAML syntax or tab spacing characters used in bedrock_agent_core.yaml. | Use spaces instead of tabs, and validate the file using an online YAML validator. |
| Variables return None on getenv | The .env file was not loaded or does not exist in the working folder. | Call 'load_dotenv()' before fetching environment variables, and verify the file is named exactly '.env'. |

---

## 15. Interview Questions


### Knowledge Verification Check (20 Interactive Quizzes)

<Quiz 
  question="What is the primary role of 07 Configuration Files in Bedrock AgentCore?" 
  options=["To provide hardware-isolated, scalable, and code-first execution for 07 Configuration Files.", "To store plain text credentials in Git repos.", "To run legacy Windows desktop apps.", "To disable security permissions."] 
  answerIndex=0 
  explanation="07 Configuration Files provides enterprise-grade, code-first runtime logic for Bedrock AgentCore." 
/>

<Quiz 
  question="How does Bedrock AgentCore enforce security for 07 Configuration Files?" 
  options=["By sharing memory across all tenants.", "By hosting session runtimes inside isolated AWS Firecracker microVM containers with scoped IAM roles.", "By disabling SSL/TLS encryption.", "By running code as root on public servers."] 
  answerIndex=1 
  explanation="Firecracker microVMs deliver hardware-level security boundaries between multi-tenant executions." 
/>

<Quiz 
  question="Which environment variable loading pattern is recommended for 07 Configuration Files?" 
  options=["Hardcoding values in Python source code files.", "Using os.getenv() or Pydantic BaseSettings to read environment configuration dynamically.", "Storing secrets in public web pages.", "Editing binary files manually."] 
  answerIndex=1 
  explanation="12-Factor App principles mandate decoupling configuration from application source code via environment variables." 
/>

<Quiz 
  question="How should runtime errors be handled in 07 Configuration Files handlers?" 
  options=["Allowing exceptions to crash the container process.", "Wrapping invocation logic in try-except blocks and returning clean structured error payloads (e.g. 400/500 status codes).", "Ignoring all errors completely.", "Printing errors to static HTML files."] 
  answerIndex=1 
  explanation="Defensive error trapping prevents unhandled runtime exceptions from crashing container workers." 
/>

<Quiz 
  question="What key metric should be monitored in CloudWatch for 07 Configuration Files?" 
  options=["Invocation latency, token consumption rates, and HTTP error response counts.", "Monitor resolution of user monitors.", "Keyboard stroke frequency.", "Color contrast ratios."] 
  answerIndex=0 
  explanation="Tracking latency and token usage guarantees cost control and performance optimization in production." 
/>

<Quiz 
  question="How does 07 Configuration Files achieve sub-second scaling during high concurrency?" 
  options=["By leveraging pre-warmed Firecracker microVM snapshots and serverless AWS Fargate clusters.", "By restarting physical servers manually.", "By deleting user databases.", "By restricting app usage to one request per minute."] 
  answerIndex=0 
  explanation="Pre-warmed microVM snapshots enable sub-second boot times under peak traffic spikes." 
/>

<Quiz 
  question="Which IAM action is required to invoke foundation models in 07 Configuration Files?" 
  options=["bedrock:InvokeModel and bedrock:InvokeModelWithResponseStream", "s3:DeleteBucket", "ec2:TerminateInstances", "iam:DeleteUser"] 
  answerIndex=0 
  explanation="The bedrock:InvokeModel permission permits agents to call Bedrock foundation models." 
/>

<Quiz 
  question="Which Python SDK client is used for Amazon Bedrock runtime interactions in 07 Configuration Files?" 
  options=["boto3.client('bedrock-runtime')", "urllib2.open()", "os.system('cmd')", "pandas.read_csv()"] 
  answerIndex=0 
  explanation="Boto3 bedrock-runtime provides low-latency access to foundation model inference endpoints." 
/>

<Quiz 
  question="How is session state maintained across multiple request turns in 07 Configuration Files?" 
  options=["By using unique session identifiers mapped to warm microVMs and persistent DynamoDB memory stores.", "By clearing memory after every line.", "By saving state in browser cookies only.", "Session state cannot be maintained."] 
  answerIndex=0 
  explanation="AgentCore combines sticky microVM routing with persistent database backends for session continuity." 
/>

<Quiz 
  question="Why is Docker multi-stage building recommended for 07 Configuration Files container deployments?" 
  options=["It reduces image file sizes by omitting build dependencies from final production runtime containers.", "It makes Docker containers slower.", "It forces Python to compile to JavaScript.", "It deletes Git version history."] 
  answerIndex=0 
  explanation="Multi-stage Docker builds produce lightweight images, reducing deployment times and attack surfaces." 
/>

<Quiz 
  question="Which tracing standard does Bedrock AgentCore use for end-to-end observability of 07 Configuration Files?" 
  options=["OpenTelemetry (OTel) distributed tracing standards", "Custom print() text files", "Syslog UDP broadcast", "Manual paper logbooks"] 
  answerIndex=0 
  explanation="OpenTelemetry enables distributed trace collection across model calls, memory lookups, and tool executions." 
/>

<Quiz 
  question="What is the recommended solution if 07 Configuration Files returns a 403 Forbidden status during Bedrock invocations?" 
  options=["Verify IAM role policies and confirm foundation model access is enabled in the AWS Bedrock Console.", "Reinstall the operating system.", "Delete the AWS account.", "Use an unencrypted connection."] 
  answerIndex=0 
  explanation="Model access must be explicitly granted in the AWS Bedrock Console before IAM roles can invoke models." 
/>

<Quiz 
  question="What is a primary cause of HTTP 500 errors during 07 Configuration Files execution?" 
  options=["Unhandled exceptions in custom Python tool code or missing required payload keys.", "Network speeds exceeding 1 Gbps.", "Using Python 3.11 instead of Python 2.7.", "High GPU availability."] 
  answerIndex=0 
  explanation="Uncaught exceptions within tool handlers or missing request keys trigger 500 Internal Server errors." 
/>

<Quiz 
  question="Where does 07 Configuration Files fit into the ReAct (Reason + Act) loop pattern?" 
  options=["It executes reasoning steps, structures tool parameters, and processes observations.", "It bypasses the model completely.", "It only runs when offline.", "It formats HTML styling tags."] 
  answerIndex=0 
  explanation="AgentCore coordinates the continuous cycle of LLM reasoning, tool invocation, and observation processing." 
/>

<Quiz 
  question="How can API cost be optimized when operating 07 Configuration Files at high volume?" 
  options=["By caching model responses, optimizing prompt lengths, and choosing appropriate foundation model tiers.", "By sending empty prompts repeatedly.", "By turning off logging.", "By disabling database indexes."] 
  answerIndex=0 
  explanation="Prompt caching and selecting model size according to task complexity drastically cuts inference spending." 
/>

<Quiz 
  question="How does the Memory Engine support long-term retrieval in 07 Configuration Files?" 
  options=["By indexing conversational history and vector embeddings into persistent storage like Amazon DynamoDB or OpenSearch.", "By storing files in temporary RAM.", "By requiring users to re-enter prompts every time.", "Memory Engine is not supported."] 
  answerIndex=0 
  explanation="Vector stores and DynamoDB backing enable long-term semantic memory retrieval across sessions." 
/>

<Quiz 
  question="What role does the API Gateway play in front of 07 Configuration Files?" 
  options=["It provides authentication, rate limiting, request validation, and routing to backend microVM workers.", "It replaces the foundation model.", "It generates synthetic test data.", "It compiles Python code into C."] 
  answerIndex=0 
  explanation="API Gateways secure entry points and shield agent runtime workers from unauthorized or throttled traffic." 
/>

<Quiz 
  question="Why are Firecracker microVMs superior to standard Docker containers for multi-tenant 07 Configuration Files workloads?" 
  options=["They offer minimal virtualization overhead with strict hardware-isolated kernel boundaries between tenant workloads.", "They require 100GB of RAM to start.", "They do not support Linux.", "They are slower than full virtual machines."] 
  answerIndex=0 
  explanation="Firecracker provides VM-grade security with container-grade startup speed and minimal memory footprint." 
/>

<Quiz 
  question="What production antipattern should be strictly avoided when designing 07 Configuration Files?" 
  options=["Hardcoding AWS access keys or maintaining stateless logic without error handling.", "Using virtual environments.", "Writing unit tests for Python code.", "Logging trace events to CloudWatch."] 
  answerIndex=0 
  explanation="Hardcoded credentials and unhandled exceptions are critical antipatterns in production systems." 
/>

<Quiz 
  question="How does 07 Configuration Files integrate with enterprise databases and external APIs?" 
  options=["Through standardized Python tool schemas (e.g. Pydantic models) invoked securely via sandboxed tool registries.", "By exposing database passwords publicly.", "By using manual copy-paste mechanisms.", "External integration is unsupported."] 
  answerIndex=0 
  explanation="Pydantic-defined tools allow foundation models to execute validated API and database calls safely." 
/>

### Q: What is the Twelve-Factor App recommendation for configuration?
* **Answer:** The Twelve-Factor App methodology recommends storing configuration in the environment, separating settings from the codebase. This allows the application to move between environments without modification.

### Q: Why is YAML commonly used for configuration over JSON?
* **Answer:** YAML supports comments, handles multiline strings cleanly, and features a readable syntax without brackets and braces, simplifying configuration management.

### Q: How do you load environment variables in Python?
* **Answer:** Use the `os.getenv('KEY')` method to fetch values, and utilize the `python-dotenv` library's `load_dotenv()` function to load them from a local `.env` file.

---

## 16. Real-World Use Cases
**Enterprise Scenario:** SaaS Multi-Region Legal Document Analysis Engine

* **Business Challenge:** Hardcoded database URIs, API keys, and model identifiers caused accidental staging database overwrites and regional compliance violations during global deployments.
* **Bedrock AgentCore Solution:** Centralizing application settings inside `bedrock_agent_core.yaml` and isolating sensitive API keys and environment overrides inside `.env` files loaded dynamically at runtime.
* **Production Impact:**
  * Enabled seamless deployment of the same container image across US, EU, and APAC AWS regions with zero code changes.
  * Eliminated zero-day security exposures caused by committing sensitive keys to Git repositories.
  * Allowed DevOps teams to modify model execution parameters without rebuilding application containers.

---

## 17. Industrial Project
These configuration files define the environment settings and entry points that authorize and run the application in Chapter 8.

---

<InteractiveExample 
  language="python"
  instruction="Initialization & Runtime Setup for 07 Configuration Files."
  initialCode="# Snippet 1: Testing Bedrock AgentCore Runtime Setup for 07 Configuration Files
import sys
import os

print('=== AgentCore Runtime Init ===')
print('Python Version:', sys.version.split()[0])
print('Agent Module:', '07 Configuration Files')
print('Status: Active & Ready')"
/>

<InteractiveExample 
  language="python"
  instruction="Configuration & Environment Variables for 07 Configuration Files."
  initialCode="# Snippet 2: Validating Environment Configuration for 07 Configuration Files
import json
import os

config = {
    'AWS_REGION': os.getenv('AWS_REGION', 'us-east-1'),
    'MODEL_ID': os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet'),
    'TIMEOUT_SEC': int(os.getenv('TIMEOUT_SEC', '30')),
    'DEBUG_MODE': os.getenv('DEBUG', 'true').lower() == 'true'
}
print('Loaded Configuration:')
print(json.dumps(config, indent=2))"
/>

<InteractiveExample 
  language="python"
  instruction="Defensive Error Handling & Payload Parsing for 07 Configuration Files."
  initialCode="# Snippet 3: Defensive Request Handler for 07 Configuration Files
def process_request(payload):
    try:
        prompt = payload.get('prompt')
        if not prompt:
            return {'statusCode': 400, 'error': 'Prompt parameter is required.'}
        session_id = payload.get('session_id', 'default-session')
        return {'statusCode': 200, 'message': f'Processed prompt for session: {session_id}'}
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

print(process_request({'prompt': 'Execute query', 'session_id': 'sess-102'}))"
/>

<InteractiveExample 
  language="python"
  instruction="Boto3 Bedrock Model Invocation Simulation for 07 Configuration Files."
  initialCode="# Snippet 4: Simulating Foundation Model Inference in 07 Configuration Files
import json

def invoke_claude_model(prompt_text):
    payload = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 1000,
        'messages': [{'role': 'user', 'content': prompt_text}]
    }
    print('Sending payload to Bedrock Converse API for 07 Configuration Files...')
    response = {
        'id': 'msg_01X99',
        'role': 'assistant',
        'content': [{'type': 'text', 'text': f'Agent response generated for input: \"{prompt_text}\"'}]
    }
    return response

res = invoke_claude_model('Summarize system health')
print('Model Response:', res['content'][0]['text'])"
/>

<InteractiveExample 
  language="python"
  instruction="ReAct Reasoning Loop Execution for 07 Configuration Files."
  initialCode="# Snippet 5: ReAct (Reason + Act) Loop Simulation for 07 Configuration Files
def run_react_cycle(user_input):
    print('1. [THOUGHT] Analyzing user query:', user_input)
    print('2. [ACTION] Selected tool: query_system_database')
    observation = {'table': 'logs', 'records_found': 42}
    print('3. [OBSERVATION] Tool output received:', observation)
    print('4. [FINAL ANSWER] Processing complete based on retrieved observation.')

run_react_cycle('Check database log entries')"
/>

<InteractiveExample 
  language="python"
  instruction="Pydantic Tool Registration & Schema Validation for 07 Configuration Files."
  initialCode="# Snippet 6: Pydantic Tool Parameter Validation for 07 Configuration Files
from pydantic import BaseModel, Field

class SystemQuerySchema(BaseModel):
    target_system: str = Field(description='Name of the subsystem to query')
    limit: int = Field(default=10, ge=1, le=100)

def execute_tool(data: SystemQuerySchema):
    print(f'Executing query on {data.target_system} with limit={data.limit}...')
    return {'status': 'success', 'data': ['Item A', 'Item B']}

query = SystemQuerySchema(target_system='AgentCore-Runtime', limit=5)
print('Tool Result:', execute_tool(query))"
/>

<InteractiveExample 
  language="python"
  instruction="MicroVM Session State & Memory Engine for 07 Configuration Files."
  initialCode="# Snippet 7: MicroVM Session & Memory Management in 07 Configuration Files
class SessionMemory:
    def __init__(self):
        self.history = []
    def add_message(self, role, content):
        self.history.append({'role': role, 'content': content})
    def get_context(self):
        return self.history[-3:]

mem = SessionMemory()
mem.add_message('user', 'Hello Agent!')
mem.add_message('assistant', 'How can I assist you?')
mem.add_message('user', 'Show memory status.')
print('Active Memory Context:', mem.get_context())"
/>

<InteractiveExample 
  language="python"
  instruction="OpenTelemetry Tracing & Telemetry Logging for 07 Configuration Files."
  initialCode="# Snippet 8: OpenTelemetry Trace Event Simulation for 07 Configuration Files
import time

def log_otel_span(span_name, duration_ms, status_code='OK'):
    telemetry_record = {
        'trace_id': '0x4bf92f3577b34da6a3ce929d0e0e4736',
        'span_id': '0x00f067aa0ba902b7',
        'name': span_name,
        'duration_ms': duration_ms,
        'attributes': {
            'http.status_code': 200,
            'agent.module': '07 Configuration Files'
        }
    }
    print(f'[OTel Span Event] {span_name} executed in {duration_ms}ms ({status_code})')
    return telemetry_record

log_otel_span('07 Configuration Files_Invocation', 142)"
/>

<InteractiveExample 
  language="python"
  instruction="Docker Container Health Check Simulation for 07 Configuration Files."
  initialCode="# Snippet 9: Container MicroVM Health Status for 07 Configuration Files
def check_container_health():
    status = {
        'container_id': 'firecracker-uvm-9901',
        'health': 'HEALTHY',
        'memory_allocated_mb': 512,
        'cpu_usage_pct': 4.2,
        'active_connections': 1
    }
    print('MicroVM Runtime Status:')
    for k, v in status.items():
        print(f'  - {k}: {v}')

check_container_health()"
/>

<InteractiveExample 
  language="python"
  instruction="End-to-End Execution Pipeline Test for 07 Configuration Files."
  initialCode="# Snippet 10: Complete End-to-End Pipeline Execution for 07 Configuration Files
def run_full_pipeline(input_prompt):
    print(f'1. Gateway: Received request \"{input_prompt}\"')
    print('2. Identity: Authenticated IAM session role')
    print('3. Runtime: Allocated Firecracker MicroVM container')
    print('4. Execution: Model invoked ReAct reasoning loop')
    print('5. Response: 200 OK returned to client')
    return {'status': 'SUCCESS', 'result': 'Pipeline completed.'}

print(run_full_pipeline('Run complete diagnostic check'))"
/>

## 18. Summary
This chapter detailed how to manage application settings across environments using `bedrock_agent_core.yaml` for deployment parameters and `.env` files for local environment variables and sensitive credentials.

Key architectural insights and practical lessons learned in this chapter include:
* **Decoupling Configuration from Code:** Separating application logic from environment configuration simplifies multi-region and multi-environment deployments.
* **Credential Protection & `.gitignore`:** Environment files containing sensitive keys or local overrides must always be excluded from Git repositories to prevent credential leaks.
* **Boot-Time Validation:** Validating configuration schemas during container startup ensures early detection of missing or invalid environment variables.

By implementing strict configuration management, you guarantee secure key handling, seamless multi-environment deployments, and operational flexibility.

---

## 19. Practice Exercises
* Beginner: Add `LOG_LEVEL=DEBUG` to `.env` and read it in a Python script.
* Intermediate: Configure `bedrock_agent_core.yaml` to reference a different IAM Role ARN and verify parsing.

---

## 20. Further Reading
* [The Twelve-Factor App - Config](https://12factor.net/config)
* [YAML Specification Guide](https://yaml.org/spec/)
