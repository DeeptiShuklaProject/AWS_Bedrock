# 11_Chapter_gateway

## 1. Introduction
The Tool Gateway routes request payloads to databases and external APIs securely.

> **Analogy:** Think of a secure bank teller window. The teller window (Gateway) acts as a physical barrier. The customer (LLM) passes structured requests (MCP Schemas) through the tray, and the teller executes the transaction.

---

## 2. Learning Objectives
By the end of this chapter, you will be able to:
- In this chapter, you will learn:
- - The role of the AgentCore Gateway as an API broker.
- - How the Model Context Protocol (MCP) standardizes tool routing.
- - How to configure tool gateways using JSON settings files.
- - How semantic tool routing reduces prompt tokens and latency.

---

## 3. Prerequisites
* Configured local endpoints and AWS credentials from Chapters 3 and 8.
* Familiarity with JSON schema definitions.

---

## 4. Background Theory
Models can only process and generate text; they cannot access databases or run code directly. Integrating tools extends their capabilities. However, exposing APIs directly to LLMs risks SQL injection attacks. A tool gateway acts as a secure broker. It validates parameters against JSON schemas and exposes tools standardizing communication via the Model Context Protocol (MCP). Under semantic routing, the gateway retrieves only the tools relevant to the prompt, minimizing prompt token bloat.

---

## 5. Core Concepts
**📦 Technical Term: MCP**

* **Simple Explanation:** An open protocol standardizing communication between AI agents and external tools.
* **Why it exists:** Simplifies integrations across services.
* **Where is it used:** Defining tools in gateway configuration files.

**📦 Technical Term: Tool Gateway**

* **Simple Explanation:** An API broker routing model requests to downstream functions.
* **Why it exists:** Centralizes security, logging, and rate limiting.
* **Where is it used:** The gateway routing interface.

**📦 Technical Term: Semantic Routing**

* **Simple Explanation:** Selecting relevant tools based on prompt meaning rather than keyword matches.
* **Why it exists:** Minimizes prompt token usage and cost.
* **Where is it used:** Filtering active tools.

---

## 6. Internal Mechanics
1. Client submits a prompt to the agent.
2. The agent queries semantic routing to locate relevant tools.
3. The gateway validates the tool request schema.
4. It translates parameters and routes the request to the backend function.
5. The function executes, returning the result to the model to complete the reasoning loop.

---

## 7. Architecture Overview
The following architectural details outline the components and relationship schemas active in this module:

```mermaid
graph LR
    Agent[Agent Reasoning] -->|MCP Request| Gateway[Tool Gateway]
    Gateway -->|Route| DB[Database Server]
    Gateway -->|Route| API[External Web APIs]
    Gateway -->|Route| Lambda[AWS Lambda Functions]
```

---

## 8. Installation & Setup
Inspect active gateway server configurations using the CLI:
```bash
agentcore gateway list
```

---

## 9. Configuration
Define registered tools in the `gateway_config.json` configuration file:
```json
{
  "tools": [
    {
      "name": "fetch_stock_level",
      "description": "Check active warehouse stock counts for a product SKU.",
      "parameters": {
        "type": "object",
        "properties": {
          "sku": {"type": "string", "description": "Product identifier"}
        },
        "required": ["sku"]
      }
    }
  ]
}
```

---

## 10. Hands-on Examples
### Simple Example
```python
json
{
  "gatewayName": "enterprise-tool-gateway",
  "mcpServers": {
    "database-tools": {
      "type": "lambda",
      "functionArn": "arn:aws:lambda:us-east-1:123456789012:function:DatabaseToolExecutor",
      "tools": [
        {
          "name": "lookup_customer_profile",
          "description": "Lookup customer tier, registration date, and email by customer ID.",
          "inputSchema": {
            "type": "object",
            "properties": {
              "customer_id": {
                "type": "string",
                "description": "The unique 6-digit customer identifier."
              }
            },
            "required": ["customer_id"]
          }
        }
      ]
    }
  }
}
```

### Intermediate Example
```python
# Python script to validate input arguments against registered JSON schemas
from jsonschema import validate, ValidationError

tool_schema = {
    "type": "object",
    "properties": {
        "sku": {"type": "string", "pattern": "^[A-Z]{3}-[0-9]{3}$"}
    },
    "required": ["sku"]
}

def validate_arguments(args):
    try:
        validate(instance=args, schema=tool_schema)
        print("[OK] Arguments validated successfully!")
        return True
    except ValidationError as e:
        print("[FAIL] Validation error:", e.message)
        return False

if __name__ == "__main__":
    validate_arguments({"sku": "ABC-123"}) # Valid
    validate_arguments({"sku": "invalid"}) # Invalid
```

