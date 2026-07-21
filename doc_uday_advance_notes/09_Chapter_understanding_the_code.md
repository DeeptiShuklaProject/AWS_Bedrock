# 09_Chapter_understanding_the_code

## 1. Introduction
Analyzing the implementation details of the main application file is key to customizing agent execution logic.

> **Analogy:** Think of a factory assembly line. The conveyor belt (the SDK wrapper) moves products, and custom assembly machines (handler functions) perform specific modifications on items passing by.

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
### Simple Example
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

### Intermediate Example
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

### Advanced Example
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

---

## 11. Code Walkthrough
Let's perform a line-by-line code walk of the core logic implementation:

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

* **`import` statements:** Load libraries and core modules required by the package.
* **Initialization:** Instantiates execution frameworks and logs operational events.
* **Handler logic:** Executes input validations and triggers core business routines.

---

## 12. Production Best Practices
* Keep handler functions focused on task orchestration; delegate business logic to separate modules.
* Implement clear logging structures to capture both input parameters and execution durations.
* Write unit tests for handler functions by passing mock payload and context arguments.

---

## 13. Security Considerations
Enforce input validation rules on incoming payloads to protect against code injection. Sanitize output responses to ensure sensitive system details are not leaked in error messages.

---

## 14. Performance Optimization
Load large models and database configurations outside the handler function to avoid initialization latency during request loops.

---

## 15. Cost Optimization
Optimize the execution time of code paths inside your handler function. The longer a handler runs, the longer the compute microVM remains active, increasing execution costs.

---

## 16. Common Mistakes
* Initializing heavy client dependencies inside the handler function code, causing latency.
* Accessing payload parameters directly without check validations, causing KeyError crashes if parameters are missing.

---

## 17. Troubleshooting
Below is the diagnostic reference table for identifying and resolving issues:

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| SyntaxError on python run | Invalid syntax or indentations in main.py. | Verify syntax and check that the script compiles: 'python -m py_compile src/main.py'. |
| NameError on app object references | The application object or variable was referenced before initialization. | Verify that the app wrapper object is instantiated: 'app = BedrockAgentCoreApp()' before registering handlers. |

---

## 18. Interview Questions
### Q: What is the benefit of decorating functions with @app.invoke?
* **Answer:** The decorator registers the function as the agent's entrypoint, abstracting web server routing and request parsing so developers can focus on agent logic.

### Q: How do you extract session identifiers inside the handler?
* **Answer:** Extract the `session_id` attribute from the `context` argument: `session_id = getattr(context, 'session_id', 'default')`.

### Q: Why is logging critical inside handler functions?
* **Answer:** Logging captures request payloads, runtime errors, and execution times, providing the details needed to monitor and debug applications.

---

## 19. Real-World Use Cases
Customizing handler functions to route prompts to different agent orchestrators.

---

## 20. Industrial Project
This walkthrough defines the structural template for our main agent script (`src/main.py`) which we will expand in subsequent chapters.

---

## 21. Summary
This chapter analyzed the implementation details of the main application file, including imports, app wrappers, logging, and handlers.

---

## 22. Key Takeaways
* Handlers process incoming request payloads and metadata.
* Python decorators bind routing endpoints to functions.
* Initializing resources at the module level minimizes execution latency.

---

## 23. Practice Exercises
* Beginner: Add a log message that prints the length of the prompt inside the handler.
* Intermediate: Add a custom parameter verification step and return a 400 error status code if validation fails.

---

## 24. Further Reading
* [Clean Code Guide for Python](https://github.com/zedr/clean-code-python)
* [Python Logging Library Guide](https://docs.python.org/3/library/logging.html)
