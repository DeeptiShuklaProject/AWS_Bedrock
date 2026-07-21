import os
import re
import json

python_md_path = r"c:\Users\nishu\workspace\wscs_bedrock\doc_replica_product_developer\doc_replica_fullstackdeveloper\backend\languages\python.md"

# 26 Topics Database
TOPICS_DATA = {
    "Variables": {
        "playground_code": """import json
# Simulating dynamic parsing and reassignment of dynamic parameters in an agent tool call
raw_payload = '{"agent_name": "Auditor", "token_limit": 4096}'
config = json.loads(raw_payload)
# Reassign and cast dynamically
config["token_limit"] = int(config["token_limit"])
print(f"Agent: {config['agent_name']} (Tokens: {config['token_limit']})")""",
        "playground_instruction": "Run this advanced example showing dynamic reassignment and type casting of JSON payloads in LLM tool outputs.",
        "quiz": {
            "question": "Which of the following occurs under the hood when a Python variable is reassigned to a different data type?",
            "options": [
                "The memory occupied by the original object is immediately freed, and the variable is modified to point to the new type.",
                "Python creates a new object in memory, rebinds the variable reference, and decrements the original object's reference counter.",
                "The virtual machine throws a runtime TypeError because Python is dynamically typed.",
                "Python reuses the same memory address but changes the internal type header of the original object."
            ],
            "answerIndex": 1,
            "explanation": "Python variables are references. Reassigning a variable creates a new object and updates the variable to point to it, decrementing the reference count on the previous object."
        }
    },
    "Functions": {
        "playground_code": """def execute_agent_tool(tool_func, *args, **kwargs):
    # Dynamically unpack and execute a tool with arbitrary positional and keyword arguments
    print(f"Invoking {tool_func.__name__}...")
    return tool_func(*args, **kwargs)

def get_user(id, role="Guest"):
    return {"id": id, "role": role}

res = execute_agent_tool(get_user, "usr_99", role="Admin")
print(res)""",
        "playground_instruction": "Run this advanced example executing a tool with dynamic parameter unpacking using *args and **kwargs.",
        "quiz": {
            "question": "What is the structural difference between argument unpacking using *args and **kwargs in Python function definitions?",
            "options": [
                "*args unpacks a dictionary of keyword arguments, whereas **kwargs unpacks a list of positional arguments.",
                "*args packs excess positional arguments into a tuple, while **kwargs packs excess keyword arguments into a dictionary.",
                "*args creates an immutable generator sequence, while **kwargs creates a mutable set object.",
                "There is no difference; they can be used interchangeably to capture any parameter type."
            ],
            "answerIndex": 1,
            "explanation": "*args collects positional parameters into a tuple, while **kwargs collects keyword arguments into a standard dictionary."
        }
    },
    "Classes": {
        "playground_code": """class AgentMemory:
    # Class variable sharing a max limit across all agent instances
    GLOBAL_MAX_HISTORY = 100

    def __init__(self, agent_id):
        self.agent_id = agent_id  # Instance variable
        self.history = []

    def record(self, message):
        if len(self.history) < self.GLOBAL_MAX_HISTORY:
            self.history.append(message)

m1 = AgentMemory("Agent_A")
m1.record("Hello")
print(f"Memory length: {len(m1.history)}")""",
        "playground_instruction": "Run this example demonstrating the difference between class variables and instance variables in agent memory class setups.",
        "quiz": {
            "question": "If you modify a mutable class variable directly on a class instance (e.g. instance.class_var = new_val), what happens to other instances?",
            "options": [
                "All other instances automatically see the new value of the class variable.",
                "The class variable is modified globally across all instances, including the base class definition.",
                "A new instance variable of the same name is created, shadowing the class variable on that specific instance only.",
                "The Python interpreter raises an AttributeError for invalid modification."
            ],
            "answerIndex": 2,
            "explanation": "Assigning to a class variable via an instance creates a new instance variable of the same name on that specific instance, shadowing the class variable."
        }
    },
    "OOP": {
        "playground_code": """from abc import ABC, abstractmethod

class AgentBase(ABC):
    @abstractmethod
    def step(self): pass

class LoggerMixin:
    def log_step(self, status):
        print(f"[LOG] Step completed with status: {status}")

class AutonomousAgent(AgentBase, LoggerMixin):
    def step(self):
        self.log_step("Success")
        return "Done"

agent = AutonomousAgent()
agent.step()""",
        "playground_instruction": "Run this example utilizing abstract base classes and logging mixins with multiple inheritance.",
        "quiz": {
            "question": "What is the primary role of Method Resolution Order (MRO) when calling a method on a class that uses multiple inheritance?",
            "options": [
                "MRO compiles the parent classes in parallel to execute duplicate methods simultaneously.",
                "MRO defines the search order Python follows to look up attributes/methods, traversing the class hierarchy deterministically via C3 linearization.",
                "MRO blocks subclasses from overriding any abstract methods defined in the parent class hierarchy.",
                "MRO resolves naming conflicts by automatically renaming duplicate methods at compile time."
            ],
            "answerIndex": 1,
            "explanation": "MRO uses the C3 linearization algorithm to determine a clean, deterministic linear list of parent classes to search when resolving attributes and methods."
        }
    },
    "Modules": {
        "playground_code": """import importlib
# Dynamically import standard math module and execute sqrt
math_module = importlib.import_module("math")
square_root = getattr(math_module, "sqrt")
print(f"Result: {square_root(144)}")""",
        "playground_instruction": "Run this example showing how to dynamically load modules and execute functions at runtime.",
        "quiz": {
            "question": "Why does Python cache imported modules in sys.modules instead of loading them each time an import statement is encountered?",
            "options": [
                "To enforce private visibility modifiers for local package variables.",
                "To optimize performance by avoiding duplicate code compilation and execution of module-level statements.",
                "To prevent global variables from being reassigned in subsequent modules.",
                "Because Python cannot parse import statements inside local function scopes."
            ],
            "answerIndex": 1,
            "explanation": "When a module is imported, Python compiles and executes it, saving the resulting module object in sys.modules. Subsequent imports retrieve the cached object, saving resources."
        }
    },
    "Packages": {
        "playground_code": """import sys
# Inspecting path resolution; packages are loaded from paths in sys.path
print("First search directory:", sys.path[0])""",
        "playground_instruction": "Run this example inspecting package paths and demonstrating package path manipulations.",
        "quiz": {
            "question": "Which of the following is a characteristic of Python namespace packages (introduced in Python 3.3 via PEP 420)?",
            "options": [
                "They must contain an empty __init__.py file in their root directory.",
                "They allow splitting a single logical package across multiple independent directory paths on disk without an __init__.py file.",
                "They require compiling directories into binary files before imports work.",
                "They are only accessible within virtual environment installations."
            ],
            "answerIndex": 1,
            "explanation": "Namespace packages do not require an __init__.py file, permitting files across different directories or zip files to be combined under a single logical package namespace."
        }
    },
    "Decorators": {
        "playground_code": """import time
import functools

def retry_tool(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i+1} failed: {e}")
            return None
        return wrapper
    return decorator

@retry_tool(retries=2)
def call_unstable_api():
    raise RuntimeError("API Timeout")

call_unstable_api()""",
        "playground_instruction": "Run this example creating a parameterized decorator to automatically retry unstable API operations.",
        "quiz": {
            "question": "When stacking decorators (e.g. applying @decorator1 above @decorator2 on a function), what is the evaluation order?",
            "options": [
                "They run concurrently using multithreaded handlers.",
                "@decorator1 executes first, wrapping the raw function, and then @decorator2 wraps the result.",
                "@decorator2 executes first, wrapping the raw function, and then @decorator1 wraps the resulting decorator function.",
                "Python randomly determines the execution order at runtime."
            ],
            "answerIndex": 2,
            "explanation": "Decorators are evaluated from bottom to top. The function is passed to the closest decorator first: decorator1(decorator2(func))."
        }
    },
    "Context Managers": {
        "playground_code": """from contextlib import contextmanager
import threading

lock = threading.Lock()

@contextmanager
def safe_session_scope():
    print("Acquiring thread lock...")
    lock.acquire()
    try:
        yield "Active Session"
    finally:
        print("Releasing thread lock...")
        lock.release()

with safe_session_scope() as session:
    print(f"Working in: {session}")""",
        "playground_instruction": "Run this example utilizing a generator-based context manager to create a safe, synchronized execution block.",
        "quiz": {
            "question": "If an exception is raised inside a with block, how must the context manager's __exit__(self, exc_type, exc_val, exc_tb) method behave to allow the exception to bubble up normally?",
            "options": [
                "It must return True.",
                "It must raise the exception again manually using the raise keyword inside __exit__.",
                "It must return False (or return nothing, which evaluates to None/False).",
                "It must delete the exception parameters from the traceback memory."
            ],
            "answerIndex": 2,
            "explanation": "Returning False (or None) from __exit__ tells Python not to suppress the exception, letting it bubble up. Returning True suppresses the exception."
        }
    },
    "Exception Handling": {
        "playground_code": """class ToolExecutionError(Exception): pass

try:
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        # Exception chaining to preserve context traceback
        raise ToolExecutionError("Agent tool failed to compute") from e
except ToolExecutionError as outer:
    print(f"Caught: {outer}")
    print(f"Original Cause: {outer.__cause__}")""",
        "playground_instruction": "Run this example illustrating exception chaining and causal tracebacks in python error handling.",
        "quiz": {
            "question": "In a try-except-else-finally structure, when does the else block execute?",
            "options": [
                "Only when an exception is raised and successfully caught.",
                "Always, right before the finally block executes.",
                "Only when the try block executes successfully without raising any exceptions.",
                "Only if the finally block encounters an error."
            ],
            "answerIndex": 2,
            "explanation": "The else block executes after the code in the try block finishes, but only if no exceptions were raised during its execution."
        }
    },
    "Typing": {
        "playground_code": """from typing import Protocol

class ExecutableAgent(Protocol):
    # Protocol defines structural subtyping (duck typing)
    def execute(self, payload: dict) -> str: ...

class Worker:
    def execute(self, payload: dict) -> str:
        return "Worker complete"

def run_agent(agent: ExecutableAgent):
    return agent.execute({})

print(run_agent(Worker()))""",
        "playground_instruction": "Run this example utilizing typing.Protocol to implement structural subtyping constraints.",
        "quiz": {
            "question": "What is the key difference between typing.Protocol (Structural typing) and standard abstract base classes (Nominal typing)?",
            "options": [
                "Protocol is enforced at runtime, while abstract base classes are ignored.",
                "Protocol does not require classes to inherit from it explicitly; any class implementing the required methods matches the Protocol.",
                "Abstract base classes cannot declare concrete methods, while Protocol can.",
                "Protocol only supports basic integer types."
            ],
            "answerIndex": 1,
            "explanation": "Protocol implements structural subtyping (duck typing). A class matches a Protocol simply by having matching method signatures, without explicit inheritance."
        }
    },
    "Async Programming": {
        "playground_code": """import asyncio

async def agent_action(name, duration):
    await asyncio.sleep(duration)
    return f"{name} task done"

async def run_pipeline():
    try:
        # Run concurrently with a timeout constraint
        results = await asyncio.wait_for(
            asyncio.gather(agent_action("A", 0.5), agent_action("B", 0.8)),
            timeout=1.0
        )
        print(results)
    except asyncio.TimeoutError:
        print("Pipeline timed out!")

asyncio.run(run_pipeline())""",
        "playground_instruction": "Run this example coordinating concurrent asynchronous tasks with timeout constraints.",
        "quiz": {
            "question": "What happens if a developer runs a CPU-heavy computation loop (e.g. while True: pass) inside an asynchronous coroutine without using await?",
            "options": [
                "The event loop automatically offloads the loop to a background CPU process.",
                "The thread running the event loop is blocked, freezing all other concurrent tasks until the loop completes.",
                "The coroutine raises a RuntimeBlockingError.",
                "The execution continues in parallel using cooperative multitasking."
            ],
            "answerIndex": 1,
            "explanation": "Since asyncio runs on a single thread, blocking operations or CPU-bound loops without await block the entire thread, halting the event loop."
        }
    },
    "Dataclasses": {
        "playground_code": """from dataclasses import dataclass, field

@dataclass(frozen=True)
class ImmutableAgentConfig:
    agent_name: str
    # default_factory prevents shared mutable reference bugs
    tags: list[str] = field(default_factory=list)

config = ImmutableAgentConfig("Clara", ["search", "math"])
print(config)""",
        "playground_instruction": "Run this example defining immutable dataclasses and using default factories for mutable list fields.",
        "quiz": {
            "question": "Why does Python's dataclass raise a ValueError if you specify a mutable default parameter directly (like tags: list = [])?",
            "options": [
                "Because dataclasses are compiled into C structures that do not support lists.",
                "Because mutable defaults are evaluated once and shared across all class instances, leading to state leaks.",
                "Because lists cannot be type-hinted in Python dataclasses.",
                "Because dataclass fields must be defined as read-only constants."
            ],
            "answerIndex": 1,
            "explanation": "To prevent instance state sharing (since defaults are evaluated once at definition time), dataclasses require mutable defaults to use default_factory."
        }
    },
    "Enums": {
        "playground_code": """from enum import Enum, auto

class AgentState(Enum):
    IDLE = auto()
    THINKING = auto()
    COMPLETED = auto()
    
    def can_transition_to(self, new_state):
        # Custom routing validation
        return self != AgentState.COMPLETED

state = AgentState.THINKING
print("Can change to Completed?", state.can_transition_to(AgentState.COMPLETED))""",
        "playground_instruction": "Run this example declaring enums with custom status transition methods.",
        "quiz": {
            "question": "What is the primary difference between comparing Enum members using is vs comparing their values using ==?",
            "options": [
                "Comparing with is checks the Enum member instance identity, whereas == compares the underlying values.",
                "is comparisons are only supported for string Enums, while == is for integer Enums.",
                "is performs type coercion while == is strict.",
                "There is no difference; they are exactly identical in all contexts."
            ],
            "answerIndex": 0,
            "explanation": "Enum members are singletons, so member1 is member2 checks identity. Comparing member1.value == value checks the value assigned to the member."
        }
    },
    "Logging": {
        "playground_code": """import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Standardize log outputs as JSON objects
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        })

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("AgentLogger")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("JSON log initialization complete.")""",
        "playground_instruction": "Run this example setting up structured JSON logging in python applications.",
        "quiz": {
            "question": "What is the purpose of log propagation in Python's logging module?",
            "options": [
                "It duplicates log files across multiple server directories automatically.",
                "It passes log records up to the handlers of parent loggers in the logger hierarchy unless propagate is set to False.",
                "It converts all log formats to JSON structures.",
                "It encrypts logs before exporting them to standard output streams."
            ],
            "answerIndex": 1,
            "explanation": "Loggers are organized hierarchically. By default, events logged to child loggers are propagated up to their parents' handlers."
        }
    },
    "Environment Variables": {
        "playground_code": """import os

class AgentConfig:
    def __init__(self):
        # Safe retrieval with strict verification
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable is not set!")

try:
    config = AgentConfig()
except ValueError as e:
    print(e)""",
        "playground_instruction": "Run this example retrieving and validating environmental variable configs.",
        "quiz": {
            "question": "If you modify os.environ inside a running Python script, which processes are affected by this change?",
            "options": [
                "Only the current Python process and any sub-processes spawned by it after the modification.",
                "All system processes currently running on the operating system.",
                "The change is saved permanently to the OS environment settings.",
                "No processes, as os.environ is read-only at runtime."
            ],
            "answerIndex": 0,
            "explanation": "Environment modifications are local to the process and inherited by its child processes. They do not affect parent or unrelated system processes."
        }
    },
    "Virtual Environments": {
        "playground_code": """import sys
# Check if we are running inside an active virtual environment
is_venv = sys.prefix != sys.base_prefix
print(f"Inside virtual environment: {is_venv}")""",
        "playground_instruction": "Run this example programmatically checking if python execution environment is virtualized.",
        "quiz": {
            "question": "How does activating a virtual environment (.venv) change the interpreter's package discovery path?",
            "options": [
                "It updates sys.path to prioritize directories within the virtual environment's site-packages folder.",
                "It copies all installed libraries into the system's root Python directory.",
                "It compiles python files into native shell commands.",
                "It blocks standard library modules from being loaded."
            ],
            "answerIndex": 0,
            "explanation": "Activation modifies environment paths (PATH, VIRTUAL_ENV) so that the interpreter resolves packages from the virtual environment's directories."
        }
    },
    "Pip": {
        "playground_code": """import subprocess
import sys

# Programmatically execute pip list using subprocess
res = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
print("Pip Package Check:")
print("\\n".join(res.stdout.splitlines()[:5]))""",
        "playground_instruction": "Run this example executing pip packages list checks programmatically.",
        "quiz": {
            "question": "What is the primary purpose of using requirements constraints (e.g. pydantic>=2.0,<3.0) in a requirements.txt file?",
            "options": [
                "To speed up the network download speed of libraries.",
                "To prevent breaking changes by locking updates to compatible major/minor versions while permitting bug fixes.",
                "To compile dependencies into binary wheels before installing.",
                "To force pip to run only inside a Docker container."
            ],
            "answerIndex": 1,
            "explanation": "Constraints ensure that compatible versions are installed (e.g. avoiding major breaking versions), preventing dependency drift and runtime breaks."
        }
    },
    "UV": {
        "playground_code": """# Simulating a uv-based virtual env setup check
import sys
print("UV packages are resolved in optimized, concurrent caches.")
print("Interpreter:", sys.executable)""",
        "playground_instruction": "Run this example demonstrating UV environment path variables.",
        "quiz": {
            "question": "How does UV achieve significant performance gains over traditional pip when installing packages?",
            "options": [
                "It skips resolving dependencies entirely and copies files directly.",
                "It is written in Rust, resolves dependencies concurrently, and uses global cache links (hard links/reflink) to avoid copying files.",
                "It executes only inside web browser interpreters.",
                "It compresses package archives using a custom algorithm before download."
            ],
            "answerIndex": 1,
            "explanation": "UV leverages Rust concurrency and global caching with system file links (reflink or hard link) to make installs extremely fast and resource-efficient."
        }
    },
    "Poetry": {
        "playground_code": """# Simulating reading project config from pyproject.toml
project_config = \"\"\"
[tool.poetry.dependencies]
python = "^3.11"
pydantic = "^2.5.0"
\"\"\"
print("Parsed pyproject.toml layout:")
print(project_config.strip())""",
        "playground_instruction": "Run this example displaying sample Poetry config files layout structures.",
        "quiz": {
            "question": "What security role does the poetry.lock file play in package deployments?",
            "options": [
                "It encrypts all code files before sending them to production.",
                "It records exact package versions along with cryptographic content hashes to ensure identical and secure builds.",
                "It locks file permissions to prevent unauthorised users from editing code.",
                "It logs all active API keys in a secure dashboard."
            ],
            "answerIndex": 1,
            "explanation": "The lockfile ensures reproducibility and security by pinning the exact package version and storing file hashes to verify that installed code hasn't been altered."
        }
    },
    "JSON": {
        "playground_code": """import json
from datetime import datetime

class AgentJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

payload = {"timestamp": datetime.now(), "status": "active"}
print(json.dumps(payload, cls=AgentJsonEncoder))""",
        "playground_instruction": "Run this example utilizing custom JSON encoders for non-serializable objects (datetime).",
        "quiz": {
            "question": "Which error does Python's standard json.dumps() throw when attempting to serialize a custom object without a custom encoder?",
            "options": [
                "AttributeError",
                "TypeError",
                "ValueError",
                "SerializationError"
            ],
            "answerIndex": 1,
            "explanation": "A TypeError is raised when an object of a non-serializable type (like custom class instances or datetime) is passed to json.dumps()."
        }
    },
    "HTTP APIs": {
        "playground_code": """import httpx
import asyncio

async def check_api_status():
    # Reusing an async HTTP client session
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://httpbin.org/status/200")
        print(f"Status Code: {resp.status_code}")

asyncio.run(check_api_status())""",
        "playground_instruction": "Run this example executing concurrent API calls using httpx.",
        "quiz": {
            "question": "What is a major advantage of using HTTPX's connection pooling via Client sessions over individual request calls?",
            "options": [
                "It automatically encrypts request parameters.",
                "It reuses established TCP connections, reducing network latency and handshaking overhead.",
                "It bypasses system firewall constraints.",
                "It translates HTTP requests into GraphQL queries."
            ],
            "answerIndex": 1,
            "explanation": "Connection pooling reuses TCP connections, avoiding the overhead of opening and closing connections for each request, enhancing API performance."
        }
    },
    "FastAPI Basics": {
        "playground_code": """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptInput(BaseModel):
    text: str

@app.post("/agent")
async def run_agent_route(payload: PromptInput):
    return {"response": f"Processed: {payload.text}"}

print("FastAPI agent route registered successfully.")""",
        "playground_instruction": "Run this example showing route mappings and request body models configurations in FastAPI.",
        "quiz": {
            "question": "What is ASGI, and how does it differ from WSGI in Python web framework architectures?",
            "options": [
                "ASGI is faster because it compiles Python to native C++.",
                "ASGI is an asynchronous interface supporting WebSockets, Server-Sent Events, and async routing, whereas WSGI is synchronous.",
                "ASGI only runs on cloud systems, while WSGI runs locally.",
                "WSGI is the newer, asynchronous standard that replaced ASGI."
            ],
            "answerIndex": 1,
            "explanation": "ASGI (Asynchronous Server Gateway Interface) supports async Python features (like websockets and async tasks), while WSGI is limited to synchronous requests."
        }
    },
    "Pydantic": {
        "playground_code": """from pydantic import BaseModel, Field, field_validator

class AgentTask(BaseModel):
    task_id: str
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator("task_id")
    def check_id_prefix(cls, val):
        if not val.startswith("task_"):
            raise ValueError("task_id must start with 'task_' prefix")
        return val

try:
    task = AgentTask(task_id="invalid_id", priority=10)
except Exception as e:
    print(e)""",
        "playground_instruction": "Run this example showing strict field validations and validators checks using Pydantic schemas.",
        "quiz": {
            "question": "How does Pydantic behave when performing field validation under Strict Mode (strict=True)?",
            "options": [
                "It coerces values (e.g. converting '42' to 42) before validating.",
                "It fails validation immediately if the input type does not match the type annotation exactly.",
                "It compiles model declarations into binary executables.",
                "It ignores all custom field validators."
            ],
            "answerIndex": 1,
            "explanation": "In strict mode, Pydantic prevents automatic type coercion (like casting string numbers or floats to ints), raising validation errors if types aren't exact."
        }
    },
    "Dependency Injection": {
        "playground_code": """# Simulating a dependency override check for unit tests
def get_real_db():
    return "Production_Database_Connection"

def execute_query(db_conn=None):
    conn = db_conn or get_real_db()
    print("Connecting to:", conn)

# Injecting a mock connection
execute_query(db_conn="Mock_Test_Connection")""",
        "playground_instruction": "Run this example demonstrating manual dependency injection configuration and overrides simulation.",
        "quiz": {
            "question": "In FastAPI, how are dependency overrides specified for test clients during integration testing?",
            "options": [
                "By modifying the sys.path list.",
                "By assigning override functions to the app.dependency_overrides dictionary map.",
                "By deleting the standard dependency definitions.",
                "By compiling the application in Test mode."
            ],
            "answerIndex": 1,
            "explanation": "FastAPI provides a dictionary app.dependency_overrides. Mapping a dependency callable to a mock callable redirects the resolver automatically."
        }
    },
    "File Handling": {
        "playground_code": """from pathlib import Path

# Secure path resolution, preventing directory traversal attacks
base_dir = Path("/app/sandbox").resolve()
user_input = "output.txt"

# Join and resolve
target_file = (base_dir / user_input).resolve()
is_safe = target_file.is_relative_to(base_dir)
print(f"Path resolved to: {target_file}")
print(f"Is path safe (within sandbox)? {is_safe}")""",
        "playground_instruction": "Run this example using pathlib.Path to prevent path traversal vulnerability security risks.",
        "quiz": {
            "question": "Why is Path.resolve() crucial when validating user-supplied file paths in backend applications?",
            "options": [
                "It compiles path strings to binary bytes.",
                "It resolves symbolic links and relative segments (like '..'), returning the absolute path to detect path traversal attempts.",
                "It automatically creates the file on disk if it is missing.",
                "It limits the maximum file read size to 10MB."
            ],
            "answerIndex": 1,
            "explanation": "resolve() produces the absolute canonical path, eliminating symlink aliases and traversal tokens (..), allowing clean safety boundaries checks."
        }
    },
    "Package Structure": {
        "playground_code": """# Simulating path resolution checks in src package layouts
import sys
print("System search paths listing:")
print("\\n".join(sys.path[:3]))""",
        "playground_instruction": "Run this example showing system search paths configurations in package distributions structures.",
        "quiz": {
            "question": "Why is the src/ layout configuration considered a best practice in Python packaging?",
            "options": [
                "It decreases package size.",
                "It forces tests to run against the installed package version from site-packages rather than raw local source files.",
                "It makes relative imports simpler.",
                "It is required by the Python interpreter."
            ],
            "answerIndex": 1,
            "explanation": "The src/ layout forces developers to install the package before tests run, helping identify configuration/packaging bugs before release."
        }
    }
}

