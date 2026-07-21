import os
import glob
import re

bedrock_dir = r"c:\Users\nishu\workspace\wscs_bedrock\doc_uday_bedrock_notes"

chapter_data = {
    "Chapter_01_introduction_to_bedrock_agentcore": {
        "playground": {
            "instruction": "Test a simulated Bedrock AgentCore runtime reasoning step in Python.",
            "code": """import sys
import json

print("Initializing Bedrock AgentCore Runtime Environment...")

def simulate_agent_reasoning(user_prompt):
    print(f"[AgentCore MicroVM] Received prompt: '{user_prompt}'")
    reasoning_step = {
        "status": "success",
        "container_id": "firecracker-microvm-001",
        "action": "invoke_foundation_model",
        "model": "anthropic.claude-3-5-sonnet",
        "result": "Agent reasoning loop initialized safely inside hardware boundary."
    }
    return reasoning_step

response = simulate_agent_reasoning("Execute multi-step data query")
print(json.dumps(response, indent=2))"""
        },
        "quizzes": [
            {
                "question": "What is the primary role of AWS Firecracker microVMs in Bedrock AgentCore?",
                "options": [
                    "To store long-term vector embeddings",
                    "To provide hardware-isolated lightweight containers for safe multi-tenant code and agent execution",
                    "To translate SQL queries to GraphQL",
                    "To manage AWS billing accounts"
                ],
                "answerIndex": 1,
                "explanation": "AWS Firecracker microVMs provide hardware-level isolation and rapid boot times, preventing multi-tenant data leakage and execution interference."
            },
            {
                "question": "How does Bedrock AgentCore differ from console-based Bedrock Agents?",
                "options": [
                    "Bedrock AgentCore is code-first and containerized, giving developers full control over agent logic and Python frameworks.",
                    "AgentCore cannot execute Python code.",
                    "Console-based Bedrock Agents require raw C++ code.",
                    "AgentCore only supports static prompts without tools."
                ],
                "answerIndex": 0,
                "explanation": "AgentCore is code-first and framework-agnostic, allowing developers to write custom agent loops using frameworks like LangChain or CrewAI."
            },
            {
                "question": "Which foundation model provider is natively supported within Bedrock AgentCore loops?",
                "options": [
                    "Anthropic Claude models via Amazon Bedrock Converse API",
                    "Local text files only",
                    "Browser extension scripts",
                    "No AI models are supported"
                ],
                "answerIndex": 0,
                "explanation": "Bedrock AgentCore leverages Amazon Bedrock APIs to connect with models such as Anthropic Claude 3.5 Sonnet."
            }
        ]
    },
    "Chapter_02_prerequisites": {
        "playground": {
            "instruction": "Verify your local Python 3.11+ environment and package manager setup.",
            "code": """import sys
import os
import platform

print("=== Environment Verification ===")
print(f"Python Version: {platform.python_version()}")
print(f"OS Platform: {platform.system()} {platform.release()}")
print(f"Architecture: {platform.machine()}")

# Check environment
print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV", "None (System Python)"))
print("Environment checks passed!")"""
        },
        "quizzes": [
            {
                "question": "Why is Python 3.11+ specifically recommended for Bedrock AgentCore development?",
                "options": [
                    "It introduces performance improvements and asynchronous features required for fast agent runtime execution.",
                    "Python 3.11 is the only version with HTML support.",
                    "Older versions cannot run Docker containers.",
                    "Python 3.11 removes the need for AWS credentials."
                ],
                "answerIndex": 0,
                "explanation": "Python 3.11+ provides substantial speedups, improved tracebacks, and enhanced async task handling critical for agent workloads."
            },
            {
                "question": "What is the primary advantage of using `uv` over standard `pip` for dependency management?",
                "options": [
                    "It compiles Python code to C automatically.",
                    "It is written in Rust and offers 10x-100x faster package resolution and installation.",
                    "It bypasses PyPI security checks.",
                    "It replaces Docker containers."
                ],
                "answerIndex": 1,
                "explanation": "`uv` is an extremely fast Python package manager written in Rust, significantly accelerating installation and virtual environment management."
            }
        ]
    },
    "Chapter_03_aws_configuration": {
        "playground": {
            "instruction": "Test AWS Boto3 Bedrock client instantiation and credential check.",
            "code": """import boto3
from botocore.exceptions import NoCredentialsError

def test_aws_bedrock_connection():
    print("Testing Boto3 Bedrock Client Configuration...")
    try:
        # Create Bedrock client
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        print("Bedrock Runtime client successfully instantiated!")
        return True
    except NoCredentialsError:
        print("AWS Credentials not found. Run 'aws configure' in terminal.")
        return False
    except Exception as e:
        print(f"Configuration test note: {e}")
        return True

test_aws_bedrock_connection()"""
        },
        "quizzes": [
            {
                "question": "Which AWS IAM permission policy is required for an agent to invoke foundation models?",
                "options": [
                    "AmazonBedrockFullAccess or bedrock:InvokeModel",
                    "AdministratorAccess-AWSElasticBeanstalk",
                    "AmazonS3ReadOnlyAccess",
                    "AmazonEC2FullAccess"
                ],
                "answerIndex": 0,
                "explanation": "The `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` permissions allow agents to invoke foundation models."
            },
            {
                "question": "Where should AWS credentials never be stored in a production codebase?",
                "options": [
                    "In AWS Secrets Manager",
                    "Hardcoded as plain text inside Python scripts or Git repository files",
                    "In IAM Roles for EC2/ECS tasks",
                    "In environment variables passed securely at runtime"
                ],
                "answerIndex": 1,
                "explanation": "Hardcoding credentials in scripts poses severe security risks and can leak sensitive access keys to version control systems."
            }
        ]
    },
    "Chapter_04_clone_repository": {
        "playground": {
            "instruction": "Simulate git repository verification and branch checking script.",
            "code": """import subprocess
import os

def check_git_status():
    print("Checking Git Repository Status...")
    try:
        res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        print("Git Status Output:")
        print(res.stdout if res.stdout else "Clean working directory.")
    except Exception as e:
        print(f"Git check error: {e}")

check_git_status()"""
        },
        "quizzes": [
            {
                "question": "What is the recommended Git branch workflow when working on Bedrock AgentCore development?",
                "options": [
                    "Commit directly to main without testing",
                    "Create feature branches (e.g. feature/agent-tools) and merge via pull requests",
                    "Never use branches",
                    "Delete .git directory before running"
                ],
                "answerIndex": 1,
                "explanation": "Feature branch workflows ensure code isolation, systematic review, and stable integration before merging into main branches."
            }
        ]
    },
    "Chapter_05_repository_walkthrough": {
        "playground": {
            "instruction": "Inspect directory layout and essential module entry points programmatically.",
            "code": """import os

def list_project_structure(path='.'):
    print(f"Project Root: {os.path.abspath(path)}")
    essential_files = ['pyproject.toml', 'requirements.txt', 'Dockerfile', 'app.py']
    for file in essential_files:
        exists = os.path.exists(os.path.join(path, file))
        status = "FOUND" if exists else "NOT FOUND"
        print(f"  - {file}: {status}")

list_project_structure()"""
        },
        "quizzes": [
            {
                "question": "What is the main purpose of isolating agent tools into a `tools/` sub-package?",
                "options": [
                    "To make the project folder look larger",
                    "To maintain modular code separation, allowing tools to be added, tested, and updated independently",
                    "Because Docker requires tools in a separate folder",
                    "To prevent Python from importing files"
                ],
                "answerIndex": 1,
                "explanation": "Modular tool architecture enables unit testing individual tool schemas without initializing the entire agent runtime."
            }
        ]
    },
    "Chapter_06_project_setup": {
        "playground": {
            "instruction": "Test package imports and verify core dependencies in Python.",
            "code": """dependencies = ['boto3', 'pydantic', 'fastapi', 'uvicorn', 'requests']

print("Verifying Core Bedrock Dependencies...")
for dep in dependencies:
    try:
        __import__(dep)
        print(f"  [OK] {dep} is installed.")
    except ImportError:
        print(f"  [MISSING] {dep} is not installed.")"""
        },
        "quizzes": [
            {
                "question": "Why is a `pyproject.toml` file preferred over legacy `setup.py` files in modern Python projects?",
                "options": [
                    "It provides a standardized, declarative specification for build systems and dependencies defined in PEP 518/621.",
                    "It runs faster in binary mode.",
                    "It is automatically generated by AWS.",
                    "Legacy setup.py files are illegal."
                ],
                "answerIndex": 0,
                "explanation": "PEP 518/621 standardized `pyproject.toml` as the unified declarative configuration format for modern Python packaging."
            }
        ]
    },
    "Chapter_07_configuration_files": {
        "playground": {
            "instruction": "Simulate reading and validating application configuration from environment variables.",
            "code": """import os
import json

config = {
    "AWS_REGION": os.environ.get("AWS_REGION", "us-east-1"),
    "MODEL_ID": os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
    "MAX_TOKENS": int(os.environ.get("MAX_TOKENS", "4096")),
    "TEMPERATURE": float(os.environ.get("TEMPERATURE", "0.7"))
}

print("Loaded AgentCore Configuration:")
print(json.dumps(config, indent=2))"""
        },
        "quizzes": [
            {
                "question": "Why should configuration settings like AWS region and model IDs be loaded from environment variables?",
                "options": [
                    "To decouple configuration from application source code across dev, staging, and production environments.",
                    "Because hardcoded strings slow down Python execution.",
                    "To prevent Git from tracking Python files.",
                    "Environment variables are required by HTML."
                ],
                "answerIndex": 0,
                "explanation": "Storing configuration in environment variables follows 12-Factor App principles, allowing identical builds to run across different deployment environments."
            }
        ]
    },
    "Chapter_08_running_the_application": {
        "playground": {
            "instruction": "Simulate starting an AgentCore FastAPI server endpoint test.",
            "code": """import time

print("Starting Bedrock AgentCore Local Server Simulation...")
print("Binding server to host: 0.0.0.0, port: 8000")
time.sleep(0.5)

print("GET /healthcheck -> 200 OK (Status: Healthy)")
print("POST /api/v1/agent/invoke -> 200 OK (Agent Execution Completed)")
print("Server is active and ready for incoming requests.")"""
        },
        "quizzes": [
            {
                "question": "Which ASGI web server is commonly used to run asynchronous FastAPI AgentCore services?",
                "options": [
                    "Uvicorn",
                    "Apache HTTPD",
                    "Nginx Static Server",
                    "Tomcat"
                ],
                "answerIndex": 0,
                "explanation": "Uvicorn is a lightning-fast ASGI server implementation for Python, ideal for async FastAPI applications."
            }
        ]
    },
    "Chapter_09_understanding_the_code": {
        "playground": {
            "instruction": "Dissect the ReAct (Reason + Act) loop of an autonomous agent in Python.",
            "code": """def agent_react_loop(user_query):
    print(f"Step 1: Thought -> Analyzing query '{user_query}'")
    print("Step 2: Action -> Invoking weather_tool(location='Seattle')")
    tool_result = {"temperature": "62F", "condition": "Cloudy"}
    print(f"Step 3: Observation -> Received tool output: {tool_result}")
    print("Step 4: Final Answer -> 'The current temperature in Seattle is 62F and cloudy.'")

agent_react_loop("What is the weather in Seattle?")"""
        },
        "quizzes": [
            {
                "question": "What are the core steps of the ReAct (Reason + Act) agent loop pattern?",
                "options": [
                    "Thought, Action, Observation, Final Answer",
                    "Download, Compile, Run, Delete",
                    "Prompt, Reset, Retry, Cancel",
                    "Format, Print, Clear, Save"
                ],
                "answerIndex": 0,
                "explanation": "The ReAct framework alternates between reasoning (Thought), taking tool actions (Action), and observing execution outputs (Observation) to reach a final answer."
            }
        ]
    },
    "Chapter_10_agentcore_runtime": {
        "playground": {
            "instruction": "Test MicroVM container session state management logic.",
            "code": """class MicroVMRuntimeManager:
    def __init__(self):
        self.active_containers = {}

    def spawn_container(self, session_id):
        container_ip = f"172.16.0.{len(self.active_containers) + 2}"
        self.active_containers[session_id] = {"ip": container_ip, "status": "WARM"}
        print(f"Spawned Firecracker microVM for session '{session_id}' at {container_ip}")

mgr = MicroVMRuntimeManager()
mgr.spawn_container("session-user-9941")
print("Active containers:", mgr.active_containers)"""
        },
        "quizzes": [
            {
                "question": "How does Bedrock AgentCore achieve sub-second container spin-up times for agent workflows?",
                "options": [
                    "By pre-warming Firecracker microVM snapshots and sharing lightweight base images.",
                    "By skipping memory allocation.",
                    "By running code on the user's browser.",
                    "By executing code inside SQL databases."
                ],
                "answerIndex": 0,
                "explanation": "Firecracker microVMs leverage minimal virtual machine architectures and pre-warmed snapshot states to launch in milliseconds."
            }
        ]
    },
    "Chapter_11_gateway": {
        "playground": {
            "instruction": "Test API Gateway request routing and payload validation in Python.",
            "code": """def gateway_router(path, payload):
    print(f"[API Gateway] Routing request for path: {path}")
    if path == "/v1/agent/chat":
        if "prompt" not in payload:
            return {"status": 400, "error": "Missing 'prompt' field"}
        return {"status": 200, "destination": "AgentCore-Runtime-Cluster", "data": payload}
    return {"status": 404, "error": "Route not found"}

res = gateway_router("/v1/agent/chat", {"prompt": "Explain Quantum Computing"})
print("Gateway Routing Result:", res)"""
        },
        "quizzes": [
            {
                "question": "What is the primary function of the AgentCore API Gateway component?",
                "options": [
                    "To act as a single entry point for routing, authentication, rate limiting, and protocol translation.",
                    "To store user passwords in plain text.",
                    "To generate random images.",
                    "To format HTML web pages."
                ],
                "answerIndex": 0,
                "explanation": "API Gateways consolidate traffic management, security filtering, rate limiting, and request routing before forwarding payloads to backend agent microservices."
            }
        ]
    },
    "Chapter_12_identity": {
        "playground": {
            "instruction": "Simulate JWT token verification and IAM authorization scope checking.",
            "code": """import time

def verify_token_claims(token):
    print(f"Decoding JWT bearer token: {token[:15]}...")
    claims = {
        "sub": "user_id_8819",
        "role": "DataEngineer",
        "exp": int(time.time()) + 3600,
        "permissions": ["bedrock:invoke", "tools:execute"]
    }
    if "bedrock:invoke" in claims["permissions"]:
        print("Authorization SUCCESS: User granted agent invocation access.")
        return claims
    raise PermissionError("Access denied.")

claims = verify_token_claims("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token")
print("User Identity Claims:", claims)"""
        },
        "quizzes": [
            {
                "question": "How does Bedrock AgentCore enforce tenant isolation during multi-tenant tool execution?",
                "options": [
                    "By isolating session scopes in dedicated Firecracker microVMs and attaching session-specific IAM scoped tokens.",
                    "By giving all users root administrative access.",
                    "By storing data in public S3 buckets.",
                    "By turning off authentication."
                ],
                "answerIndex": 0,
                "explanation": "MicroVM container boundaries combined with fine-grained IAM session tokens prevent users from querying or invoking resources belonging to other tenants."
            }
        ]
    },
    "Chapter_13_memory": {
        "playground": {
            "instruction": "Simulate short-term conversational context and long-term memory retrieval.",
            "code": """class AgentMemoryEngine:
    def __init__(self):
        self.short_term = []
        self.long_term_vector_db = {}

    def add_turn(self, role, text):
        self.short_term.append({"role": role, "content": text})

    def get_context_window(self):
        return self.short_term[-4:] # Last 4 turns

mem = AgentMemoryEngine()
mem.add_turn("user", "My name is Alice.")
mem.add_turn("assistant", "Hello Alice! How can I help you?")
mem.add_turn("user", "What is my name?")
print("Context Window for LLM:", mem.get_context_window())"""
        },
        "quizzes": [
            {
                "question": "What is the difference between short-term conversational context and long-term agent memory?",
                "options": [
                    "Short-term context lives within the LLM context window; long-term memory persists in vector databases or DynamoDB across sessions.",
                    "Short-term context is saved to disk; long-term memory is deleted when the browser closes.",
                    "They are identical terms.",
                    "Long-term memory only works in C++."
                ],
                "answerIndex": 0,
                "explanation": "Short-term context fits in immediate prompt context windows, whereas long-term memory relies on persistent databases (vector search, DynamoDB) to retain facts across sessions."
            }
        ]
    },
    "Chapter_14_tools": {
        "playground": {
            "instruction": "Register and execute a custom Pydantic-validated Python tool for AgentCore.",
            "code": """from pydantic import BaseModel, Field

class DatabaseQueryInput(BaseModel):
    table_name: str = Field(description="Database table to query")
    limit: int = Field(default=10, description="Max rows to return")

def execute_db_tool(input_data: DatabaseQueryInput):
    print(f"Executing tool query on table '{input_data.table_name}' (limit={input_data.limit})...")
    return [{"id": 1, "data": "Sample Record"}]

query = DatabaseQueryInput(table_name="customer_orders", limit=5)
result = execute_db_tool(query)
print("Tool Execution Result:", result)"""
        },
        "quizzes": [
            {
                "question": "Why are Pydantic schemas essential when defining agent tools in Python?",
                "options": [
                    "They automatically generate JSON Schema definitions that foundation models require to format tool parameters accurately.",
                    "Pydantic speeds up CPU clock rates.",
                    "They allow tools to run without Python.",
                    "Pydantic converts Python code into Docker files."
                ],
                "answerIndex": 0,
                "explanation": "LLMs require unambiguous JSON schemas to understand expected parameters. Pydantic automatically serializes Python type hints into JSON Schema specifications."
            }
        ]
    },
    "Chapter_15_deployment": {
        "playground": {
            "instruction": "Simulate Docker build and ECS task deployment health check.",
            "code": """def simulate_deployment():
    print("Step 1: Building Docker Image 'agentcore-runtime:latest'...")
    print("Step 2: Pushing image to Amazon Elastic Container Registry (ECR)...")
    print("Step 3: Updating ECS Fargate Task Definition...")
    print("Step 4: Service status -> 2/2 Tasks RUNNING (HEALTHY)")
    print("Deployment completed successfully!")

simulate_deployment()"""
        },
        "quizzes": [
            {
                "question": "Why is AWS Fargate a preferred container hosting platform for AgentCore microVM workers?",
                "options": [
                    "It is a serverless compute engine that manages underlying EC2 instances automatically, scaling containers seamlessly.",
                    "Fargate only runs static HTML pages.",
                    "It requires manual server patching every hour.",
                    "Fargate removes the need for container images."
                ],
                "answerIndex": 0,
                "explanation": "AWS Fargate removes the operational burden of provisioning and managing EC2 servers, allowing agent runtimes to scale on demand."
            }
        ]
    },
    "Chapter_16_observability": {
        "playground": {
            "instruction": "Test OpenTelemetry trace logging and token usage tracking in Python.",
            "code": """import time

def log_telemetry_trace(span_name, input_tokens, output_tokens, duration_ms):
    trace_event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "span_name": span_name,
        "metrics": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_ms": duration_ms
        }
    }
    print("[OpenTelemetry Trace Event]:")
    print(trace_event)

log_telemetry_trace("AgentCore_Model_Invocation", input_tokens=420, output_tokens=185, duration_ms=640)"""
        },
        "quizzes": [
            {
                "question": "Why is OpenTelemetry (OTel) tracing crucial for autonomous multi-step agent debugging?",
                "options": [
                    "It provides distributed tracing across reasoning steps, model calls, and tool invocations, isolating latency bottlenecks and errors.",
                    "OTel formats text colors in terminal windows.",
                    "It replaces database backups.",
                    "It eliminates API costs."
                ],
                "answerIndex": 0,
                "explanation": "Because agent workflows execute multiple nested steps (thought, tool call, model call, memory fetch), OTel distributed traces allow developers to pinpoint exactly where latencies or failures occur."
            }
        ]
    },
    "Chapter_17_complete_end_to_end_flow": {
        "playground": {
            "instruction": "Simulate the full end-to-end Bedrock AgentCore execution flow.",
            "code": """print("=== End-to-End Bedrock AgentCore Workflow ===")
print("1. User Request -> API Gateway (/v1/agent/invoke)")
print("2. Identity Check -> Validated IAM & Session Token")
print("3. MicroVM Spawn -> Isolated AWS Firecracker Container Created")
print("4. Memory Engine -> Fetched session context from DynamoDB")
print("5. Reasoning Loop -> Model called tool 'search_knowledge_base'")
print("6. Tool Execution -> Retrieved top matching vector records")
print("7. Final Output -> Formatted response returned to client (200 OK)")
print("=== Workflow Execution Completed Successfully ===")"""
        },
        "quizzes": [
            {
                "question": "How do all 7 pillars of Bedrock AgentCore work together in a production deployment?",
                "options": [
                    "Gateway routes traffic, Identity authorizes access, Runtime isolates execution in MicroVMs, Memory retains state, Tools execute actions, Deployment scales compute, and Observability monitors traces.",
                    "Each pillar operates as a separate standalone project without connecting.",
                    "Only the foundation model matters; other components are optional.",
                    "They replace the need for AWS accounts."
                ],
                "answerIndex": 0,
                "explanation": "The 7 pillars form a unified architecture bridging foundation models with enterprise-grade security, scalability, statefulness, and observability."
            }
        ]
    }
}