### Advanced Example
```python
# Complete mock gateway router resolving dynamic tool execution requests
import json

class MockGatewayRouter:
    def __init__(self):
        self.tool_registry = {}

    def register(self, name, func):
        self.tool_registry[name] = func

    def route_request(self, tool_name, arguments_json):
        if tool_name not in self.tool_registry:
            return {"success": False, "error": f"Tool '{tool_name}' not found."}
        try:
            args = json.loads(arguments_json)
            # Execute target function
            res = self.tool_registry[tool_name](**args)
            return {"success": True, "output": res}
        except Exception as e:
            return {"success": False, "error": str(e)}

def mock_db_lookup(sku):
    db = {"SHI-001": "12 units in stock", "PAN-002": "Out of stock"}
    return db.get(sku, "SKU not found.")

if __name__ == "__main__":
    router = MockGatewayRouter()
    router.register("fetch_stock_level", mock_db_lookup)
    print(router.route_request("fetch_stock_level", '{"sku": "SHI-001"}'))
```

---

## 11. Code Walkthrough
Let's perform a line-by-line code walk of the core logic implementation:

```python
json
{
  "gatewayName": "enterprise-tool-gateway",
  "mcpServers": {
    "database-tools": {
      "type": "lambda",
      "functionArn": "arn:aws:lambda:us-east-1:123456789012:function:DatabaseToolExecutor",
      "tools": [
        {
          "name": "lookup_customer_profile",
          "description": "Lookup customer tier, registration date, and email by customer ID.",
          "inputSchema": {
            "type": "object",
            "properties": {
              "customer_id": {
                "type": "string",
                "description": "The unique 6-digit customer identifier."
              }
            },
            "required": ["customer_id"]
          }
        }
      ]
    }
  }
}
```

* **`import` statements:** Load libraries and core modules required by the package.
* **Initialization:** Instantiates execution frameworks and logs operational events.
* **Handler logic:** Executes input validations and triggers core business routines.

---

## 12. Production Best Practices
* Define clear descriptions in schemas to guide model selection.
* Apply strict schemas to protect backend APIs from malformed parameters.
* Route calls through private connections to secure network traffic.

---

## 13. Security Considerations
Enforce IAM boundary limits on gateway execution roles. Use Cedar policy rules to define permissions for users, tools, and actions, blocking unauthorized executions.

---

## 14. Performance Optimization
Utilize semantic routing to minimize the number of tool schemas appended to prompts, optimizing latency and reducing costs.

---

## 15. Cost Optimization
Monitor token usage associated with tool definitions. Long tool descriptions increase input token usage, inflating overall execution costs.

---

## 16. Common Mistakes
* Defining ambiguous tool descriptions, causing models to select the wrong tool.
* Committing API secret keys inside tool execution scripts instead of retrieving them dynamically.

---

## 17. Troubleshooting
Below is the diagnostic reference table for identifying and resolving issues:

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| Model invokes wrong tool during run | Ambiguous descriptions inside the gateway configuration schema. | Clarify description text to guide the model's reasoning loop. |
| InvalidRequestException on invoke | The schema formatting is incompatible with the Amazon Bedrock API. | Verify configurations align with JSON schema formatting standards. |

---

## 18. Interview Questions
### Q: What is the advantage of using Model Context Protocol (MCP)?
* **Answer:** MCP standardizes integrations by decoupling clients from specific database API formats, providing a uniform schema for tool communication.

### Q: How does semantic tool routing optimize prompt sizes?
* **Answer:** Semantic routing filters tool lists to only append schemas relevant to the query, reducing prompt token bloat and lowering costs.

### Q: How do you secure tool calls from SQL injection attacks?
* **Answer:** Verify input arguments against strict parameter schemas, and use parameterized queries in backend database drivers to block injection vectors.

---

## 19. Real-World Use Cases
Integrating customer database lookups securely into customer service workflows.

---

## 20. Industrial Project
This gateway acts as the integration point that allows our agent to invoke database tools and Lambda functions.

---

## 21. Summary
This chapter covered the Tool Gateway architecture, the Model Context Protocol (MCP), and configuring tool schemas in `gateway_config.json`.

---

## 22. Key Takeaways
* Expose tools using standardized MCP schemas to simplify integrations.
* Leverage semantic routing to minimize prompt token usage.
* Validate input arguments against strict schemas to secure backend APIs.

---

## 23. Practice Exercises
* Beginner: Write a JSON schema definition for a tool that retrieves weather updates by city.
* Intermediate: Add validation checks to reject city strings containing numeric characters.

---

## 24. Further Reading
* [Model Context Protocol Specification](https://modelcontextprotocol.io/)
* [JSON Schema Standard Reference](https://json-schema.org/)