def enrich_python_file():
    with open(python_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split python.md into prefix, main body (26 topics), and suffix
    # The 26 topics section starts after `# Python for AI Agents (Beginner to Advanced)`
    split_term_1 = "# Python for AI Agents (Beginner to Advanced)"
    parts_1 = content.split(split_term_1)
    
    if len(parts_1) != 2:
        print("Could not find start split term!")
        return
        
    prefix = parts_1[0] + split_term_1
    body_and_suffix = parts_1[1]
    
    split_term_2 = "## Agent Architecture with Python"
    parts_2 = body_and_suffix.split(split_term_2)
    
    if len(parts_2) != 2:
        print("Could not find end split term!")
        return
        
    body = parts_2[0]
    suffix = split_term_2 + parts_2[1]

    # Process all topics in the body
    # We will split the body by '### '
    # Note: The first element in the split is everything between the split_term_1 and the first topic
    sub_parts = body.split("### ")
    
    new_sub_parts = [sub_parts[0]]
    
    for part in sub_parts[1:]:
        # Find which topic this is. The topic name is the first line of the part.
        lines = part.split("\n", 1)
        topic_name = lines[0].strip()
        
        # Strip trailing # or sub-formatting if any (none in python.md)
        if topic_name in TOPICS_DATA:
            data = TOPICS_DATA[topic_name]
            part_content = part
            
            # --- 1. Add Advanced Playground to Tabs ---
            # Search for </Tabs>
            # We want to insert the new Tab right before </Tabs>
            escaped_code = json.dumps(data["playground_code"])[1:-1]
            new_tab_str = f"""
  <Tab label="Advanced Playground">
    <InteractiveExample 
      language="python"
      initialCode="{escaped_code}" 
      instruction="{data["playground_instruction"]}"
    />
  </Tab>
</Tabs>"""
            # Replace the last </Tabs> in this section with the new tab + </Tabs>
            if "</Tabs>" in part_content:
                # We replace the first occurrence (should only be one per section)
                part_content = part_content.replace("</Tabs>", new_tab_str, 1)
            else:
                print(f"Warning: </Tabs> not found in {topic_name}!")

            # --- 2. Add Quiz 2 right below Quiz 1 ---
            # The existing quiz component ends with '/>'
            # Let's find '<Quiz' and its closing '/>'
            # To be safe, let's find the closing '/>' of the Quiz component
            quiz_match = re.search(r'(<Quiz\s+.*?\n/>)', part_content, re.DOTALL)
            if quiz_match:
                existing_quiz = quiz_match.group(1)
                options_str = json.dumps(data["quiz"]["options"])
                escaped_question = json.dumps(data["quiz"]["question"])[1:-1]
                escaped_explanation = json.dumps(data["quiz"]["explanation"])[1:-1]
                
                new_quiz_str = f"""
<Quiz 
  question="{escaped_question}" 
  options={options_str} 
  answerIndex={data["quiz"]["answerIndex"]} 
  explanation="{escaped_explanation}" 
/>"""
                # Insert the new quiz right after the existing one
                part_content = part_content.replace(existing_quiz, f"{existing_quiz}\n{new_quiz_str}", 1)
            else:
                print(f"Warning: Quiz component not found in {topic_name}!")
                
            new_sub_parts.append(part_content)
        else:
            print(f"Unknown topic or section header: '{topic_name}'")
            new_sub_parts.append(part)

    new_body = "### ".join(new_sub_parts)
    final_content = prefix + new_body + suffix

    with open(python_md_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("python.md successfully enriched!")

if __name__ == "__main__":
    enrich_python_file()
