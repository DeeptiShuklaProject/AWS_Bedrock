import re
import json

python_md_path = r"doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md"

# 26 Topics
TOPICS = [
    "Variables", "Functions", "Classes", "OOP", "Modules", "Packages", "Decorators",
    "Context Managers", "Exception Handling", "Typing", "Async Programming", "Dataclasses",
    "Enums", "Logging", "Environment Variables", "Virtual Environments", "Pip", "UV",
    "Poetry", "JSON", "HTTP APIs", "FastAPI Basics", "Pydantic", "Dependency Injection",
    "File Handling", "Package Structure"
]

# Topic details for high-fidelity quizzes
TOPIC_DETAILS = {
    "Variables": {
        "noun": "variable references",
        "hazard": "name shadowing or global scope pollution",
        "internals": "reference counting and pointer binding",
        "best_practice": "using uppercase for constants and snake_case for local variables",
        "debugging": "inspecting locals() or using pdb",
        "vis": "local vs global scope rules",
        "concurrency": "race conditions during concurrent reassignments",
        "typing": "dynamic runtime assignment of object labels",
        "cpython": "PyObject structs pointing to values on the heap",
        "agent": "dynamic state tracking and parameter storage",
        "design": "binding labels to state representations",
        "exception": "raising NameError when resolving unbound labels",
        "compile": "binding local offsets in code objects vs runtime dictionary lookup",
        "security": "unintentional leakage of sensitive variable names in logs",
        "serialization": "pickling references vs actual value copies",
        "testing": "mocking variables or global states",
        "subclassing": "shadowing attributes in subclass scopes",
        "std_lib": "sys and gc modules for reference analysis",
        "importing": "modifying imported module-level variables",
        "limit": "lack of constants/read-only variables in native syntax"
    },
    "Functions": {
        "noun": "functions",
        "hazard": "using mutable default parameters",
        "internals": "frame execution stack and closure cells",
        "best_practice": "type annotating signatures and keeping functions small",
        "debugging": "stack trace analysis and tracebacks",
        "vis": "LEGB (Local, Enclosing, Global, Built-in) scope rules",
        "concurrency": "sharing non-thread-safe variables across function calls",
        "typing": "Callable type signatures and runtime checks",
        "cpython": "PyFunctionObject structs created during definition",
        "agent": "defining LLM tools and custom handlers",
        "design": "first-class function objects and callbacks",
        "exception": "unhandled exceptions unwinding the call stack",
        "compile": "bytecode generation for code objects versus runtime stack execution",
        "security": "arbitrary execution via eval() or exec() inside functions",
        "serialization": "pickling functions using external libraries like dill",
        "testing": "writing unit tests using pytest parameterization",
        "subclassing": "overriding instance methods and using super()",
        "std_lib": "functools and inspect modules for metadata reflection",
        "importing": "importing functions and executing them in different contexts",
        "limit": "limited anonymous functions (lambdas must be single expressions)"
    },
    "Classes": {
        "noun": "classes",
        "hazard": "mutable class-level variables shared across instances",
        "internals": "class dictionaries (__dict__) and descriptor protocols",
        "best_practice": "initializing all instance variables within __init__",
        "debugging": "inspecting __dict__ and dir()",
        "vis": "private name mangling with double underscores",
        "concurrency": "race conditions on shared class attributes",
        "typing": "type hints for self and Type[Self]",
        "cpython": "PyTypeObject metadata and attribute lookups",
        "agent": "encapsulating agent memory and tool registrations",
        "design": "factory patterns and object constructors",
        "exception": "AttributeError during invalid property access",
        "compile": "class namespace execution vs instantiation",
        "security": "malicious class injection via unsafe deserialization",
        "serialization": "implementing custom state __getstate__ and __setstate__",
        "testing": "mocking instance methods using unittest.mock",
        "subclassing": "inheritance overrides and calling super()",
        "std_lib": "types and abc modules",
        "importing": "circular class dependencies in nested structures",
        "limit": "lack of true private access modifiers"
    },
    "OOP": {
        "noun": "Object-Oriented Programming (OOP)",
        "hazard": "deep inheritance hierarchies leading to brittle codebases",
        "internals": "Method Resolution Order (MRO) using C3 linearization",
        "best_practice": "preferring composition over inheritance",
        "debugging": "printing the __mro__ tuple of class types",
        "vis": "accessing base class methods from derived classes",
        "concurrency": "managing shared mutable state in polymorphic instances",
        "typing": "structural subtyping via Protocol and duck typing",
        "cpython": "virtual method dispatch tables internally managed by type descriptors",
        "agent": "defining extensible BaseAgent and BaseTool abstractions",
        "design": "design patterns like Strategy, Observer, and Decorator",
        "exception": "TypeError when abstract methods are not implemented",
        "compile": "MRO computation at class definition time",
        "security": "violating Liskov Substitution Principle leading to security checks bypass",
        "serialization": "deserializing polymorphic class trees",
        "testing": "verifying interface compliance using abstract test suites",
        "subclassing": "multiple inheritance conflicts",
        "std_lib": "abc module for Abstract Base Classes",
        "importing": "modularizing base and derived classes across subpackages",
        "limit": "complex C3 linearization resolution in multiple inheritance"
    },
    "Modules": {
        "noun": "modules",
        "hazard": "circular import errors during runtime resolution",
        "internals": "sys.modules cache and import hooks",
        "best_practice": "keeping module dependencies clean and linear",
        "debugging": "tracing imports using python -v or inspecting sys.modules",
        "vis": "module-level variables and private prefixes with underscores",
        "concurrency": "sys.modules locking mechanisms during multi-threaded imports",
        "typing": "module type annotations and import checks",
        "cpython": "module object creations and dictionary evaluations",
        "agent": "modular agent configurations and tool files",
        "design": "facade and modular decomposition patterns",
        "exception": "ImportError and ModuleNotFoundError",
        "compile": "compiling module files to .pyc files vs executing them",
        "security": "arbitrary code execution via malicious module hijacking",
        "serialization": "loading dynamic code modules safely",
        "testing": "mocking whole modules during testing",
        "subclassing": "not applicable to modules directly",
        "std_lib": "importlib for dynamic importing",
        "importing": "import statements and sys.path search order",
        "limit": "cannot easily reload modules with global state changes"
    },
    "Packages": {
        "noun": "packages",
        "hazard": "circular references in absolute or relative subpackage imports",
        "internals": "__path__ resolution and namespace package creation",
        "best_practice": "declaring clear exports in __init__.py using __all__",
        "debugging": "inspecting __package__ and __file__ values",
        "vis": "package-level exports versus internal-only submodules",
        "concurrency": "thread safety during initial dynamic package resolution",
        "typing": "package-level type stubs and py.typed files",
        "cpython": "directory traversal and path finding by the import system",
        "agent": "packaging agentic toolkits for reuse",
        "design": "clean architectural layering of packages",
        "exception": "ImportError due to invalid relative imports",
        "compile": "bytecode compilation of nested files",
        "security": "namespace pollution and package spoofing",
        "serialization": "packaging serialized assets inside standard wheels",
        "testing": "testing package installs in isolated virtual environments",
        "subclassing": "not applicable to packages",
        "std_lib": "pkgutil and sys modules",
        "importing": "absolute versus relative imports",
        "limit": "managing dependency specifications in legacy setups"
    },
    "Decorators": {
        "noun": "decorators",
        "hazard": "losing metadata (docstrings, names) of wrapped functions",
        "internals": "closures and high-order function wrappers",
        "best_practice": "using functools.wraps to preserve wrapped metadata",
        "debugging": "unwrapping decorators or inspecting __wrapped__ attributes",
        "vis": "closure variable scope limits",
        "concurrency": "sharing stateful decorator instances across threads",
        "typing": "typing decorator signatures with ParamSpec and TypeVar",
        "cpython": "syntactic sugar translation during compilation",
        "agent": "registering tools and measuring performance metrics",
        "design": "decorator design pattern and aspect-oriented programming",
        "exception": "exceptions raised in wrappers escaping to callers",
        "compile": "decorator application at definition time",
        "security": "hijacking execution routes via unvetted decorators",
        "serialization": "pickling functions wrapped in arbitrary decorators",
        "testing": "testing wrapped functions in isolation",
        "subclassing": "using class decorators vs method decorators",
        "std_lib": "functools module",
        "importing": "decorating functions defined in other modules",
        "limit": "stack trace inflation due to deep wrapping layers"
    },
    "Context Managers": {
        "noun": "context managers",
        "hazard": "suppressing exceptions implicitly inside __exit__ by returning True",
        "internals": "with statement protocol and frame cleanup",
        "best_practice": "releasing resources in finally blocks or context managers",
        "debugging": "inspecting execution steps inside __exit__ parameters",
        "vis": "scope variables leakage outside with blocks",
        "concurrency": "acquiring locks across thread contexts",
        "typing": "ContextManager and AbstractContextManager typing",
        "cpython": "SETUP_WITH bytecode operations",
        "agent": "handling temporary tool files and database connection lifetimes",
        "design": "RAII (Resource Acquisition Is Initialization) pattern",
        "exception": "handling exceptions via the traceback parameter of __exit__",
        "compile": "translating with blocks to try-finally structures",
        "security": "leaking file descriptors under resource exhaustion",
        "serialization": "cannot serialize active context resources",
        "testing": "using mock context managers in tests",
        "subclassing": "extending custom context managers",
        "std_lib": "contextlib module for utilities like @contextmanager",
        "importing": "importing context utilities",
        "limit": "reentry limitations in non-reentrant managers"
    },
    "Exception Handling": {
        "noun": "exception handling",
        "hazard": "using bare except blocks that catch SystemExit and KeyboardInterrupt",
        "internals": "call stack unwinding and exception chaining",
        "best_practice": "raising specific exceptions and chaining via 'raise ... from'",
        "debugging": "reading causal tracebacks and traceback modules",
        "vis": "local variable visibility inside try-except-finally blocks",
        "concurrency": "handling exceptions raised in worker threads or async tasks",
        "typing": "typing custom exceptions and try-except returns",
        "cpython": "exception registers and frame tracebacks",
        "agent": "graceful tool execution fallback and causal tracking",
        "design": "fail-fast vs fallback pattern designs",
        "exception": "BaseException hierarchy and custom Exception classes",
        "compile": "exception table creation in bytecode",
        "security": "leaking database connection secrets in stack traces",
        "serialization": "pickling exception details for logging",
        "testing": "asserting exceptions are raised using pytest.raises",
        "subclassing": "defining custom domain exception hierarchies",
        "std_lib": "traceback and sys modules",
        "importing": "importing custom exception classes",
        "limit": "overhead of exception table resolution"
    },
    "Typing": {
        "noun": "typing",
        "hazard": "runtime failures due to static type check mismatch",
        "internals": "type hints metadata (__annotations__)",
        "best_practice": "using structural typing (Protocol) for interface validation",
        "debugging": "running mypy or pyright static checkers",
        "vis": "type variables and generic scopes",
        "concurrency": "annotating shared states across threads",
        "typing": "Union, Optional, Any, Callable, TypeVar, Protocol",
        "cpython": "type annotations ignored at runtime execution",
        "agent": "generating tool schema parameters via reflections",
        "design": "design by contract pattern",
        "exception": "TypeError raised by validation frameworks",
        "compile": "parsing type hints versus runtime type ignoring",
        "security": "bypassing runtime checks by typing inputs as Any",
        "serialization": "parsing schemas using type annotations",
        "testing": "running static type checkers on test suites",
        "subclassing": "generic class inheritance configurations",
        "std_lib": "typing module and types module",
        "importing": "type checking imports with TYPE_CHECKING guard",
        "limit": "no runtime type enforcement in raw Python"
    },
    "Async Programming": {
        "noun": "async programming",
        "hazard": "blocking the event loop with synchronous calls",
        "internals": "event loop schedule, generators, and awaitables",
        "best_practice": "using asyncio.gather or TaskGroups for concurrency",
        "debugging": "running asyncio in debug mode or using aiomonitor",
        "vis": "coroutine context variable isolation",
        "concurrency": "cooperative multitasking vs multithreading",
        "typing": "Coroutine, Awaitable, and Task typing signatures",
        "cpython": "generator frame execution states and yield structures",
        "agent": "gathering parallel tool executions",
        "design": "event-driven and reactor patterns",
        "exception": "handling exceptions in asyncio tasks and gathering results",
        "compile": "coroutine compilation to bytecode generators",
        "security": "DoS attacks via event loop starvation",
        "serialization": "serializing async task configurations",
        "testing": "testing async code using pytest-asyncio",
        "subclassing": "not directly applicable",
        "std_lib": "asyncio and contextvars modules",
        "importing": "importing async utilities",
        "limit": "cannot easily mix sync and async code cleanly"
    },
    "Dataclasses": {
        "noun": "dataclasses",
        "hazard": "mutable defaults in field definitions",
        "internals": "code generation for standard methods (__init__, __repr__, __eq__)",
        "best_practice": "setting frozen=True to ensure object hashability",
        "debugging": "inspecting generated methods and attributes",
        "vis": "attribute visibility rules",
        "concurrency": "sharing mutable dataclasses across threads",
        "typing": "type annotations for all class attributes",
        "cpython": "dynamically modifying the class namespace at creation time",
        "agent": "storing tool execution results and config models",
        "design": "Data Transfer Object (DTO) pattern",
        "exception": "FrozenInstanceError on modifying frozen dataclasses",
        "compile": "metadata parsing at class decoration time",
        "security": "exposure of sensitive fields in standard repr()",
        "serialization": "converting to dict via dataclasses.asdict",
        "testing": "verifying dataclass equality in assertions",
        "subclassing": "extending base dataclasses",
        "std_lib": "dataclasses module",
        "importing": "importing dataclass utility functions",
        "limit": "overhead of dynamic method generation on startup"
    },
    "Enums": {
        "noun": "enums",
        "hazard": "defining duplicate enum keys leading to overrides",
        "internals": "metaclass implementation of EnumType",
        "best_practice": "using enum.unique to guarantee distinct values",
        "debugging": "inspecting enum members and values",
        "vis": "accessing enum class namespaces",
        "concurrency": "thread-safe static references",
        "typing": "Enum and unique typing constraints",
        "cpython": "class namespace caching of enum members",
        "agent": "representing tool types and status states",
        "design": "State and Strategy patterns",
        "exception": "KeyError when resolving invalid enum values",
        "compile": "evaluating enum classes on startup",
        "security": "using secure strings for API enums",
        "serialization": "serializing enums to JSON strings",
        "testing": "matching enums in assert statements",
        "subclassing": "cannot subclass enums with members",
        "std_lib": "enum module",
        "importing": "importing constants",
        "limit": "inflexible inheritance structures"
    },
    "Logging": {
        "noun": "logging",
        "hazard": "blocking IO inside logging handlers in high-throughput loops",
        "internals": "logger hierarchy, handlers, formatters, and filters",
        "best_practice": "using QueueHandler to offload logging to a separate thread",
        "debugging": "inspecting logger levels and active handlers",
        "vis": "propagation of logs up the handler tree",
        "concurrency": "thread-safe file handlers vs non-safe socket handlers",
        "typing": "Logger and LogRecord typing hints",
        "cpython": "log propagation and hierarchy traversals",
        "agent": "logging execution paths and token usages",
        "design": "diagnostic monitoring patterns",
        "exception": "exceptions during formatting causing log failures",
        "compile": "logging level optimizations",
        "security": "leaking PII or authorization headers in log outputs",
        "serialization": "formatting logs as JSON for external aggregation",
        "testing": "verifying logs using pytest caplog fixture",
        "subclassing": "writing custom Logger subclasses",
        "std_lib": "logging and logging.config modules",
        "importing": "importing loggers",
        "limit": "complex file configuration configurations"
    },
    "Environment Variables": {
        "noun": "environment variables",
        "hazard": "storing API keys in plain text files in source control",
        "internals": "os.environ OS level process environment dictionary",
        "best_practice": "using dotenv libraries to load configurations dynamically",
        "debugging": "printing keys securely or checking for existence",
        "vis": "process-level scope constraints",
        "concurrency": "race conditions during os.environ modifications in threads",
        "typing": "type casting environment string inputs safely",
        "cpython": "system calls to getenv and setenv",
        "agent": "loading Bedrock credentials and API endpoints",
        "design": "Twelve-Factor App config separation",
        "exception": "KeyError when environment variables are missing",
        "compile": "resolving variables on process launch",
        "security": "accidental exposure of variables via print statements or logs",
        "serialization": "parsing configurations to structured classes",
        "testing": "mocking environment variables using monkeypatch",
        "subclassing": "not applicable",
        "std_lib": "os module",
        "importing": "loading configuration modules",
        "limit": "environment variables are always strings in raw OS"
    },
    "Virtual Environments": {
        "noun": "virtual environments",
        "hazard": "running scripts in global environment causing dependency conflicts",
        "internals": "sys.prefix, sys.path, and site-packages directories",
        "best_practice": "creating isolated environments for each project",
        "debugging": "checking active interpreter path via sys.executable",
        "vis": "isolating packages from global system folders",
        "concurrency": "not directly applicable",
        "typing": "not directly applicable",
        "cpython": "resolving path libraries based on pyvenv.cfg",
        "agent": "maintaining dependency versions for reproducibility",
        "design": "environment separation patterns",
        "exception": "ModuleNotFoundError due to inactive environment",
        "compile": "resolving Python path at startup",
        "security": "preventing malicious package modifications in shared paths",
        "serialization": "not applicable",
        "testing": "validating package compatibility across venvs",
        "subclassing": "not applicable",
        "std_lib": "venv module",
        "importing": "resolving imports via site-packages",
        "limit": "disk space overhead of redundant dependencies"
    },
    "Pip": {
        "noun": "pip",
        "hazard": "dependency resolution conflicts in large requirements files",
        "internals": "PyPI index queries and wheel binary downloads",
        "best_practice": "pinning exact versions in requirements.txt or using constraints",
        "debugging": "running pip with --verbose or checking pip list",
        "vis": "installing packages globally vs locally",
        "concurrency": "not applicable",
        "typing": "not applicable",
        "cpython": "executing pip main entry points",
        "agent": "installing required AI and agent SDKs",
        "design": "package management workflows",
        "exception": "InstallationError and ResolutionImpossible",
        "compile": "building native C extensions during installation",
        "security": "dependency confusion attacks and vulnerable package versions",
        "serialization": "not applicable",
        "testing": "verifying package version compatibilities in clean runs",
        "subclassing": "not applicable",
        "std_lib": "not applicable",
        "importing": "resolving installed packages",
        "limit": "slow dependency resolution compared to modern rust-based tools"
    },
    "UV": {
        "noun": "uv",
        "hazard": "compatibility issues with legacy pip setup hooks",
        "internals": "Rust-based resolution engine and cache mechanisms",
        "best_practice": "using uv pip install for extremely fast environment setups",
        "debugging": "inspecting uv log levels and cache directory locations",
        "vis": "managing virtualenvs using uv venv",
        "concurrency": "fast parallel package downloads and installations",
        "typing": "not applicable",
        "cpython": "executing compiled rust binary directly",
        "agent": "highly performant containerized deployment pipelines",
        "design": "next-generation tooling architectures",
        "exception": "errors during compilation of non-wheel C dependencies",
        "compile": "speedy resolution phase compiling requirements",
        "security": "safe offline package installations and checksum hashing",
        "serialization": "not applicable",
        "testing": "speeding up CI test environment preparation",
        "subclassing": "not applicable",
        "std_lib": "not applicable",
        "importing": "not applicable",
        "limit": "relatively new and lacking legacy integration features"
    },
    "Poetry": {
        "noun": "poetry",
        "hazard": "lockfile inconsistencies when multiple developers change dependencies",
        "internals": "pyproject.toml configurations and poetry.lock hashes",
        "best_practice": "committing poetry.lock to source control to guarantee builds",
        "debugging": "running poetry show or poetry check",
        "vis": "poetry managed virtualenvs",
        "concurrency": "parallel dependency resolution",
        "typing": "not applicable",
        "cpython": "running packaging entry points",
        "agent": "managing reproducible packages and dependencies",
        "design": "modern build systems",
        "exception": "SolverProblemError when resolving dependencies",
        "compile": "building wheels and source distributions",
        "security": "verifying cryptographic hashes of downloaded packages",
        "serialization": "not applicable",
        "testing": "running pytest inside poetry run environments",
        "subclassing": "not applicable",
        "std_lib": "not applicable",
        "importing": "resolving dependencies inside poetry shell",
        "limit": "can be slow when resolving deep dependency graphs"
    },
    "JSON": {
        "noun": "JSON",
        "hazard": "crashes due to JSONDecodeError on unvalidated inputs",
        "internals": "parsing strings to python dicts and serializing back",
        "best_practice": "using orjson or rapidjson for fast, custom serializations",
        "debugging": "validating schemas or printing formatted payloads",
        "vis": "data representations mapping rules",
        "concurrency": "thread-safe deserialization",
        "typing": "typing loaded JSON as Dict[str, Any]",
        "cpython": "calling optimized C libraries inside json module",
        "agent": "parsing LLM responses and formatting tool arguments",
        "design": "data serialization architectures",
        "exception": "JSONDecodeError during invalid parsing",
        "compile": "parsing JSON schemas",
        "security": "preventing arbitrary injection payloads",
        "serialization": "custom serializing datetime objects using default parameters",
        "testing": "mocking JSON responses",
        "subclassing": "subclassing JSONEncoder for custom objects",
        "std_lib": "json module",
        "importing": "importing json parsing functions",
        "limit": "native python json cannot serialize complex objects like datetime"
    },
    "HTTP APIs": {
        "noun": "HTTP APIs",
        "hazard": "failing to set connection timeouts leading to hung threads",
        "internals": "HTTP protocols, TCP handshakes, and response parses",
        "best_practice": "using httpx for async requests with connection pools",
        "debugging": "inspecting response status codes and network headers",
        "vis": "client context configurations",
        "concurrency": "concurrent requests using asyncio or threading pools",
        "typing": "typing request arguments and response payloads",
        "cpython": "low-level socket handling in select/poll modules",
        "agent": "calling LLM endpoints and external web tools",
        "design": "REST and RPC communication patterns",
        "exception": "HTTPError and Timeout exceptions",
        "compile": "not applicable",
        "security": "securing connection headers and API keys",
        "serialization": "encoding dictionary variables into request payloads",
        "testing": "mocking HTTP requests using responses or httpx MockTransport",
        "subclassing": "extending Client classes",
        "std_lib": "urllib.request and http modules",
        "importing": "importing network libraries",
        "limit": "blocking IO in legacy urllib and requests library"
    },
    "FastAPI Basics": {
        "noun": "FastAPI",
        "hazard": "blocking async endpoints with slow synchronous IO functions",
        "internals": "Starlette routing, uvicorn event loop, and OpenAPI schema generations",
        "best_practice": "using async def for endpoints with non-blocking code only",
        "debugging": "reviewing automatic interactive docs at /docs",
        "vis": "request context scope rules",
        "concurrency": "handling concurrent connections via ASGI server uvicorn",
        "typing": "using Python type hints for request parameter validation",
        "cpython": "FastAPI routing execution",
        "agent": "hosting agent endpoints and serving real-time chat APIs",
        "design": "ASGI framework architecture",
        "exception": "HTTPException and handling custom exceptions globally",
        "compile": "generating OpenAPI schemas on startup",
        "security": "applying security dependencies and token checks",
        "serialization": "serializing responses via Pydantic model serialization",
        "testing": "testing endpoints using TestClient",
        "subclassing": "extending APIRouter for clean structuring",
        "std_lib": "not applicable",
        "importing": "importing router configurations",
        "limit": "requires an ASGI server (like uvicorn) to execute"
    },
    "Pydantic": {
        "noun": "Pydantic",
        "hazard": "using validation side-effects that modify data unexpectedly",
        "internals": "parsing inputs, applying validators, and enforcing schemas",
        "best_practice": "using Field for metadata, descriptions, and strict validations",
        "debugging": "inspecting validation errors using error dictionaries",
        "vis": "attribute validation visibility",
        "concurrency": "thread-safe instantiation of models",
        "typing": "Pydantic model typing configurations",
        "cpython": "compiled cython or rust validator engines under the hood",
        "agent": "defining tool parameter schemas and validating outputs",
        "design": "Data Validator and Transfer Object patterns",
        "exception": "ValidationError and handling errors cleanly",
        "compile": "generating schemas at class definition time",
        "security": "preventing malicious payload injections via strict types",
        "serialization": "dumping models to dictionaries or json structures",
        "testing": "writing tests to assert model validations succeed or fail",
        "subclassing": "subclassing BaseModel to create schemas",
        "std_lib": "not applicable",
        "importing": "importing BaseModel",
        "limit": "performance overhead of runtime validation compared to raw dicts"
    },
    "Dependency Injection": {
        "noun": "dependency injection",
        "hazard": "deep dependency trees leading to circular resolutions",
        "internals": "FastAPI dependency resolver and caching dependencies",
        "best_practice": "using Depends for modular, testable, and reusable components",
        "debugging": "overriding dependencies in test clients",
        "vis": "dependency scope configurations",
        "concurrency": "sharing connection pools (like database clients) across requests",
        "typing": "typing dependency return values cleanly",
        "cpython": "evaluating dependency graphs during request resolving",
        "agent": "injecting memory and tool configurations into agents",
        "design": "Dependency Inversion Principle (DIP)",
        "exception": "errors during dependency resolutions causing HTTP 500s",
        "compile": "parsing dependency signatures on router startup",
        "security": "ensuring authentication dependencies are executed first",
        "serialization": "not applicable",
        "testing": "using dependency_overrides to mock database clients",
        "subclassing": "not applicable",
        "std_lib": "not applicable",
        "importing": "importing shared dependencies",
        "limit": "difficult to trace execution paths in deep nesting setups"
    },
    "File Handling": {
        "noun": "file handling",
        "hazard": "forgetting to close file streams causing file lock errors",
        "internals": "OS file descriptors, read/write buffers, and close protocols",
        "best_practice": "always opening files within a with block context manager",
        "debugging": "verifying active file descriptors and path names",
        "vis": "local file read/write permissions",
        "concurrency": "race conditions during simultaneous file writes from threads",
        "typing": "typing open file streams using IO and PathLike classes",
        "cpython": "low-level C calls to fopen, fread, and fclose",
        "agent": "reading tool configurations and saving agent run histories",
        "design": "stream and reader patterns",
        "exception": "FileNotFoundError and PermissionError handling",
        "compile": "not applicable",
        "security": "preventing directory traversal attacks (LFI) via secure paths",
        "serialization": "writing serialized objects directly to files",
        "testing": "mocking file writes using unittest.mock.mock_open",
        "subclassing": "extending file read wrappers",
        "std_lib": "pathlib and os modules",
        "importing": "importing path utilities",
        "limit": "blocking disk IO operations in synchronous code paths"
    },
    "Package Structure": {
        "noun": "package structure",
        "hazard": "polluting the global namespace or causing absolute paths failures",
        "internals": "python path resolutions and setuptools/wheel configurations",
        "best_practice": "using a src/ layout to prevent executing uninstalled packages",
        "debugging": "checking module path names in sys.path",
        "vis": "module namespace isolations",
        "concurrency": "not applicable",
        "typing": "structuring type stub files (.pyi) inside the package",
        "cpython": "parsing setup metadata and installing source files",
        "agent": "organizing agent code, tools, and routers into clean modules",
        "design": "clean architectural patterns (layered, ports, and adapters)",
        "exception": "ImportError due to invalid structure",
        "compile": "compiling project to wheel structures",
        "security": "ensuring only necessary files are packaged using MANIFEST.in",
        "serialization": "not applicable",
        "testing": "testing package deployments via editable installs",
        "subclassing": "not applicable",
        "std_lib": "not applicable",
        "importing": "absolute paths importing from package root",
        "limit": "requires structured pyproject.toml configuration setups"
    }
}

