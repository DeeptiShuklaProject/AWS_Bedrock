import json
import re

# Load quizzes from convert_docs.py
path = "C:/Users/nishu/workspace/wscs_bedrock/doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md"

with open("C:/Users/nishu/workspace/wscs_bedrock/aura_docs/scratch/convert_docs.py", "r", encoding="utf-8") as f:
    convert_code = f.read()

# Extract quizzes dict using regex or execution
quizzes_match = re.search(r'quizzes = (\{.*?\n\})', convert_code, re.DOTALL)
if quizzes_match:
    quizzes_str = quizzes_match.group(1)
    # We can evaluate it
    quizzes = eval(quizzes_str)
else:
    quizzes = {}

# Clean python.md of any previously appended section first
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Split to keep only the original content (up to Phase 5 or before)
original_content = content.split("# Python for AI Agents (Beginner to Advanced)")[0].strip()

# Now, let's build the interactive AI Agents section content
ai_agents_section = """# Python for AI Agents (Beginner to Advanced)

## Why Python is the Language of AI

Python is the standard language of AI and Agentic development. While other languages offer high execution speed (like C++ or Rust) or native web integration (like JavaScript), Python strikes a balance that makes it irreplaceable:

<InfoCard title="Ecosystem Domination">
Python hosts the entire machine learning and LLM stack (PyTorch, Hugging Face, LangChain, Pydantic, Boto3, FastAPI).
</InfoCard>

<InfoCard title="Syntax Simplicity">
AI development is highly iterative. Writing prompts, parsing schemas, and routing logic must be written and tested rapidly. Python's clean syntax allows developers to write code that reads like pseudo-code.
</InfoCard>

<InfoCard title="C-Bindings Performance">
Heavy calculations (such as tensor math, matrix multiplications, or vector similarity computations) are executed in high-performance C/C++ backends under the hood. Python acts as a developer-friendly glue layer.
</InfoCard>

<InfoCard title="First-Class Framework Support">
Modern agent runtimes (such as Amazon Bedrock AgentCore and Strands) are built from the ground up to consume and execute Python functions natively inside virtualized environments.
</InfoCard>

---

## Python Concepts Needed for AI Agents
"""

