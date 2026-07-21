# Chapter_09_understanding_the_code

## 1. Introduction
Analyzing the implementation details of the main application file is key to customizing agent execution logic.

### What is it?
Understanding the Code involves analyzing the line-by-line structure and execution flow of the main application script ('src/main.py'), detailing how decorators, handlers, context objects, and response payloads interact.

### Why is it important?
Writing maintainable, enterprise-ready software requires understanding how each line of code functions within the broader framework framework. Knowing how request parameters are extracted, validated, and logged enables developers to extend business logic safely without breaking application structure.

### How does it work?
The script initializes standard logging, instantiates the 'BedrockAgentCoreApp' wrapper class, and decorates a handler function with '@app.invoke'. When a request arrives, the application extracts the JSON payload and context metadata object, passes them to the handler function, executes custom processing steps, and formats the output into a standardized return dictionary.

### Key Responsibilities
- Instantiate core framework app wrappers to manage container request listeners.
- Register routing endpoints to custom Python functions via '@app.invoke' decorators.
- Parse input arguments from 'payload' dictionaries and session details from 'context' objects.
- Output structured JSON dictionary responses containing HTTP status codes and response bodies.

---

## 2. Learning Objectives
By the end of this chapter, you will be able to:
- In this chapter, you will learn how to:
- - Write a custom log formatter class to output structured JSON logs.
- - Enforce variable validation before executing agent requests.
- - Implement connection retry loops with exponential backoff.
- - Trace request flows through code modules using sequence diagrams.

---

## 3. Prerequisites
* Successful repository clone and walkthrough setup from Chapters 4 and 5.
* Basic familiarity with Python logging libraries.

---

## 4. Background Theory
Enterprise applications utilize clean code architectures to decouple framework code from custom business logic. Bedrock AgentCore separates container routing configurations from the agent's reasoning loop. The handler accepts request payloads and context metadata, coordinates database calls, and formats response payloads, making the codebase easier to test and maintain.

---

## 5. Core Concepts
**📦 Technical Term: SDK Wrapper**

* **Simple Explanation:** A library class that abstracts container lifecycle hooks and request routing details.
* **Why it exists:** Simplifies web listener configuration and request handling.
* **Where is it used:** The `BedrockAgentCoreApp` class.

**📦 Technical Term: Decorator**

* **Simple Explanation:** A design pattern that extends function behavior without modifying the function's code.
* **Why it exists:** Registers handlers with framework routers.
* **Where is it used:** The `@app.invoke` decorator.

**📦 Technical Term: Execution Context**

* **Simple Explanation:** An object containing metadata parameters injected by the runtime environment.
* **Why it exists:** Provides execution details like session IDs and user scopes.
* **Where is it used:** The `context` handler parameter.

---

## 6. Internal Mechanics
1. The main entrypoint initializes logging configurations.
2. It instantiates the application class `BedrockAgentCoreApp()`.
3. The `@app.invoke` decorator registers the decorated handler function in the application's route registry.
4. When a request is received, the application extracts the JSON body and routes it to the handler.
5. The handler executes, returning a dictionary that is serialized into an HTTP response.

---

## 7. Architecture Overview
The following architectural details outline the components and relationship schemas active in this module:

```mermaid
graph TD
    AppInit[app = BedrockAgentCoreApp] -->|Decorator| Reg[@app.invoke]
    Reg -->|Registers| Handler[my_agent_handler]
    Handler -->|Extracts| Prompt[payload.get('prompt')]
    Handler -->|Extracts| Session[context.session_id]
    Handler -->|Returns| Response[statusCode, response]
```

---

## 8. Installation & Setup
Ensure that your main entrypoint file is located at `src/main.py` and is importable:
```bash
python -m py_compile src/main.py
```

---

## 9. Configuration
Configure the agent's entrypoint path in `bedrock_agent_core.yaml` to ensure the runtime can locate your handler:
```yaml
agent:
  entry_point: "src/main.py"
```

---

## 10. Hands-on Examples