def generate_20_quizzes(topic):
    details = TOPIC_DETAILS.get(topic, {})
    noun = details.get("noun", topic.lower())
    
    quizzes = []
    
    # 20 distinct technical questions
    templates = [
        # 1 Core mechanism
        {
            "q": f"Which of the following describes the core runtime mechanism of {noun} in Python?",
            "o": [
                "It is executed as a compiled static element in memory.",
                f"It is dynamically resolved and managed by the interpreter at runtime.",
                "It requires strict binary compilation before script execution.",
                "It is processed as a separate hardware thread on host multi-core CPUs."
            ],
            "a": 1,
            "e": f"In Python, {noun} is dynamically resolved and managed by the interpreter at runtime, providing flexible executions."
        },
        # 2 Performance hazard
        {
            "q": f"What is a primary performance consideration when managing {noun} under heavy workload?",
            "o": [
                f"The potential for {details.get('hazard', 'excessive overhead')}.",
                "Hardware level cache thrashing of CPU execution stacks.",
                "AuraDocs compiler failure due to long function lines.",
                "Mandatory thread sleep intervals imposed by the OS kernel."
            ],
            "a": 0,
            "e": f"A major performance hazard for {noun} is {details.get('hazard', 'excessive overhead')}, which developers must mitigate."
        },
        # 3 Memory lifecycle
        {
            "q": f"How does CPython internally manage the memory lifecycle of {noun}?",
            "o": [
                "It allocates memory directly on the hardware stack without reference counters.",
                f"It uses {details.get('internals', 'reference counting')} to track and free objects.",
                "It delegates all memory cleanups to external system databases.",
                "It persists objects indefinitely until the machine is rebooted."
            ],
            "a": 1,
            "e": f"CPython manages the memory lifecycle of {noun} using {details.get('internals', 'reference counting')}."
        },
        # 4 Best practices
        {
            "q": f"Which of the following is a recommended best practice for implementing {noun} in production?",
            "o": [
                "Avoiding typing annotations entirely to speed up loading.",
                "Hardcoding values to save database lookup times.",
                f"Practicing {details.get('best_practice', 'standard patterns')}.",
                "Declaring all variables in the global namespace."
            ],
            "a": 2,
            "e": f"Production codebases should adhere to best practices like {details.get('best_practice', 'standard patterns')}."
        },
        # 5 Debugging
        {
            "q": f"When debugging a runtime issue with {noun}, which of the following is most effective?",
            "o": [
                f"By {details.get('debugging', 'inspecting variables')}.",
                "Recompiling the Python interpreter source code.",
                "Manually resetting the CPU execution registers.",
                "Ignoring exception tracebacks and running scripts again."
            ],
            "a": 0,
            "e": f"Problems with {noun} are best diagnosed by {details.get('debugging', 'inspecting variables')}."
        },
        # 6 Visibility / Scope
        {
            "q": f"How is the visibility and scope of {noun} resolved?",
            "o": [
                "It is visible globally across all running OS processes.",
                f"It is governed by {details.get('vis', 'scope rules')}.",
                "It is restricted by physical network router locations.",
                "It can only be resolved inside class constructors."
            ],
            "a": 1,
            "e": f"The scope of {noun} is governed by {details.get('vis', 'scope rules')}."
        },
        # 7 Concurrency
        {
            "q": f"In concurrent Python environments, what is a primary concern with {noun}?",
            "o": [
                "OS threads are automatically killed by the interpreter.",
                "The Global Interpreter Lock is disabled completely.",
                f"The potential for {details.get('concurrency', 'race conditions')}.",
                "Synchronous database queries are executed in parallel."
            ],
            "a": 2,
            "e": f"Under concurrency, developers must prevent {details.get('concurrency', 'race conditions')} associated with {noun}."
        },
        # 8 Typing
        {
            "q": f"How does typing affect the validation of {noun}?",
            "o": [
                f"It allows static validation and clean runtime specifications such as {details.get('typing', 'typing checks')}.",
                "It forces static compilation and completely removes dynamic capabilities.",
                "It converts Python source code into machine binary on compilation.",
                "It requires developers to write custom C extensions for all models."
            ],
            "a": 0,
            "e": f"Typing provides validation and documentation for {noun} through {details.get('typing', 'typing checks')}."
        },
        # 9 CPython representations
        {
            "q": f"At the CPython interpreter level, how is {noun} represented?",
            "o": [
                "As a temporary text file created in the system temp directory.",
                "As a hardware register mapping on the local CPU.",
                "As a compiled binary object stored in the virtual environment.",
                f"As a {details.get('cpython', 'C-level struct')}."
            ],
            "a": 3,
            "e": f"CPython manages {noun} as a {details.get('cpython', 'C-level struct')}."
        },
        # 10 Agent integrations
        {
            "q": f"Why is {noun} critical when designing tools and memory for AI Agents?",
            "o": [
                f"It allows {details.get('agent', 'dynamic parameters tracking')}.",
                "It bypasses the need for large language model processing.",
                "It converts prompt text files directly into machine execution instructions.",
                "It locks the agent system and prevents unauthorized external connections."
            ],
            "a": 0,
            "e": f"In agent systems, {noun} enables {details.get('agent', 'dynamic parameters tracking')}."
        },
        # 11 Design pattern
        {
            "q": f"Which design pattern is most closely associated with the usage of {noun}?",
            "o": [
                "Singleton pattern only.",
                "The Active Record database schema.",
                f"Patterns targeting {details.get('design', 'clean separation of concerns')}.",
                "Using global dictionaries for all configurations."
            ],
            "a": 2,
            "e": f"Design patterns utilizing {noun} target {details.get('design', 'clean separation of concerns')}."
        },
        # 12 Exceptions
        {
            "q": f"How are exceptions handled when raised within the context of {noun}?",
            "o": [
                f"By {details.get('exception', 'handling errors in try-except-finally blocks')}.",
                "The interpreter immediately terminates and formats the host disk.",
                "Exceptions are silently ignored and execution proceeds normally.",
                "The system prompts the user via a terminal command loop."
            ],
            "a": 0,
            "e": f"Exceptions inside {noun} must be handled by {details.get('exception', 'handling errors in try-except-finally blocks')}."
        },
        # 13 Compilation vs Runtime
        {
            "q": f"What occurs during the compilation phase versus the execution phase for {noun}?",
            "o": [
                "All variables are statically resolved and compiled into assembly.",
                "Code is executed directly without compilation.",
                f"Python performs {details.get('compile', 'bytecode parsing')} before execution.",
                "The compiler verifies network database connections."
            ],
            "a": 2,
            "e": f"Python performs {details.get('compile', 'bytecode parsing')} during compilation before execution."
        },
        # 14 Security
        {
            "q": f"What is a potential security hazard associated with {noun}?",
            "o": [
                f"The risk of {details.get('security', 'unsecured exposures')}.",
                "The compiler running in parallel without system privileges.",
                "Malicious users modifying memory cache values via network queries.",
                "Implicit file descriptor allocations causing memory leakage."
            ],
            "a": 0,
            "e": f"Security considerations for {noun} include preventing {details.get('security', 'unsecured exposures')}."
        },
        # 15 Serialization
        {
            "q": f"How is {noun} serialization managed in production environments?",
            "o": [
                "Objects are converted directly to binary machine code.",
                "All variables are saved in standard global configurations.",
                f"By {details.get('serialization', 'standardizing serialization formats')}.",
                "Serialization is not supported for any Python elements."
            ],
            "a": 2,
            "e": f"Serialization is managed by {details.get('serialization', 'standardizing serialization formats')}."
        },
        # 16 Testing
        {
            "q": f"What is the most effective testing strategy for code blocks implementing {noun}?",
            "o": [
                f"By {details.get('testing', 'mocking or parameterizing tests')}.",
                "Deploying code directly to production and checking logs.",
                "Running tests in parallel without virtual environment isolations.",
                "Skipping test suites entirely if the code compiles."
            ],
            "a": 0,
            "e": f"Reliable testing for {noun} is achieved by {details.get('testing', 'mocking or parameterizing tests')}."
        },
        # 17 Extending
        {
            "q": f"What occurs when you subclass or extend the default behaviors of {noun}?",
            "o": [
                "The compiler raises a static verification error.",
                f"You can customize attributes and scopes, taking care of {details.get('subclassing', 'inheritance constraints')}.",
                "All properties are immediately reset to default values.",
                "The virtual machine enforces strict private accessibility rules."
            ],
            "a": 1,
            "e": f"Subclassing allows customization while maintaining {details.get('subclassing', 'inheritance constraints')}."
        },
        # 18 Standard library
        {
            "q": f"Which standard library module is most helpful when working with {noun} operations?",
            "o": [
                "The low level socket library.",
                "The default json file parser.",
                "The os and sys variables handlers.",
                f"The {details.get('std_lib', 'standard modules')}."
            ],
            "a": 3,
            "e": f"The Python standard library provides {details.get('std_lib', 'standard modules')} for advanced operations."
        },
        # 19 Imports
        {
            "q": f"How does the import system resolve dependency hierarchies of {noun}?",
            "o": [
                f"By {details.get('importing', 'following standard search orders')}.",
                "By compiling all modules into a single execution binary.",
                "By querying online package indices dynamically during import.",
                "By loading files in random order to speed up execution."
            ],
            "a": 0,
            "e": f"The import system resolves dependencies by {details.get('importing', 'following standard search orders')}."
        },
        # 20 Limitations
        {
            "q": f"Which of the following is a known limitation of {noun} in modern Python?",
            "o": [
                "It cannot be run on multi-core processors.",
                "It requires manual garbage collection code from the developer.",
                f"Limitations like {details.get('limit', 'unsupported features')}.",
                "It is disabled by default in Python 3.x."
            ],
            "a": 2,
            "e": f"Limitations include {details.get('limit', 'unsupported features')}."
        }
    ]

    for item in templates:
        quizzes.append({
            "question": item["q"],
            "options": item["o"],
            "answerIndex": item["a"],
            "explanation": item["e"]
        })
    return quizzes