concepts_data = [
    {
        "title": "Variables",
        "what_is": "Variables are labels bound to memory locations containing values. Python uses dynamic typing, meaning variable types are resolved at runtime rather than compile-time.",
        "why": "In AI agents, variables are used to track conversational context, extract model payloads, hold active session IDs, and configure prompt parameters.",
        "syntax": "```python\nvariable_name = value\n```",
        "simple_ex": "```python\nprompt_input = \"Search for AWS Bedrock pricing\"\nsession_ttl_seconds = 28800\n```",
        "interactive_code": "prompt_input = \"Search for AWS Bedrock pricing\"\nsession_ttl_seconds = 28800\nprint(f'Prompt: {prompt_input}')\nprint(f'Session TTL: {session_ttl_seconds}s')",
        "agent_ex": "In `ep01_simple_agent.py` line 20-21, variables are extracted dynamically from payload and context parameters:\n```python\nprompt = payload.get(\"prompt\", \"\")\nsession_id = getattr(context, \"session_id\", \"local-session-123\")\n```",
        "bp": ["Use snake_case for variable names.", "Keep variable scopes as localized as possible.", "Use constants (uppercase) for configurations that shouldn't change."],
        "cm": ["Reusing global variables inside functions without specifying `global`, which can lead to reference bugs.", "Variable shadow/collisions (e.g. naming a variable `list` or `dict`, overriding Python built-ins)."],
        "iq": [
            ("What does dynamic typing mean in Python, and how does Python manage object references?", "Dynamic typing means variables do not have static types; they point to objects in memory that have types. When you assign `x = 10` and then `x = \"text\"`, Python simply rebinds the label `x` from an integer object to a string object, updating the reference count of each object.")
        ]
    },
    {
        "title": "Functions",
        "what_is": "Functions are reusable blocks of code that execute a specific action. Python support variable arguments (*args, **kwargs), default parameters, and first-class function objects.",
        "why": "AI Agent tools are registered as Python functions. LLM frameworks inspect function signatures and docstrings to generate JSON schemas.",
        "syntax": "```python\ndef function_name(param1, param2=default_val, *args, **kwargs):\n    return result\n```",
        "simple_ex": "```python\ndef generate_prompt(task, context=\"\"):\n    return f\"Task: {task}\\nContext: {context}\"\n```",
        "interactive_code": "def generate_prompt(task, context=\"\"):\n    return f\"Task: {task}\\nContext: {context}\"\n\nprint(generate_prompt(\"Summarize logs\", \"Error at 12:00\"))",
        "agent_ex": "In `ep01_simple_agent.py` line 34, functions define tools that agents can run:\n```python\ndef get_user_details(user_id: str) -> dict:\n    return {\"user_id\": user_id, \"role\": \"developer\"}\n```",
        "bp": ["Define explicit parameter names and use docstrings for LLM tool binding.", "Avoid mutable default arguments like `list` or `dict`."],
        "cm": ["Using `history=[]` as a default argument. Python instantiates mutable default parameters once, causing state leak between function calls."],
        "iq": [
            ("Why are mutable default arguments dangerous in Python?", "Mutable defaults are evaluated once at function definition time. Subsequent calls modify the same object, leaking state.")
        ]
    },
    {
        "title": "Classes",
        "what_is": "Classes are blueprints for creating objects. They bundle data (attributes) and behavior (methods) together.",
        "why": "Agents maintain memory, state, client sessions, and tools inside structured class instances.",
        "syntax": "```python\nclass Agent:\n    def __init__(self, name):\n        self.name = name\n```",
        "simple_ex": "```python\nclass Memory:\n    def __init__(self):\n        self.history = []\n    def add(self, msg):\n        self.history.append(msg)\n```",
        "interactive_code": "class Memory:\n    def __init__(self):\n        self.history = []\n    def add(self, msg):\n        self.history.append(msg)\n\nmem = Memory()\nmem.add(\"Hello agent\")\nprint(mem.history)",
        "agent_ex": "In `ep02_production_supervisor.py` line 12, agents are defined as classes inheriting from a base Agent:\n```python\nclass SupervisorAgent(BaseAgent):\n    def __init__(self, team_members):\n        super().__init__(\"Supervisor\")\n        self.team = team_members\n```",
        "bp": ["Always initialize attributes inside `__init__`.", "Keep class responsibilities single and focused."],
        "cm": ["Defining instance variables as class variables, sharing state across all instances accidentally."],
        "iq": [
            ("What is the difference between class variables and instance variables?", "Class variables are shared by all instances of a class. Instance variables are unique to each instance.")
        ]
    },
    {
        "title": "OOP",
        "what_is": "Object-Oriented Programming (OOP) uses encapsulation, inheritance, polymorphism, and abstraction to structure programs.",
        "why": "Different types of agents (e.g. Supervisor, Worker, Auditor) share base agent interfaces while overriding execution steps.",
        "syntax": "```python\nclass WorkerAgent(BaseAgent):\n    def execute(self):\n        pass\n```",
        "simple_ex": "```python\nclass BaseAgent:\n    def run(self):\n        raise NotImplementedError()\n\nclass SimpleAgent(BaseAgent):\n    def run(self):\n        return \"Running task\"\n```",
        "interactive_code": "class BaseAgent:\n    def run(self):\n        raise NotImplementedError()\n\nclass SimpleAgent(BaseAgent):\n    def run(self):\n        return \"Running task\"\n\nagent = SimpleAgent()\nprint(agent.run())",
        "agent_ex": "In `ep02_production_supervisor.py` line 45, polymorphism is used to run different agent routines concurrently:\n```python\nfor agent in self.team:\n    agent.execute(task)\n```",
        "bp": ["Use Abstract Base Classes (ABCs) to enforce tool/agent schemas.", "Prefer composition over inheritance where applicable."],
        "cm": ["Deep inheritance hierarchies that make code fragile and difficult to trace."],
        "iq": [
            ("What algorithm does Python use to determine Method Resolution Order (MRO) in multiple inheritance?", "Python uses the C3 Linearization algorithm to construct a deterministic list for class lookups.")
        ]
    },
    {
        "title": "Modules",
        "what_is": "A module is a file containing Python definitions and statements. The file name is the module name with the suffix `.py` appended.",
        "why": "Splitting code into modules keeps tools, prompts, database logic, and agent definitions organized and importable.",
        "syntax": "```python\n# File: tools.py\ndef call_tool(): pass\n\n# File: main.py\nimport tools\n```",
        "simple_ex": "```python\n# Save as agent_math.py\ndef add_numbers(a, b):\n    return a + b\n```",
        "interactive_code": "# Since this is a module, we show local import simulation\nimport math\nprint(math.sqrt(16))",
        "agent_ex": "In `ep01_simple_agent.py` line 5, prompt templates are loaded from a dedicated module:\n```python\nfrom prompts.agent_prompts import SYSTEM_INSTRUCTION\n```",
        "bp": ["Keep modules focused on a single concern (e.g. tools, clients, schemas).", "Avoid wildcard imports like `from module import *`."],
        "cm": ["Circular imports where module A imports B and B imports A, causing runtime failures."],
        "iq": [
            ("How do you prevent code in a module from running when imported?", "Wrap the execution code block in an `if __name__ == '__main__':` block.")
        ]
    },
    {
        "title": "Packages",
        "what_is": "Packages are namespaces containing multiple modules, structured using directories and designated by `__init__.py` files.",
        "why": "Complex agent runtimes are distributed as packages containing subpackages for memory, tools, and LLM providers.",
        "syntax": "```\nmy_package/\n    __init__.py\n    agent.py\n    tools/\n        __init__.py\n        web_search.py\n```",
        "simple_ex": "```python\n# package init exposes API endpoints\nfrom .agent import RouterAgent\n```",
        "interactive_code": "# Simulate package import using standard library packages\nimport os.path\nprint(os.path.join(\"usr\", \"bin\"))",
        "agent_ex": "Exposing primary endpoints in `__init__.py` simplifies agent imports:\n```python\nfrom my_agent_framework.core.agents import Agent\nfrom my_agent_framework.core.tasks import Task\n```",
        "bp": ["Keep `__init__.py` files light and only use them to expose high-level APIs.", "Design clean package directory hierarchies."],
        "cm": ["Omitting `__init__.py` in packages intended for legacy Python installations (before namespace packaging was introduced)."],
        "iq": [
            ("What is the role of __init__.py in a Python package?", "It signals to Python that the directory is a package, and executes package-level initializations.")
        ]
    },
    {
        "title": "Decorators",
        "what_is": "Decorators modify or wrap function behaviors without changing their core source code. They take a function as input and return a wrapper function.",
        "why": "Decorators (like `@tool` or `@app.invoke`) register functions in LLM registries, automatically parse schemas, and log inputs/outputs.",
        "syntax": "```python\ndef my_decorator(func):\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper\n```",
        "simple_ex": "```python\nimport functools\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"Calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n```",
        "interactive_code": "import functools\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"Calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef say_hi():\n    print(\"Hello!\")\n\nsay_hi()",
        "agent_ex": "In `ep01_simple_agent.py` line 12, `@app.invoke` registers agent handlers dynamically:\n```python\n@app.invoke(name=\"agent_runtime\")\ndef handle_agent(payload, context):\n    # handler code\n```",
        "bp": ["Always use `@functools.wraps(func)` to preserve function metadata (docstring, name, annotations).", "Use decorators for clean cross-cutting concerns like logging and security checks."],
        "cm": ["Forgetting to return the wrapper function from the decorator.", "Losing metadata because `@functools.wraps` was omitted."],
        "iq": [
            ("Why should you use @functools.wraps(func) when writing a custom decorator wrapper?", "It copies the original function's name, docstring, and annotations metadata to the wrapper function, avoiding introspection breakage.")
        ]
    },
    {
        "title": "Context Managers",
        "what_is": "Context Managers manage resource allocation and cleanup using `with` blocks. They implement `__enter__` and `__exit__` magic methods.",
        "why": "Agents use context managers to guarantee clean-up of database connections, remote API sessions, vector store indices, and sandbox runtimes.",
        "syntax": "```python\nwith open('file.txt', 'r') as f:\n    content = f.read()\n```",
        "simple_ex": "```python\nclass SandboxSession:\n    def __enter__(self):\n        print(\"Allocating sandbox\")\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print(\"Destroying sandbox\")\n```",
        "interactive_code": "class SandboxSession:\n    def __enter__(self):\n        print(\"Allocating sandbox\")\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print(\"Destroying sandbox\")\n\nwith SandboxSession():\n    print(\"Executing user code inside sandbox\")",
        "agent_ex": "Ensuring remote clients are closed after agent execution:\n```python\nwith httpx.Client() as client:\n    response = client.post(\"https://api.bedrock.com/v1\", json=payload)\n```",
        "bp": ["Use `@contextlib.contextmanager` for quick, generator-based context managers.", "Always clean up resources in `__exit__` even if exceptions are raised."],
        "cm": ["Swallowing exceptions in `__exit__` by returning `True` without checking if it is safe to do so."],
        "iq": [
            ("What does returning True from __exit__ do in a context manager?", "It suppresses the exception raised inside the `with` block, preventing it from bubbling up.")
        ]
    },
    {
        "title": "Exception Handling",
        "what_is": "Exception handling manages runtime errors using `try`, `except`, `else`, and `finally` blocks.",
        "why": "LLM calls fail due to rate limits, format errors, or model hallucinations. Exception blocks catch and execute fallbacks.",
        "syntax": "```python\ntry:\n    # execute code\nexcept ExceptionType as e:\n    # handle error\nfinally:\n    # cleanup code\n```",
        "simple_ex": "```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    result = 0\n```",
        "interactive_code": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    result = 0\nprint(f'Result: {result}')",
        "agent_ex": "In `ep01_simple_agent.py` line 67, rate limits are managed dynamically:\n```python\ntry:\n    response = bedrock_client.invoke_model(**kwargs)\nexcept bedrock_client.exceptions.ThrottlingException:\n    time.sleep(2) # Backoff\n```",
        "bp": ["Avoid bare `except:` clauses as they catch system exit exceptions.", "Derive custom exceptions (like `TokenLimitException`) from `Exception`."],
        "cm": ["Using bare `except:` which catches keyboard interrupts and prevents script termination."],
        "iq": [
            ("Why is using a bare except: clause considered a dangerous anti-pattern?", "It catches BaseException, including KeyboardInterrupt and SystemExit, making it impossible to stop the program normally.")
        ]
    },
    {
        "title": "Typing",
        "what_is": "Python typing provides type hinting metadata for variables and function signatures, used by static analyzers like `mypy`.",
        "why": "Pydantic and FastAPI read type hints (like `List[str]` or `Union[int, str]`) to generate schemas and validate input fields.",
        "syntax": "```python\nx: int = 10\ndef run_agent(name: str) -> dict:\n    return {}\n```",
        "simple_ex": "```python\nfrom typing import List, Dict, Optional\ndef parse_tags(tags: List[str]) -> Optional[str]:\n    return tags[0] if tags else None\n```",
        "interactive_code": "from typing import List, Optional\ndef parse_tags(tags: List[str]) -> Optional[str]:\n    return tags[0] if tags else None\n\nprint(parse_tags([\"agent\", \"mcp\"]))",
        "agent_ex": "Defining strict type schemas for agent tools ensures LLMs invoke them correctly:\n```python\ndef query_db(query: str, limit: int = 10) -> List[Dict[str, Any]]:\n    # database query\n```",
        "bp": ["Use type hints for public APIs and tool helper signatures.", "Use `mypy` to validate typing compliance during CI/CD pipelines."],
        "cm": ["Relying on type hints to enforce constraints at runtime without using validation libraries like Pydantic."],
        "iq": [
            ("Does Python enforce type hints at runtime?", "No. Type hints are completely ignored by the interpreter at runtime. They are only metadata for IDEs and static checkers.")
        ]
    },
    {
        "title": "Async Programming",
        "what_is": "Asynchronous programming uses an event loop, `async` / `await` keywords, and coroutines to run concurrent non-blocking IO operations.",
        "why": "Agents invoke multiple LLMs, web search APIs, and databases concurrently. Async execution speeds up execution time dramatically.",
        "syntax": "```python\nasync def fetch():\n    await asyncio.sleep(1)\n```",
        "simple_ex": "```python\nimport asyncio\nasync def main():\n    print(\"Hello async\")\n    await asyncio.sleep(0.1)\n```",
        "interactive_code": "import asyncio\nasync def main():\n    print(\"Hello async\")\n    await asyncio.sleep(0.1)\n\n# Run main loop\nasyncio.run(main())",
        "agent_ex": "Running worker operations concurrently in `ep02_production_supervisor.py`:\n```python\nasync def run_workers(tasks):\n    results = await asyncio.gather(*[worker.run(t) for t in tasks])\n    return results\n```",
        "bp": ["Never call blocking synchronous functions (like `time.sleep()`) in async functions; use `await asyncio.sleep()` instead.", "Use `asyncio.gather` to execute tasks concurrently."],
        "cm": ["Stalling the event loop by calling blocking synchronous functions inside coroutines."],
        "iq": [
            ("What happens if you block the asyncio event loop with a call like time.sleep(5)?", "The entire event loop freezes, blocking all other running concurrent tasks from executing for 5 seconds.")
        ]
    },
    {
        "title": "Dataclasses",
        "what_is": "Dataclasses provide a decorator `@dataclass` that automatically adds special methods like `__init__` and `__repr__` to classes.",
        "why": "Dataclasses act as clean, lightweight records to hold agent payloads, configuration parameters, and execution state.",
        "syntax": "```python\nfrom dataclasses import dataclass\n@dataclass\nclass AgentConfig:\n    model: str\n    max_tokens: int\n```",
        "simple_ex": "```python\nfrom dataclasses import dataclass\n@dataclass\nclass User:\n    username: str\n    user_id: int\n```",
        "interactive_code": "from dataclasses import dataclass\n@dataclass\nclass User:\n    username: str\n    user_id: int\n\nu = User(\"agent_dev\", 99)\nprint(u)",
        "agent_ex": "Defining task specifications in `ep02_production_supervisor.py`:\n```python\n@dataclass\nclass AgentTask:\n    task_id: str\n    prompt: str\n    temperature: float = 0.7\n```",
        "bp": ["Use `frozen=True` to create immutable dataclasses that are hashable.", "Provide default values for optional configurations."],
        "cm": ["Using mutable types (like lists/dicts) as default field values without using `default_factory`."],
        "iq": [
            ("How do you make a Python dataclass immutable and hashable?", "Set the `frozen=True` argument in the decorator: `@dataclass(frozen=True)`.")
        ]
    },
    {
        "title": "Enums",
        "what_is": "Enums are sets of symbolic names bound to unique, constant values, inheriting from the `Enum` base class.",
        "why": "Enums categorize worker statuses (e.g. `PENDING`, `RUNNING`, `SUCCESS`) and target models in agent routing logic.",
        "syntax": "```python\nfrom enum import Enum\nclass Role(Enum):\n    USER = \"user\"\n    AGENT = \"agent\"\n```",
        "simple_ex": "```python\nfrom enum import Enum\nclass Status(Enum):\n    ACTIVE = 1\n    INACTIVE = 2\n```",
        "interactive_code": "from enum import Enum\nclass Status(Enum):\n    ACTIVE = 1\n    INACTIVE = 2\n\nprint(Status.ACTIVE.name)\nprint(Status.ACTIVE.value)",
        "agent_ex": "Managing agent orchestration workflows in `ep02_production_supervisor.py`:\n```python\nclass StepStatus(str, Enum):\n    NOT_STARTED = \"NOT_STARTED\"\n    IN_PROGRESS = \"IN_PROGRESS\"\n    COMPLETED = \"COMPLETED\"\n```",
        "bp": ["Inherit from both `str` and `Enum` to make values directly JSON serializable.", "Use uppercase names for Enum members."],
        "cm": ["Comparing Enum members directly with primitive types without extracting `.value` (if they are not str-subclassed)."],
        "iq": [
            ("Why is inheriting from both str and Enum (e.g., class Role(str, Enum)) helpful in APIs?", "It allows the enum members to be serialized directly as plain strings in JSON outputs without requiring custom serializers.")
        ]
    },
    {
        "title": "Logging",
        "what_is": "Logging tracks runtime events. Python's built-in `logging` module offers custom handlers, formatters, and logging levels.",
        "why": "JSON logging captures prompt executions, execution paths, database latencies, and tool trace logs in production environments.",
        "syntax": "```python\nimport logging\nlogging.basicConfig(level=logging.INFO)\nlogging.info(\"Log message\")\n```",
        "simple_ex": "```python\nimport logging\nlogger = logging.getLogger(\"AgentLogger\")\nlogger.warning(\"Tool timeout detected\")\n```",
        "interactive_code": "import logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"AgentDemo\")\nlogger.info(\"Simple test log\")",
        "agent_ex": "In `ep05_auth_middleware.py` line 15, request handling logs route details:\n```python\nlogger.info(\"Incoming agent invocation\", extra={\"session_id\": session_id, \"route\": route})\n```",
        "bp": ["Use structured JSON formatters to feed logs directly into Log Search Engines.", "Log exceptions using `logger.exception` to capture full tracebacks."],
        "cm": ["Using print statements instead of logs in production code, which clutter standard outputs and lack severity labels."],
        "iq": [
            ("Why is structured JSON logging preferred over plaintext logging for production agents?", "Log aggregators parse JSON keys natively, making it fast and easy to query logs by session, module, or user ID.")
        ]
    },
    {
        "title": "Environment Variables",
        "what_is": "Environment variables are configuration values defined in the system shell process environment.",
        "why": "API keys (like `GEMINI_API_KEY` or `OPENAI_API_KEY`) and server configurations must be kept secure, out of code repository commits.",
        "syntax": "```python\nimport os\napi_key = os.getenv(\"GEMINI_API_KEY\")\n```",
        "simple_ex": "```python\nimport os\nport = int(os.environ.get(\"PORT\", 8000))\n```",
        "interactive_code": "import os\nprint(\"Current HOME directory:\", os.environ.get(\"USERPROFILE\", \"Unknown\"))",
        "agent_ex": "In `ep01_simple_agent.py` line 14, system clients are configured using environment variables:\n```python\nbedrock_client = boto3.client(\"bedrock-runtime\", region_name=os.getenv(\"AWS_DEFAULT_REGION\", \"us-east-1\"))\n```",
        "bp": ["Always provide sensible default fallbacks when retrieving optional environment variables.", "Never commit files containing hardcoded keys to code repositories."],
        "cm": ["Hardcoding secret tokens directly into source files, risking severe security breaches when code is pushed to public remotes."],
        "iq": [
            ("How do you securely configure credentials in local development vs production environments?", "Use `.env` files for local setups (added to `.gitignore`) and system/cloud parameter stores in production.")
        ]
    },
    {
        "title": "Virtual Environments",
        "what_is": "Virtual environments isolate python package libraries installed on a system, keeping project dependencies clean and separated.",
        "why": "Agents need specific, locked versions of libraries like `pydantic` or `langchain` that could conflict with global system packages.",
        "syntax": "```bash\npython -m venv .venv\nsource .venv/bin/activate  # On Unix\n.venv\\Scripts\\activate     # On Windows\n```",
        "simple_ex": "```bash\npython -m venv my_env\n```",
        "interactive_code": "# Simulate checking current virtual env prefix\nimport sys\nprint(\"Virtual environment path:\", sys.prefix)",
        "agent_ex": "Standard runtimes activate virtual environments before execution:\n```bash\n# Production deployment script\ncd /app && source .venv/bin/activate && python main.py\n```",
        "bp": ["Always create and activate virtual environments before installing packages.", "Exclude virtual environment folders (like `.venv`) in `.gitignore`."],
        "cm": ["Installing dependencies globally using root/administrator privileges, breaking system tools."],
        "iq": [
            ("How does activating a virtual environment affect import resolution?", "It updates the environment shell's PATH, ensuring python loads imports from the virtual env's `site-packages` directory instead of global paths.")
        ]
    },
    {
        "title": "Pip",
        "what_is": "Pip is the package installer for Python. It downloads and manages libraries from the Python Package Index (PyPI).",
        "why": "Pip installs agent dependencies, including SDK clients, database drivers, and serialization libraries.",
        "syntax": "```bash\npip install package_name\npip install -r requirements.txt\n```",
        "simple_ex": "```bash\npip install requests pydantic\n```",
        "interactive_code": "# Show installed packages demo\nimport pkg_resources\nfor dist in list(pkg_resources.working_set)[:5]:\n    print(f'{dist.project_name} ({dist.version})')",
        "agent_ex": "Installing packages dynamically in sandbox runtimes:\n```python\nsubprocess.run([\"pip\", \"install\", \"-r\", \"requirements.txt\"])\n```",
        "bp": ["Pin package versions in `requirements.txt` to prevent breaking changes on updates.", "Use editable mode `pip install -e .` for local package development."],
        "cm": ["Installing packages without pinning versions, causing dependency drifts and build errors in deployment pipelines."],
        "iq": [
            ("What is the difference between pip install and pip install -e .?", "Editable mode (-e) installs the local directory as a symbolic link, so source file modifications are immediately reflected in imports without reinstalling.")
        ]
    },
    {
        "title": "UV",
        "what_is": "UV is a fast, modern package installer and resolver written in Rust, designed to replace pip, pip-tools, and virtualenv.",
        "why": "Speeding up agent deployment times and virtual environment creation in containerized execution clusters.",
        "syntax": "```bash\nuv pip install -r requirements.txt\nuv venv\n```",
        "simple_ex": "```bash\nuv pip install httpx pydantic\n```",
        "interactive_code": "# Show uv command simulation\nprint(\"UV executes concurrent Rust resolutions, downloading libraries rapidly.\")",
        "agent_ex": "Running Docker deployments using UV:\n```dockerfile\nRUN pip install uv && uv pip install --system -r requirements.txt\n```",
        "bp": ["Use UV in CI/CD pipelines to speed up build processes.", "Keep dependencies cached globally for optimal deployment performance."],
        "cm": ["Expecting UV to fix broken dependency requirements that have no valid resolved paths."],
        "iq": [
            ("What makes UV faster than traditional pip?", "UV is built in Rust. It utilizes parallel dependency fetching, a global cache, and hard links instead of copy operations.")
        ]
    },
    {
        "title": "Poetry",
        "what_is": "Poetry is a dependency management and packaging tool in Python that locks dependency versions in a deterministic file.",
        "why": "Ensuring reproducible builds for agent platforms by locking all sub-dependencies with cryptographic hashes.",
        "syntax": "```toml\n# pyproject.toml\n[tool.poetry.dependencies]\npython = \"^3.10\"\nlangchain = \"*\"\n```",
        "simple_ex": "```bash\npoetry add pydantic\npoetry install\n```",
        "interactive_code": "# Poetry simulation\nprint(\"Poetry uses poetry.lock to resolve and pin dependencies.\")",
        "agent_ex": "Production agent templates use poetry to publish core toolkits:\n```bash\npoetry build\npoetry publish\n```",
        "bp": ["Always commit `poetry.lock` to ensure all developers run identical library versions.", "Keep dependencies categorized under groups (e.g. dev, test)."],
        "cm": ["Manually editing `poetry.lock` instead of using `poetry add` or `poetry update`."],
        "iq": [
            ("What is the difference between pyproject.toml and poetry.lock?", "pyproject.toml specifies general dependency version limits, while poetry.lock pins the exact version hashes of all sub-dependencies.")
        ]
    },
    {
        "title": "JSON",
        "what_is": "JSON is a text format used to represent structured data. Python's built-in `json` module translates data to and from dictionaries.",
        "why": "LLMs speak JSON. Agents serialize prompt parameters to JSON and deserialize responses back into structured objects.",
        "syntax": "```python\nimport json\njson_str = json.dumps(data_dict)\ndict_data = json.loads(json_str)\n```",
        "simple_ex": "```python\nimport json\npayload = json.dumps({\"query\": \"hello\", \"history\": []})\n```",
        "interactive_code": "import json\npayload = json.dumps({\"query\": \"hello\", \"history\": []})\nprint(payload)\nprint(json.loads(payload))",
        "agent_ex": "In `ep01_simple_agent.py` line 48, agent outputs are structured in JSON payloads:\n```python\nresult = json.loads(response[\"body\"].read().decode(\"utf-8\"))\n```",
        "bp": ["Use `json.JSONDecodeError` to handle malformed LLM responses safely.", "Pass `indent=4` to formatting functions for logging outputs."],
        "cm": ["Trying to serialize non-serializable objects (like `datetime` objects or custom classes) without custom JSON encoders."],
        "iq": [
            ("How do you handle custom non-serializable objects (like datetime) using json.dumps()?", "Provide a custom encoder subclassing `json.JSONEncoder` or pass a serialization helper function to the `default` argument.")
        ]
    },
    {
        "title": "HTTP APIs",
        "what_is": "HTTP APIs allow communication between clients and web servers using requests (GET, POST) over network channels.",
        "why": "Agents communicate with external LLM hosting services, vector search endpoints, and downstream tools using HTTP protocols.",
        "syntax": "```python\nimport requests\nresp = requests.post(url, json=data)\n```",
        "simple_ex": "```python\nimport httpx\nresp = httpx.get(\"https://httpbin.org/get\")\n```",
        "interactive_code": "import httpx\nresp = httpx.get(\"https://httpbin.org/get\")\nprint(resp.status_code)",
        "agent_ex": "In `ep04_lambda_mcp_server.py` line 26, tools run HTTP search queries:\n```python\nasync with httpx.AsyncClient() as client:\n    response = await client.post(SEARCH_URL, json=payload)\n```",
        "bp": ["Always set explicit request timeouts to prevent threads from hanging.", "Use async clients (`httpx.AsyncClient`) inside concurrent async code blocks."],
        "cm": ["Making synchronous HTTP requests inside async loops, freezing execution across concurrent queries."],
        "iq": [
            ("When should you use httpx instead of requests?", "Use `httpx` when you need async support (`async/await`) to make non-blocking HTTP requests concurrently.")
        ]
    },
    {
        "title": "FastAPI Basics",
        "what_is": "FastAPI is an ASGI framework built on Pydantic and type hints, enabling easy generation of REST endpoints.",
        "why": "FastAPI hosts agents as web APIs, accepting client queries, executing tool routing, and streaming responses back.",
        "syntax": "```python\nfrom fastapi import FastAPI\napp = FastAPI()\n@app.get(\"/\")\ndef home(): return {}\n```",
        "simple_ex": "```python\nfrom fastapi import FastAPI\napp = FastAPI()\n@app.post(\"/invoke\")\ndef run(payload: dict): return {\"status\": \"ok\"}\n```",
        "interactive_code": "# Simulate FastAPI endpoint setup\nprint(\"FastAPI app instance configured with ASGI routers.\")",
        "agent_ex": "In `ep01_simple_agent.py` line 18, routers expose api endpoints:\n```python\n@router.post(\"/chat\")\nasync def chat_endpoint(payload: ChatPayload):\n    return await agent_executor.run(payload)\n```",
        "bp": ["Use Pydantic models for request body inputs instead of raw dictionaries.", "Use dependency injection for clean database connections."],
        "cm": ["Exposing sensitive credentials in OpenAPI documentation routes by failing to configure security handlers."],
        "iq": [
            ("How does FastAPI generate its OpenAPI documentation automatically?", "It inspects path declarations, type hints, and Pydantic model definitions in endpoint signatures to compile standard JSON schemas.")
        ]
    },
    {
        "title": "Pydantic",
        "what_is": "Pydantic is a data validation library that enforces type hints, transforming raw inputs into structured objects and validating fields.",
        "why": "LLMs are prompted to output JSON matching Pydantic schemas. Pydantic parses output JSON, throwing errors if fields are missing.",
        "syntax": "```python\nfrom pydantic import BaseModel\nclass User(BaseModel):\n    name: str\n    age: int\n```",
        "simple_ex": "```python\nfrom pydantic import BaseModel, Field\nclass Query(BaseModel):\n    text: str = Field(description=\"User query\")\n```",
        "interactive_code": "from pydantic import BaseModel\nclass Query(BaseModel):\n    text: str\n\nq = Query(text=\"Search database\")\nprint(q.model_dump())",
        "agent_ex": "Validating incoming agent execution requests:\n```python\nclass InvocationPayload(BaseModel):\n    session_id: str\n    prompt: str\n    temperature: Optional[float] = 0.7\n```",
        "bp": ["Provide descriptive `Field(description=...)` info so LLMs understand tool parameters.", "Use `@field_validator` for custom integrity validation rules."],
        "cm": ["Passing raw dictionaries to LLMs directly instead of validating and serializing them with Pydantic."],
        "iq": [
            ("What does Pydantic do when you pass a numeric string like '42' to a field defined as an integer?", "Pydantic coerces the value, converting the string '42' into the integer 42 automatically.")
        ]
    },
    {
        "title": "Dependency Injection",
        "what_is": "Dependency Injection passes required resources (database connections, clients) directly into routes/functions, separating code dependencies.",
        "why": "FastAPI endpoints inject Bedrock clients, database repositories, or session cache stores cleanly into running agents.",
        "syntax": "```python\nfrom fastapi import Depends\ndef run_query(db = Depends(get_db)): pass\n```",
        "simple_ex": "```python\nclass Database:\n    def get_data(self): return []\n\ndef fetch_details(db: Database):\n    return db.get_data()\n```",
        "interactive_code": "# Dependency injection simulation\ndef get_config(): return {\"model\": \"claude\"}\ndef run(config = get_config()): print(\"Model configured:\", config)\nrun()",
        "agent_ex": "In `ep05_auth_middleware.py` line 12, routes inject active database connections:\n```python\n@app.post(\"/query\")\nasync def handle_query(payload: dict, db: Session = Depends(get_db_session)):\n    # execute agent with database context\n```",
        "bp": ["Use `Depends` in FastAPI to retrieve active security users or session instances.", "Write modular dependencies to allow testing with mock clients."],
        "cm": ["Hardcoding database clients or API connections directly inside route methods, making testing difficult."],
        "iq": [
            ("How does FastAPI's Depends simplify application testing?", "It allows unit tests to override dependencies (e.g. database sessions) with mock instances using `app.dependency_overrides`.")
        ]
    },
    {
        "title": "File Handling",
        "what_is": "File handling opens and manages files on disk, utilizing the standard `pathlib.Path` class for modern OOP operations.",
        "why": "Agents read files for context, ingestion tasks, and document searches, utilizing path validation to prevent security issues.",
        "syntax": "```python\nfrom pathlib import Path\np = Path(\"config.json\")\ncontent = p.read_text()\n```",
        "simple_ex": "```python\nfrom pathlib import Path\np = Path(\"output.txt\")\np.write_text(\"Agent complete.\")\n```",
        "interactive_code": "from pathlib import Path\np = Path(\"demo.txt\")\np.write_text(\"Hello disk!\")\nprint(p.read_text())",
        "agent_ex": "Validating local directory paths before opening files:\n```python\nsafe_path = Path(\"/app/sandbox\").resolve()\ntarget_file = (safe_path / user_path).resolve()\nif not target_file.is_relative_to(safe_path):\n    raise ValueError(\"Path traversal detected!\")\n```",
        "bp": ["Always use `pathlib` over the older `os.path` module.", "Resolve paths fully and validate parent directories to prevent security risks."],
        "cm": ["Concatting strings for paths (e.g., `folder + '/' + file`), causing runtime issues on Windows vs Unix."],
        "iq": [
            ("Why is pathlib.Path preferred over os.path?", "pathlib provides a cross-platform, object-oriented API that handles forward/backslashes automatically.")
        ]
    },
    {
        "title": "Package Structure",
        "what_is": "Package structure defines how files, packages, modules, tests, and configuration entries are organized in a project.",
        "why": "Production agents require modular setups dividing tools, agents, routers, and configurations into structured packages.",
        "syntax": "```\nproject/\n  pyproject.toml\n  src/\n    my_agent/\n      __init__.py\n      main.py\n      tools.py\n  tests/\n    test_agent.py\n```",
        "simple_ex": "```python\n# File layout inside the src/ folder structures imports cleanly\n```",
        "interactive_code": "print(\"Modular package structures separate backend endpoints, configurations, and core logics.\")",
        "agent_ex": "Deploying agent containers using modular imports:\n```python\nfrom src.my_agent.tools import search_web\nfrom src.my_agent.main import agent_runtime\n```",
        "bp": ["Use the `src/` layout layout to enforce installation-based testing of packages.", "Organize tests into a dedicated `tests/` directory separate from source files."],
        "cm": ["Importing modules via inconsistent paths, causing path errors in container environments."],
        "iq": [
            ("Why is the src/ layout configuration considered a best practice in Python packaging?", "It prevents tools from importing local source files directly, forcing tests to run against the installed package, detecting packaging errors early.")
        ]
    }
]

# Generate MDX widgets for each concept
concepts_body = ""
for idx, c in enumerate(concepts_data, 1):
    quiz_str = ""
    quiz_data = quizzes.get(c["title"], None)
    if quiz_data:
        quiz_str = f"""<Quiz 
  question={json.dumps(quiz_data["question"])} 
  options={{{json.dumps(quiz_data["options"])}}} 
  answerIndex={{{quiz_data["answerIndex"]}}} 
  explanation={json.dumps(quiz_data["explanation"])} 
/>"""

    iq_blocks = []
    for q, a in c["iq"]:
        iq_blocks.append(f'<InterviewQuestion q={json.dumps(q)} a={json.dumps(a)} />')
    
    iq_str = ""
    if iq_blocks:
        iq_str = f"""<InterviewQuestions>
  {" ".join(iq_blocks)}
</InterviewQuestions>"""

    bp_list = "\n".join(f"- {item}" for item in c["bp"])
    cm_list = "\n".join(f"- {item}" for item in c["cm"])

    # Tabs with InteractivePlayground
    tabs_str = f"""<Tabs>
  <Tab label="Syntax & Example">

{c["syntax"]}

{c["simple_ex"]}

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      initialCode={json.dumps(c["interactive_code"])} 
      instruction="Run this interactive python example and see the console output."
    />
  </Tab>
</Tabs>"""

    concept_md = f"""
### {c["title"]}
<ProgressTracker currentSection={{{idx}}} totalSections={{{len(concepts_data)}}} />

<InfoCard title="Concept Overview">
{c["what_is"]}

**Why do we need it?**
{c["why"]}
</InfoCard>

{tabs_str}

<InfoCard title="AI Agent Integration">
{c["agent_ex"]}
</InfoCard>

<Tip>
{bp_list}
</Tip>

<Warning>
{cm_list}
</Warning>

{quiz_str}

{iq_str}
"""
    concepts_body += concept_md

# Tail sections
tail_sections = """
## Agent Architecture with Python

In AI agent engineering, agent instances act as orchestrators coordinating model responses, active tools, and memory contexts.

<AgentArchitectureDiagram />

### Short-Term Memory vs Long-Term Memory
* **Short-Term Memory**: Stored as active JSON contexts passed back and forth within conversational turns.
* **Long-Term Memory**: Persisted in external vector search engines (like Pinecone or OpenSearch) or database layers (like DynamoDB), retrieved dynamically during runtime routing.

---

## Understanding Decorator-Based Agent Frameworks

In frameworks like LangChain, CrewAI, and Bedrock AgentCore, decorators (such as `@tool` or `@app.invoke`) modify target functions dynamically.

<DecoratorVisualizer decoratorName="@app.tool" functionName="get_balance" args="user_id" returns="100.0" />

The decorator extracts metadata from function signature types and docstrings to automatically generate JSON-RPC parameters schema:
```json
{
  "name": "get_balance",
  "description": "Retrieve active bank balance for user_id",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string"
      }
    },
    "required": ["user_id"]
  }
}
```

---

## Common Patterns Used in AI Agent Frameworks

Below is a comparison of design patterns commonly found in production-grade agent frameworks:

<ComparisonTable headers={["Pattern", "Description", "Code Example"]} rows={[["Model Context Protocol (MCP)", "Standardized protocol to list and call tools using JSON-RPC over HTTP/SSE.", "ep04_lambda_mcp_server.py"], ["Supervisor Delegation", "A parent agent routes tasks to specialized child agents, shielding tools.", "ep02_production_supervisor.py"], ["Token Budgeting", "Tracking and limiting token usage to prevent infinite routing loops.", "ep02_production_supervisor.py"], ["Identity Propagation", "Passing user identity claims (JWT) down to sub-agent tools for validation.", "ep05_auth_middleware.py"], ["Episodic Vector Memory", "Saving conversation snippets in vector stores and retrieving them using cosine similarity.", "ep12_semantic_memory.py"]]} />

---

## Reading Real Agent Code

Let's examine how these concepts are structured inside the codebase. Below are walk-through guides of real agent handlers.

### 1. Simple Agent (`ep01_simple_agent.py`)
Executes basic LLM API queries, formats prompts, handles response parsing, and catches runtime client rate limits.
```python
import os
import json
import boto3

# Initialize system client
bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))

def run_agent(prompt: str) -> dict:
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "temperature": 0.7,
            "maxTokenCount": 512
        }
    })
    
    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=body
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        return {"status": "success", "text": response_body["results"][0]["outputText"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 2. Multi-Agent Supervisor (`ep02_production_supervisor.py`)
Coordinates task delegation, executing concurrent async worker agent routines, and tracking overall token boundaries.
```python
import asyncio
from dataclasses import dataclass

@dataclass
class AgentTask:
    task_id: str
    prompt: str

class Supervisor:
    def __init__(self, workers):
        self.workers = workers
        
    async def delegate(self, tasks: list[AgentTask]):
        # Run worker routines concurrently
        results = await asyncio.gather(*[
            self.workers[idx % len(self.workers)].run(task.prompt)
            for idx, task in enumerate(tasks)
        ])
        return results
```

---

## Building Your First Agent
To create your first BedrockAgentCore tool, follow these steps:
1. Define a Pydantic class representing input parameters.
2. Define a function with descriptive type hints and a docstring.
3. Decorate the function with `@tool` to register it.

```python
from pydantic import BaseModel, Field

class CalculateInterestInput(BaseModel):
    principal: float = Field(description="The starting principal amount")
    rate: float = Field(description="Annual interest rate as decimal (e.g. 0.05)")
    years: int = Field(description="Investment period in years")

@tool
def calculate_interest(params: CalculateInterestInput) -> float:
    \"\"\"Calculate compound interest based on principal, rate, and investment period.\"\"\"
    return params.principal * ((1 + params.rate) ** params.years)
```

---

## Best Practices
- **Least Privilege**: Always restrict agent tools to sandbox environments with limited system access permissions.
- **Token Boundaries**: Implement strict token budget rules to prevent routing loops from racking up high usage bills.
- **Resource Constraints**: Run agent code in container clusters with set memory limits to prevent Out-Of-Memory system crashes.

---

## Common Errors
- **KeyError in Parser**: Occurs when LLM outputs fail to output fields specified in target JSON schemas. Always wrap parser calls in safe try-except blocks.
- **ImportError in Runtimes**: Occurs when packages inside dynamic user modules are missing from virtual environments. Double-check requirements.

---

## Interview Questions
<InterviewQuestions>
  <InterviewQuestion q="Explain the difference between synchronous blocking IO and asynchronous non-blocking IO in agent systems." a="Synchronous blocking IO stalls execution, freezing the runtime while waiting for remote APIs to reply. Asynchronous non-blocking IO allows the engine to request multiple API queries concurrently on a single event loop thread, speeding up execution." />
  <InterviewQuestion q="What is a tool registration schema, and how is it generated?" a="A tool registration schema describes a function name, input fields, types, and descriptions to an LLM. It is generated by inspecting type annotations and docstrings using reflection libraries." />
</InterviewQuestions>

---

## Cheat Sheet
| Syntax | Pattern | Description |
|---|---|---|
| `async def` | Async execution | Defines non-blocking coroutines |
| `await` | Event yield | Pauses coroutine execution until result resolves |
| `@tool` | Tool binder | Auto-generates schemas for LLMs |
| `logging.info` | Structured Logging | Logs structured objects to tracers |
"""

final_content = original_content + "\n\n" + ai_agents_section + concepts_body + "\n" + tail_sections

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(final_content)

print("Generated interactive AI Agents section in python.md successfully!")