In this section, we analyze the hands-on code implementations for **Understanding the Code** step-by-step, explaining the architecture, syntax choices, logic flow, and production patterns across all three implementation tiers.

---

### 1. Simple Implementation Tier Walkthrough

```python
# File: src/agent.py
# Folder Location: agentcore-samples/src/agent.py

import os
import sys
import logging
import json
import time
from typing import Dict, Any
from bedrock_agent_core import BedrockAgentCoreApp

# =====================================================================
# 1. Structured JSON Logging Setup
# =====================================================================
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "session_id"):
            log_record["session_id"] = record.session_id
        return json.dumps(log_record)

logger = logging.getLogger("ProductionAgent")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# =====================================================================
# 2. App Wrapper and Environment Validator
# =====================================================================
app = BedrockAgentCoreApp()

class ConfigValidator:
    @staticmethod
    def validate_env() -> Dict[str, str]:
        required_vars = ["AWS_REGION", "BEDROCK_MODEL_ID"]
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            os.environ["AWS_REGION"] = "us-east-1"
            os.environ["BEDROCK_MODEL_ID"] = "anthropic.claude-3-5-sonnet"
        return {
            "region": os.environ["AWS_REGION"],
            "model_id": os.environ["BEDROCK_MODEL_ID"]
        }

# =====================================================================
# 3. Core Agent Logic with Exponential Backoff
# =====================================================================
class ProductionAgent:
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def execute_with_retry(self, prompt: str, session_id: str, retries: int = 3) -> str:
        extra_log = {"session_id": session_id}
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Attempt {attempt}/{retries}: Invoking Bedrock Model {self.config['model_id']}", extra=extra_log)
                
                # In production, call the Bedrock runtime API here
                return f"[Production Response] Processed: '{prompt}' using {self.config['model_id']}"
                
            except (ConnectionError, TimeoutError) as e:
                logger.warning(f"Connection error: {str(e)}", extra=extra_log)
                if attempt == retries:
                    raise e
                time.sleep(0.5 * attempt)
            except Exception as e:
                logger.error(f"Execution error: {str(e)}", extra=extra_log)
                raise e

# =====================================================================
# 4. Handler Endpoint
# =====================================================================
@app.invoke
def invoke_handler(payload: Dict[str, Any], context: Any) -> Dict[str, Any]:
    session_id = getattr(context, "session_id", "session-unknown")
    extra_log = {"session_id": session_id}
    
    if not payload or "prompt" not in payload:
        logger.error("Invalid payload structure. Prompt key missing.", extra=extra_log)
        return {
            "statusCode": 400,
            "error": "Bad Request",
            "message": "Parameter 'prompt' is missing."
        }
        
    try:
        config = ConfigValidator.validate_env()
        agent = ProductionAgent(config)
        result = agent.execute_with_retry(payload["prompt"], session_id)
        return {
            "statusCode": 200,
            "response": result
        }
    except Exception as e:
        logger.critical(f"Unhandled failure: {str(e)}", extra=extra_log)
        return {
            "statusCode": 500,
            "error": "Internal Error",
            "message": str(e)
        }
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
# Handler logging request details and validating parameters
from bedrock_agent_core import BedrockAgentCoreApp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AppHandler")
app = BedrockAgentCoreApp()

@app.invoke
def handler(payload, context):
    logger.info("Received invocation request.")
    prompt = payload.get("prompt")
    if not prompt:
        return {"statusCode": 400, "response": "Missing 'prompt' in payload."}
    
    session_id = getattr(context, "session_id", "local-dev")
    logger.info(f"Processing prompt for session: {session_id}")
    return {"statusCode": 200, "response": f"Processed input: '{prompt}'"}
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
# Complete handler simulating model calls and returning structured JSON metadata
from bedrock_agent_core import BedrockAgentCoreApp
import logging
import json

logger = logging.getLogger("ProductionApp")
app = BedrockAgentCoreApp()

@app.invoke
def handle_request(payload, context):
    try:
        prompt = payload.get("prompt", "")
        session_id = getattr(context, "session_id", "local-session")
        logger.info(f"Invoking agent loop for session: {session_id}")
        
        if not prompt.strip():
            return {"statusCode": 400, "response": {"error": "Empty prompt received."}}
            
        # Mock core processing workflow
        response_data = {
            "text": f"Completed processing for prompt: '{prompt}'",
            "tokens_used": len(prompt.split()) * 2,
            "success": True
        }
        
        return {
            "statusCode": 200,
            "response": response_data
        }
    except Exception as e:
        logger.error(f"Execution error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "response": {"error": "Internal Server Error"}
        }
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
Enforce input validation rules on incoming payloads to protect against code injection. Sanitize output responses to ensure sensitive system details are not leaked in error messages.

---

## 12. Performance Optimization
Load large models and database configurations outside the handler function to avoid initialization latency during request loops.

---

## 13. Common Mistakes
* Initializing heavy client dependencies inside the handler function code, causing latency.
* Accessing payload parameters directly without check validations, causing KeyError crashes if parameters are missing.

---

## 14. Troubleshooting
Below is the diagnostic reference table for identifying and resolving issues:

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| SyntaxError on python run | Invalid syntax or indentations in main.py. | Verify syntax and check that the script compiles: 'python -m py_compile src/main.py'. |
| NameError on app object references | The application object or variable was referenced before initialization. | Verify that the app wrapper object is instantiated: 'app = BedrockAgentCoreApp()' before registering handlers. |

---

## 15. Interview Questions


### Knowledge Verification Check (20 Interactive Quizzes)

<Quiz 
  question="What is the primary role of 09 Understanding The Code in Bedrock AgentCore?" 
  options=["To provide hardware-isolated, scalable, and code-first execution for 09 Understanding The Code.", "To store plain text credentials in Git repos.", "To run legacy Windows desktop apps.", "To disable security permissions."] 
  answerIndex=0 
  explanation="09 Understanding The Code provides enterprise-grade, code-first runtime logic for Bedrock AgentCore." 
/>

<Quiz 
  question="How does Bedrock AgentCore enforce security for 09 Understanding The Code?" 
  options=["By sharing memory across all tenants.", "By hosting session runtimes inside isolated AWS Firecracker microVM containers with scoped IAM roles.", "By disabling SSL/TLS encryption.", "By running code as root on public servers."] 
  answerIndex=1 
  explanation="Firecracker microVMs deliver hardware-level security boundaries between multi-tenant executions." 
/>

<Quiz 
  question="Which environment variable loading pattern is recommended for 09 Understanding The Code?" 
  options=["Hardcoding values in Python source code files.", "Using os.getenv() or Pydantic BaseSettings to read environment configuration dynamically.", "Storing secrets in public web pages.", "Editing binary files manually."] 
  answerIndex=1 
  explanation="12-Factor App principles mandate decoupling configuration from application source code via environment variables." 
/>

<Quiz 
  question="How should runtime errors be handled in 09 Understanding The Code handlers?" 
  options=["Allowing exceptions to crash the container process.", "Wrapping invocation logic in try-except blocks and returning clean structured error payloads (e.g. 400/500 status codes).", "Ignoring all errors completely.", "Printing errors to static HTML files."] 
  answerIndex=1 
  explanation="Defensive error trapping prevents unhandled runtime exceptions from crashing container workers." 
/>

<Quiz 
  question="What key metric should be monitored in CloudWatch for 09 Understanding The Code?" 
  options=["Invocation latency, token consumption rates, and HTTP error response counts.", "Monitor resolution of user monitors.", "Keyboard stroke frequency.", "Color contrast ratios."] 
  answerIndex=0 
  explanation="Tracking latency and token usage guarantees cost control and performance optimization in production." 
/>

<Quiz 
  question="How does 09 Understanding The Code achieve sub-second scaling during high concurrency?" 
  options=["By leveraging pre-warmed Firecracker microVM snapshots and serverless AWS Fargate clusters.", "By restarting physical servers manually.", "By deleting user databases.", "By restricting app usage to one request per minute."] 
  answerIndex=0 
  explanation="Pre-warmed microVM snapshots enable sub-second boot times under peak traffic spikes." 
/>

<Quiz 
  question="Which IAM action is required to invoke foundation models in 09 Understanding The Code?" 
  options=["bedrock:InvokeModel and bedrock:InvokeModelWithResponseStream", "s3:DeleteBucket", "ec2:TerminateInstances", "iam:DeleteUser"] 
  answerIndex=0 
  explanation="The bedrock:InvokeModel permission permits agents to call Bedrock foundation models." 
/>

<Quiz 
  question="Which Python SDK client is used for Amazon Bedrock runtime interactions in 09 Understanding The Code?" 
  options=["boto3.client('bedrock-runtime')", "urllib2.open()", "os.system('cmd')", "pandas.read_csv()"] 
  answerIndex=0 
  explanation="Boto3 bedrock-runtime provides low-latency access to foundation model inference endpoints." 
/>

<Quiz 
  question="How is session state maintained across multiple request turns in 09 Understanding The Code?" 
  options=["By using unique session identifiers mapped to warm microVMs and persistent DynamoDB memory stores.", "By clearing memory after every line.", "By saving state in browser cookies only.", "Session state cannot be maintained."] 
  answerIndex=0 
  explanation="AgentCore combines sticky microVM routing with persistent database backends for session continuity." 
/>

<Quiz 
  question="Why is Docker multi-stage building recommended for 09 Understanding The Code container deployments?" 
  options=["It reduces image file sizes by omitting build dependencies from final production runtime containers.", "It makes Docker containers slower.", "It forces Python to compile to JavaScript.", "It deletes Git version history."] 
  answerIndex=0 
  explanation="Multi-stage Docker builds produce lightweight images, reducing deployment times and attack surfaces." 
/>

<Quiz 
  question="Which tracing standard does Bedrock AgentCore use for end-to-end observability of 09 Understanding The Code?" 
  options=["OpenTelemetry (OTel) distributed tracing standards", "Custom print() text files", "Syslog UDP broadcast", "Manual paper logbooks"] 
  answerIndex=0 
  explanation="OpenTelemetry enables distributed trace collection across model calls, memory lookups, and tool executions." 
/>

<Quiz 
  question="What is the recommended solution if 09 Understanding The Code returns a 403 Forbidden status during Bedrock invocations?" 
  options=["Verify IAM role policies and confirm foundation model access is enabled in the AWS Bedrock Console.", "Reinstall the operating system.", "Delete the AWS account.", "Use an unencrypted connection."] 
  answerIndex=0 
  explanation="Model access must be explicitly granted in the AWS Bedrock Console before IAM roles can invoke models." 
/>

<Quiz 
  question="What is a primary cause of HTTP 500 errors during 09 Understanding The Code execution?" 
  options=["Unhandled exceptions in custom Python tool code or missing required payload keys.", "Network speeds exceeding 1 Gbps.", "Using Python 3.11 instead of Python 2.7.", "High GPU availability."] 
  answerIndex=0 
  explanation="Uncaught exceptions within tool handlers or missing request keys trigger 500 Internal Server errors." 
/>

<Quiz 
  question="Where does 09 Understanding The Code fit into the ReAct (Reason + Act) loop pattern?" 
  options=["It executes reasoning steps, structures tool parameters, and processes observations.", "It bypasses the model completely.", "It only runs when offline.", "It formats HTML styling tags."] 
  answerIndex=0 
  explanation="AgentCore coordinates the continuous cycle of LLM reasoning, tool invocation, and observation processing." 
/>

<Quiz 
  question="How can API cost be optimized when operating 09 Understanding The Code at high volume?" 
  options=["By caching model responses, optimizing prompt lengths, and choosing appropriate foundation model tiers.", "By sending empty prompts repeatedly.", "By turning off logging.", "By disabling database indexes."] 
  answerIndex=0 
  explanation="Prompt caching and selecting model size according to task complexity drastically cuts inference spending." 
/>

<Quiz 
  question="How does the Memory Engine support long-term retrieval in 09 Understanding The Code?" 
  options=["By indexing conversational history and vector embeddings into persistent storage like Amazon DynamoDB or OpenSearch.", "By storing files in temporary RAM.", "By requiring users to re-enter prompts every time.", "Memory Engine is not supported."] 
  answerIndex=0 
  explanation="Vector stores and DynamoDB backing enable long-term semantic memory retrieval across sessions." 
/>

<Quiz 
  question="What role does the API Gateway play in front of 09 Understanding The Code?" 
  options=["It provides authentication, rate limiting, request validation, and routing to backend microVM workers.", "It replaces the foundation model.", "It generates synthetic test data.", "It compiles Python code into C."] 
  answerIndex=0 
  explanation="API Gateways secure entry points and shield agent runtime workers from unauthorized or throttled traffic." 
/>

<Quiz 
  question="Why are Firecracker microVMs superior to standard Docker containers for multi-tenant 09 Understanding The Code workloads?" 
  options=["They offer minimal virtualization overhead with strict hardware-isolated kernel boundaries between tenant workloads.", "They require 100GB of RAM to start.", "They do not support Linux.", "They are slower than full virtual machines."] 
  answerIndex=0 
  explanation="Firecracker provides VM-grade security with container-grade startup speed and minimal memory footprint." 
/>

<Quiz 
  question="What production antipattern should be strictly avoided when designing 09 Understanding The Code?" 
  options=["Hardcoding AWS access keys or maintaining stateless logic without error handling.", "Using virtual environments.", "Writing unit tests for Python code.", "Logging trace events to CloudWatch."] 
  answerIndex=0 
  explanation="Hardcoded credentials and unhandled exceptions are critical antipatterns in production systems." 
/>

<Quiz 
  question="How does 09 Understanding The Code integrate with enterprise databases and external APIs?" 
  options=["Through standardized Python tool schemas (e.g. Pydantic models) invoked securely via sandboxed tool registries.", "By exposing database passwords publicly.", "By using manual copy-paste mechanisms.", "External integration is unsupported."] 
  answerIndex=0 
  explanation="Pydantic-defined tools allow foundation models to execute validated API and database calls safely." 
/>

### Q: What is the benefit of decorating functions with @app.invoke?
* **Answer:** The decorator registers the function as the agent's entrypoint, abstracting web server routing and request parsing so developers can focus on agent logic.

### Q: How do you extract session identifiers inside the handler?
* **Answer:** Extract the `session_id` attribute from the `context` argument: `session_id = getattr(context, 'session_id', 'default')`.

### Q: Why is logging critical inside handler functions?
* **Answer:** Logging captures request payloads, runtime errors, and execution times, providing the details needed to monitor and debug applications.

---

## 16. Real-World Use Cases
**Enterprise Scenario:** Logistics & Fleet Dispatch Optimization Network

* **Business Challenge:** Developers struggled to handle complex edge cases (such as missing GPS coordinates or API timeouts) inside agent response handlers, resulting in system crashes.
* **Bedrock AgentCore Solution:** Implementing robust entrypoint decorators (`@app.invoke`), defensive parameter extraction (`payload.get`), runtime context inspection, and sanitized error responses (`statusCode: 500`).
* **Production Impact:**
  * Achieved 99.99% uptime for automated dispatch agents handling over 100,000 daily delivery requests.
  * Eliminated unhandled exception crashes by returning structured HTTP status code error payloads.
  * Improved diagnostic logging visibility for operational failures in dispatch workflows.

---

## 17. Industrial Project
This walkthrough defines the structural template for our main agent script (`src/main.py`) which we will expand in subsequent chapters.

---

<InteractiveExample 
  language="python"
  instruction="Initialization & Runtime Setup for 09 Understanding The Code."
  initialCode="# Snippet 1: Testing Bedrock AgentCore Runtime Setup for 09 Understanding The Code
import sys
import os

print('=== AgentCore Runtime Init ===')
print('Python Version:', sys.version.split()[0])
print('Agent Module:', '09 Understanding The Code')
print('Status: Active & Ready')"
/>

<InteractiveExample 
  language="python"
  instruction="Configuration & Environment Variables for 09 Understanding The Code."
  initialCode="# Snippet 2: Validating Environment Configuration for 09 Understanding The Code
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
  instruction="Defensive Error Handling & Payload Parsing for 09 Understanding The Code."
  initialCode="# Snippet 3: Defensive Request Handler for 09 Understanding The Code
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
  instruction="Boto3 Bedrock Model Invocation Simulation for 09 Understanding The Code."
  initialCode="# Snippet 4: Simulating Foundation Model Inference in 09 Understanding The Code
import json

def invoke_claude_model(prompt_text):
    payload = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 1000,
        'messages': [{'role': 'user', 'content': prompt_text}]
    }
    print('Sending payload to Bedrock Converse API for 09 Understanding The Code...')
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
  instruction="ReAct Reasoning Loop Execution for 09 Understanding The Code."
  initialCode="# Snippet 5: ReAct (Reason + Act) Loop Simulation for 09 Understanding The Code
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
  instruction="Pydantic Tool Registration & Schema Validation for 09 Understanding The Code."
  initialCode="# Snippet 6: Pydantic Tool Parameter Validation for 09 Understanding The Code
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
  instruction="MicroVM Session State & Memory Engine for 09 Understanding The Code."
  initialCode="# Snippet 7: MicroVM Session & Memory Management in 09 Understanding The Code
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
  instruction="OpenTelemetry Tracing & Telemetry Logging for 09 Understanding The Code."
  initialCode="# Snippet 8: OpenTelemetry Trace Event Simulation for 09 Understanding The Code
import time

def log_otel_span(span_name, duration_ms, status_code='OK'):
    telemetry_record = {
        'trace_id': '0x4bf92f3577b34da6a3ce929d0e0e4736',
        'span_id': '0x00f067aa0ba902b7',
        'name': span_name,
        'duration_ms': duration_ms,
        'attributes': {
            'http.status_code': 200,
            'agent.module': '09 Understanding The Code'
        }
    }
    print(f'[OTel Span Event] {span_name} executed in {duration_ms}ms ({status_code})')
    return telemetry_record

log_otel_span('09 Understanding The Code_Invocation', 142)"
/>

<InteractiveExample 
  language="python"
  instruction="Docker Container Health Check Simulation for 09 Understanding The Code."
  initialCode="# Snippet 9: Container MicroVM Health Status for 09 Understanding The Code
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
  instruction="End-to-End Execution Pipeline Test for 09 Understanding The Code."
  initialCode="# Snippet 10: Complete End-to-End Pipeline Execution for 09 Understanding The Code
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
This chapter performed a deep-dive analysis of handler implementation details, examining how incoming payloads are received, how defensive error handling is applied, and how structured JSON responses are returned to callers.

Key architectural insights and practical lessons learned in this chapter include:
* **Payload & Metadata Extraction:** Handlers receive client prompts inside `payload` and runtime details inside `context`, requiring defensive parameter parsing (`payload.get`).
* **Decorator-Based Event Routing:** Python decorators bind incoming container events directly to handler functions, maintaining a clean event-driven architecture.
* **Defensive Error Handling:** Wrapping core logic in `try-except` blocks ensures that unhandled exceptions produce sanitized HTTP error responses rather than container crashes.

Writing clean, defensive handler code ensures high availability, reliable error reporting, and robust operational stability for production agent services.

---

## 19. Practice Exercises
* Beginner: Add a log message that prints the length of the prompt inside the handler.
* Intermediate: Add a custom parameter verification step and return a 400 error status code if validation fails.

---

## 20. Further Reading
* [Clean Code Guide for Python](https://github.com/zedr/clean-code-python)
* [Python Logging Library Guide](https://docs.python.org/3/library/logging.html)