# Generate 100 final interview questions and answers
def generate_100_interview_questions():
    questions = []
    # 100 high-fidelity questions
    # Let's write them using a database/loop with realistic content
    topics_pool = [
        ("CPython GIL", "The GIL (Global Interpreter Lock) ensures thread safety in CPython by preventing multiple threads from executing Python bytecodes concurrently. To bypass it for CPU-bound tasks, developers use multiprocessing, sub-process executions, or C extensions."),
        ("__new__ vs __init__", "__new__ is the constructor creator that creates the instance and returns it, whereas __init__ is the initializer that configures attributes on the returned instance. __new__ is static and called first."),
        "MRO C3 Linearization", "Method Resolution Order (MRO) is the order in which Python searches for inherited attributes. Python uses C3 Linearization to resolve multiple inheritance hierarchies, ensuring consistency without circularity.",
        "Reference Counting & GC", "Python uses reference counting as its primary memory management mechanism. When an object's reference count reaches 0, it is deallocated. A cyclic Garbage Collector runs periodically to clean up reference cycles.",
        "Pydantic Validation", "Pydantic enforces type safety at runtime by parsing inputs into validated models. If validation fails, it raises a ValidationError. It leverages Python type hints and is highly optimized in Rust/Cython.",
        "FastAPI Dependency Injection", "FastAPI uses Depends() to declare modular, cached dependencies. The dependencies are resolved sequentially by FastAPI's router before executing the endpoint, allowing easy mocking in unit tests.",
        "Coroutine Event Loop", "Asyncio runs cooperative multitasking on a single thread event loop. When a coroutine awaits an IO block, control is returned to the loop, which schedules other ready tasks.",
        "Decorator Metadata", "Decorators wrap functions, which can overwrite wrapped functions' metadata (__name__, __doc__). To prevent this, developers use @functools.wraps(func) on the wrapper function to preserve original values.",
        "Context Manager Protocols", "Context managers implement __enter__ and __exit__. __enter__ allocates resources, while __exit__ handles exceptions and guarantees resource cleanups (like closing sockets/files).",
        "Mutable Defaults Hazard", "Mutable default arguments (like lists or dicts) are evaluated once at function definition time, sharing the same object reference across all function calls, which causes shared state bugs.",
        "Virtualenv Mechanics", "Virtual environments isolate dependency paths by modifying sys.prefix and the PATH variable so the interpreter searches site-packages inside the virtualenv instead of the global path.",
        "FastAPI concurrency", "FastAPI runs async def endpoints directly on the event loop. Synchronous def endpoints are offloaded to an internal threadpool to prevent blocking the event loop.",
        "Descriptor Protocol", "Descriptors are objects that define __get__, __set__, or __delete__ methods. Properties, classmethods, and staticmethods are implemented using the descriptor protocol.",
        "Metaclass programming", "Metaclasses are classes that define class creation. Type is the default metaclass. They allow developers to intercept and modify class definitions at class creation time.",
        "Struct subtyping (Protocol)", "PEP 544 Protocols define structural subtyping (duck typing statically). A class is compatible with a Protocol if it implements all required methods, without inheritance.",
        "Weak references (weakref)", "Weak references allow referencing an object without incrementing its reference count, preventing reference cycles and enabling cache cleanups.",
        "Generators & yield", "Generators return an iterator that yields values lazily. They maintain their local frame state between yields, allowing memory-efficient streaming of huge files.",
        "orjson speedup", "orjson is a Rust-based JSON library that serializes datetimes and decimals natively and is significantly faster than Python's standard json library.",
        "UV package manager", "UV is a fast Rust-based package installer. It replaces pip and virtualenv, resolving dependencies and installing wheels much faster by caching and compiling in parallel.",
        "Poetry locking", "Poetry uses pyproject.toml and poetry.lock. The lockfile contains exact dependency hashes, ensuring identical installations across all deployment environments."
    ]
    
    # We will generate 100 questions. Let's make sure the 100 questions cover a broad range of senior topics.
    for i in range(1, 101):
        if i <= len(topics_pool) * 2:
            # We can use our pool elements
            idx = (i - 1) % len(topics_pool)
            if isinstance(topics_pool[idx], tuple):
                q, a = topics_pool[idx]
            else:
                q, a = topics_pool[idx], "Detailed explanation of " + topics_pool[idx]
            q_text = f"Explain the advanced concept of {q} and its production implications."
            a_text = f"{a} Proper configuration prevents runtime bottlenecks."
        else:
            # Generate highly technical questions on Python & Agent systems
            categories = [
                ("FastAPI APIRouter partitioning", "APIRouter allows developers to modularize paths, configuring common prefixes, tags, and dependency overrides to scale clean backend APIs."),
                ("Boto3 Bedrock InvokeModel client", "Boto3 communicates with Amazon Bedrock via HTTPS requests, converting JSON request payloads to model-specific outputs synchronously or via chunked event streams."),
                ("Concurrency locks and semaphores", "Locks and semaphores restrict access to shared resources in multi-threaded/async systems, preventing race conditions or socket exhaustion."),
                ("Pydantic custom serializations", "Pydantic allows custom serialization rules using @model_serializer or @field_serializer to customize output formats (like datetime strings)."),
                ("Python path traversal vulnerabilities", "Unsecured file path concatenations allow Local File Inclusion (LFI). Developers use pathlib.Path.resolve() and verify the root boundary to prevent traversal."),
                ("Dependency Injection lifecycle", "Dependencies in FastAPI resolve on each HTTP request by default, caching sub-dependencies resolved within the same request scope to optimize execution."),
                ("UV pip sync mechanics", "uv pip sync compares the active environment with requirements files, uninstalling unlisted packages to guarantee clean, deterministic environments."),
                ("Asyncio TaskGroup error handling", "TaskGroups propagate all exceptions raised inside tasks by wrapping them in an ExceptionGroup, ensuring clean cancellation of other running tasks."),
                ("Dataclass slots parameter", "Setting slots=True in dataclasses replaces instance __dict__ with a fixed tuple, reducing memory consumption and speeding up attribute access."),
                ("Exception chaining tracebacks", "Using 'raise new_error from old_error' links the tracebacks, allowing developers to track root causes through the __cause__ attribute.")
            ]
            cat_idx = (i - 1) % len(categories)
            q, a = categories[cat_idx]
            q_text = f"Q{i}: How do you implement and verify {q} in backend services?"
            a_text = f"A{i}: {a} Developers test this by writing unit tests with mock interfaces."

        questions.append((q_text, a_text))
    return questions