def format_quiz_jsx(q):
    options_str = str(q['options']).replace("'", '"')
    exp_str = q['explanation'].replace('"', '\\"')
    q_str = q['question'].replace('"', '\\"')
    return f'<Quiz \n  question="{q_str}" \n  options={options_str} \n  answerIndex={q["answerIndex"]} \n  explanation="{exp_str}" \n/>'

def format_playground_jsx(p):
    code_str = p['code'].replace('\\', '\\\\').replace('`', '\\`').replace('"', '\\"')
    inst_str = p['instruction'].replace('"', '\\"')
    return f'<InteractiveExample \n  language="python"\n  instruction="{inst_str}"\n  initialCode="{code_str}"\n/>'

def enrich_file(filepath):
    basename = os.path.splitext(os.path.basename(filepath))[0]
    data = chapter_data.get(basename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any existing duplicate Quiz or InteractiveExample tags to allow fresh clean injection
    content = re.sub(r'<Quiz\s+[\s\S]*?\/>\s*\n*', '', content)
    content = re.sub(r'<InteractiveExample\s+[\s\S]*?\/>\s*\n*', '', content)

    if not data:
        # Generic fallback if specific chapter data isn't mapped
        data = {
            "playground": {
                "instruction": f"Run and test interactive Python code for {basename}.",
                "code": "print('Bedrock AgentCore Interactive Environment Active')\nimport sys\nprint(f'Python version: {sys.version}')"
            },
            "quizzes": [
                {
                    "question": f"What is the key takeaway from {basename}?",
                    "options": [
                        "Following modular architectural principles ensures scalable and secure agent development on AWS.",
                        "Static text files replace software systems.",
                        "All agent code must be written in assembly language.",
                        "Database connections are unnecessary for AI agents."
                    ],
                    "answerIndex": 0,
                    "explanation": "Adhering to structured cloud architecture ensures high reliability, modularity, and security for AI applications."
                }
            ]
        }

    # Format components
    playground_jsx = format_playground_jsx(data['playground'])
    quizzes_jsx = "\n\n".join([format_quiz_jsx(q) for q in data['quizzes']])

    # Insert Playground under Section 10 (Hands-on Examples) or Section 8 / top code area
    if "## 10. Hands-on Examples" in content:
        content = content.replace("## 10. Hands-on Examples", f"## 10. Hands-on Examples\n\n### Interactive Python Playground\n\n{playground_jsx}\n")
    elif "## 8. Installation & Setup" in content:
        content = content.replace("## 8. Installation & Setup", f"## 8. Installation & Setup\n\n### Interactive Python Playground\n\n{playground_jsx}\n")
    else:
        # Append before summary if section 10 not found
        content = content.replace("## 18. Summary", f"### Interactive Python Playground\n\n{playground_jsx}\n\n---\n\n## 18. Summary")

    # Insert Quizzes under Section 15 (Interview Questions) or Section 19 (Practice Exercises)
    if "## 15. Interview Questions" in content:
        content = content.replace("## 15. Interview Questions", f"## 15. Interview Questions\n\n### Knowledge Verification Check\n\n{quizzes_jsx}\n")
    elif "## 19. Practice Exercises" in content:
        content = content.replace("## 19. Practice Exercises", f"## 19. Practice Exercises\n\n### Knowledge Verification Check\n\n{quizzes_jsx}\n")
    else:
        content += f"\n\n---\n\n### Knowledge Verification Check\n\n{quizzes_jsx}\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully enriched {basename}")

# Find all chapter files in bedrock_dir
chapter_files = glob.glob(os.path.join(bedrock_dir, "Chapter_*.md"))
print(f"Found {len(chapter_files)} chapter files to enrich.")

for cf in sorted(chapter_files):
    enrich_file(cf)

print("All chapters successfully enriched with Quizzes and Interactive Playgrounds!")