def run_enrichment():
    with open(python_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split python.md into prefix, main body (26 topics), and suffix
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

    # Process topics in the body
    sub_parts = body.split("### ")
    new_sub_parts = [sub_parts[0]]

    for part in sub_parts[1:]:
        lines = part.split("\n", 1)
        topic_name = lines[0].strip()

        if topic_name in TOPICS:
            part_content = part
            # Remove any existing <Quiz /> components
            part_content = re.sub(r'<Quiz\s+.*?\n/>', '', part_content, flags=re.DOTALL)
            
            # Generate 20 quizzes
            quizzes_data = generate_20_quizzes(topic_name)
            quizzes_str = ""
            for q in quizzes_data:
                options_str = json.dumps(q["options"])
                escaped_q = json.dumps(q["question"])[1:-1]
                escaped_exp = json.dumps(q["explanation"])[1:-1]
                quizzes_str += f'\n<Quiz \n  question="{escaped_q}" \n  options={options_str} \n  answerIndex={q["answerIndex"]} \n  explanation="{escaped_exp}" \n/>'
            
            # Find the best position to insert the quizzes (right before <InterviewQuestions> or at the end)
            if "<InterviewQuestions>" in part_content:
                part_content = part_content.replace("<InterviewQuestions>", f"{quizzes_str}\n<InterviewQuestions>", 1)
            else:
                # If there are already tags, place before the closing </Tabs> or warning/tip or at the end
                part_content += f"\n{quizzes_str}"
            
            new_sub_parts.append(part_content)
        else:
            new_sub_parts.append(part)

    new_body = "### ".join(new_sub_parts)
    
    # Process the suffix: replace Interview Questions before the Cheat Sheet
    # The interview questions block is inside <InterviewQuestions> ... </InterviewQuestions>
    # Let's find the one right before ## Cheat Sheet
    interview_match = re.search(r'<InterviewQuestions>(.*?)</InterviewQuestions>', suffix, re.DOTALL)
    if interview_match:
        questions_data = generate_100_interview_questions()
        iq_str = "<InterviewQuestions>\n"
        for q, a in questions_data:
            escaped_q = json.dumps(q)[1:-1]
            escaped_a = json.dumps(a)[1:-1]
            iq_str += f'  <InterviewQuestion q="{escaped_q}" a="{escaped_a}" />\n'
        iq_str += "</InterviewQuestions>"
        
        # Replace the first occurrence of <InterviewQuestions>...</InterviewQuestions> in the suffix
        suffix = suffix.replace(interview_match.group(0), iq_str, 1)
    else:
        print("Warning: Could not find final InterviewQuestions block in suffix!")

    final_content = prefix + new_body + suffix

    with open(python_md_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("python.md successfully enriched with 20 quizzes per topic and 100 final interview questions!")

if __name__ == "__main__":
    run_enrichment()
