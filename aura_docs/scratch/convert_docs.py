import re
import json

path = "C:/Users/nishu/workspace/wscs_bedrock/doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split("# Python for AI Agents (Beginner to Advanced)")
header = parts[0]
ai_section = parts[1]

# Quizzes definition
quizzes = {
    "Variables": {
        "question": "Which of the following describes Python's variable typing system?",
        "options": [
            "Static typing: Types are declared at write-time and enforced by compiler.",
            "Dynamic typing: Variable labels point to memory objects whose types are resolved at runtime.",
            "Duck typing: Variables are immutable and typed on first assignment.",
            "Strict typing: Types are determined by the folder directory structure."
        ],
        "answerIndex": 1,
        "explanation": "Python resolves variable types dynamically at runtime. Variable names are labels bound to memory locations containing values."
    },
    "Functions": {
        "question": "Why are mutable default arguments (like history=[]) dangerous in Python functions?",
        "options": [
            "They consume double the memory on execution.",
            "They raise a SyntaxError at compile time.",
            "They are instantiated only once when the module is loaded, causing state to leak between subsequent calls.",
            "They cannot be passed to LLM tool schemas."
        ],
        "answerIndex": 2,
        "explanation": "Mutable default parameters are evaluated once when the function is defined, meaning the same object is shared across all subsequent invocations."
    },
    "Classes": {
        "question": "What is the primary difference between __new__ and __init__ in Python classes?",
        "options": [
            "__new__ initializes the attributes; __init__ allocates the memory.",
            "__new__ creates the object instance and returns it; __init__ configures the instance attributes.",
            "__new__ is only for static methods; __init__ is for instance methods.",
            "There is no difference; they are aliases."
        ],
        "answerIndex": 1,
        "explanation": "__new__ is the constructor creator which returns the new instance, while __init__ initializes the fields on that instance."
    },
    "OOP": {
        "question": "What algorithm does Python use to determine Method Resolution Order (MRO) in multiple inheritance?",
        "options": [
            "A* Search Algorithm",
            "Depth First Search",
            "C3 Linearization Algorithm",
            "Kruskal's Algorithm"
        ],
        "answerIndex": 2,
        "explanation": "Python uses the C3 Linearization algorithm to construct a deterministic Method Resolution Order (MRO) list for class lookups."
    },
    "Modules": {
        "question": "How can you resolve circular import dependency errors in Python?",
        "options": [
            "Rename all modules to use capital letters.",
            "Refactor dependencies, use dynamic imports inside functions, or place imports at the bottom of the file.",
            "Delete the __init__.py files from both modules.",
            "Use wildcards (from module import *) everywhere."
        ],
        "answerIndex": 1,
        "explanation": "Circular dependencies can be fixed by refactoring shared code into a third module, executing dynamic imports at runtime inside functions, or reorganizing code structure."
    },
    "Packages": {
        "question": "What is the purpose of __init__.py in a Python package?",
        "options": [
            "It is used to compile the package to binary C code.",
            "It initializes the virtual environment parameters.",
            "It tells Python that the directory should be treated as a package, allowing package-level imports and api exposing.",
            "It registers the package with the global PyPI index."
        ],
        "answerIndex": 2,
        "explanation": "An __init__.py file designates a directory as a Python package, executing automatically when the package is imported."
    },
    "Decorators": {
        "question": "Why should you use @functools.wraps(func) when writing a custom decorator wrapper?",
        "options": [
            "To speed up function execution.",
            "To bypass the Global Interpreter Lock (GIL).",
            "To preserve the original function's name, docstring, and signature metadata.",
            "To automatically catch runtime errors."
        ],
        "answerIndex": 2,
        "explanation": "@functools.wraps copies the original function metadata (name, docstring, arguments) to the wrapper function so that introspection libraries can still read it."
    },
    "Context Managers": {
        "question": "In class-based Context Managers, what return value from __exit__ suppresses exceptions raised inside the with block?",
        "options": [
            "None",
            "True",
            "False",
            "raise"
        ],
        "answerIndex": 1,
        "explanation": "Returning True from __exit__ tells Python to catch/suppress the exception; returning False allows the exception to bubble up."
    },
    "Exception Handling": {
        "question": "Why is using a bare except: clause considered a dangerous anti-pattern?",
        "options": [
            "It causes memory leaks.",
            "It raises a TypeError.",
            "It catches all exceptions, including system-interrupt signals like KeyboardInterrupt, making it impossible to stop execution.",
            "It is ignored by Python at runtime."
        ],
        "answerIndex": 2,
        "explanation": "A bare except: clause catches BaseException, which includes SystemExit and KeyboardInterrupt, preventing the user from interrupting the script."
    },
    "Typing": {
        "question": "Does Python enforce type hints (e.g. x: int) at runtime by default?",
        "options": [
            "Yes, Python raises a TypeError if the value doesn't match the annotation.",
            "No, type hints are ignored during execution; static analysis must be run separately using tools like mypy.",
            "Yes, but only inside FastAPI routers.",
            "Only if the virtual environment is activated."
        ],
        "answerIndex": 1,
        "explanation": "Python does not check types at runtime. Type hints are metadata used by static analyzers (like mypy), IDEs, or frameworks like Pydantic."
    },
    "Async Programming": {
        "question": "Which of the following should you avoid inside an asynchronous function?",
        "options": [
            "Using the await keyword.",
            "Calling synchronous blocking functions like time.sleep() or requests.get().",
            "Using asyncio.gather().",
            "Returning a dictionary."
        ],
        "answerIndex": 1,
        "explanation": "Synchronous blocking calls stall the entire event loop, preventing other concurrent tasks from executing. Use non-blocking async counterparts."
    },
    "Dataclasses": {
        "question": "How do you make a Python dataclass immutable and hashable?",
        "options": [
            "Pass frozen=True to the @dataclass decorator.",
            "Use the readonly keyword.",
            "Store the class inside a tuple.",
            "Define all fields as private."
        ],
        "answerIndex": 0,
        "explanation": "Using @dataclass(frozen=True) automatically generates code that prevents attribute mutation and defines a __hash__ method."
    },
    "Enums": {
        "question": "Why is inheriting from both str and Enum (e.g. class Role(str, Enum)) a best practice for API states?",
        "options": [
            "It speeds up comparison operators.",
            "It allows the enum members to be serialized directly to JSON as plain strings.",
            "It bypasses pydantic validation.",
            "It makes the enum hashable."
        ],
        "answerIndex": 1,
        "explanation": "Inheriting from str ensures that enum values can be serialized directly into JSON outputs without needing custom serialization logic."
    },
    "Logging": {
        "question": "Why is structured JSON logging preferred over plaintext logging for production agents?",
        "options": [
            "JSON logging takes less disk space.",
            "Plaintext logs cannot be read on Windows.",
            "JSON logs group metadata into a single parseable line, enabling instant filtering and analysis in log search engines.",
            "JSON logs automatically mask all passwords."
        ],
        "answerIndex": 2,
        "explanation": "Log aggregators like CloudWatch or Elasticsearch parse JSON properties natively, allowing instant querying by session ID, module, or log level."
    },
    "Environment Variables": {
        "question": "What is a major security risk regarding environment variables in code?",
        "options": [
            "Retrieving values with os.environ.get() causes memory fragmentation.",
            "Hardcoding secret keys/API tokens directly in code files instead of using environment variables, risking leaks to public repositories.",
            "Environment variables can only hold integers.",
            "They are cleared every time a function finishes execution."
        ],
        "answerIndex": 1,
        "explanation": "Hardcoding secrets in source files allows anyone with access to the source code repository to read them. Env variables keep secrets separated from code."
    },
    "Virtual Environments": {
        "question": "How does activating a virtual environment affect import resolution?",
        "options": [
            "It copies the entire python interpreter to the root directory.",
            "It overrides global imports by prepending the virtual environment path to the shell's PATH, resolving imports from its site-packages.",
            "It compiles python code to C++.",
            "It blocks all standard library imports."
        ],
        "answerIndex": 1,
        "explanation": "Activation configures environment variables so that pip installations and python execution refer to the isolated folder structure."
    },
    "Pip": {
        "question": "What is the difference between pip install and pip install -e .?",
        "options": [
            "Editable mode (-e) installs the package as a read-only symlink.",
            "Editable mode (-e) allows modifying the package source code directly without reinstalling to see changes.",
            "Editable mode disables sub-dependency resolution.",
            "Standard install downloads code from GitHub only."
        ],
        "answerIndex": 1,
        "explanation": "Editable install symlinks the source code directory, ensuring changes to the local files are immediately reflected in imports."
    },
    "UV": {
        "question": "What makes UV faster than traditional pip?",
        "options": [
            "It ignores sub-dependency resolution.",
            "It is written in Rust, compiling dependencies concurrently and caching globally using hard links.",
            "It only installs binary wheel files.",
            "It executes in the browser."
        ],
        "answerIndex": 1,
        "explanation": "UV implements state-of-the-art Rust architecture with parallel dependency fetching, caching, and linking for high performance."
    },
    "Poetry": {
        "question": "What is the difference between pyproject.toml and poetry.lock?",
        "options": [
            "pyproject.toml is used on Windows, poetry.lock on Unix.",
            "pyproject.toml specifies general dependencies, while poetry.lock locks the exact resolved sub-dependency versions.",
            "poetry.lock contains encrypted security tokens.",
            "Poetry ignores the lockfile during installs."
        ],
        "answerIndex": 1,
        "explanation": "The toml configuration describes broad limits; the lockfile registers exact pinned versions to guarantee reproducible builds."
    },
    "JSON": {
        "question": "How do you handle custom non-serializable objects (like datetime) when using json.dumps()?",
        "options": [
            "Cast the entire object to a string.",
            "Provide a custom JSONEncoder subclass to parse and serialize the types.",
            "JSON cannot handle nested structures in Python.",
            "Import the json2 package."
        ],
        "answerIndex": 1,
        "explanation": "Providing a subclass of JSONEncoder allows defining customized serialization rules for non-primitive types."
    },
    "HTTP APIs": {
        "question": "When should you use httpx instead of requests?",
        "options": [
            "When you need to make asynchronous non-blocking HTTP requests.",
            "When you want to parse JSON automatically.",
            "Only when calling AWS Bedrock endpoints.",
            "When running on Python 2.x."
        ],
        "answerIndex": 0,
        "explanation": "httpx supports async requests via async/await, allowing concurrent I/O calls without blocking the async event loop."
    },
    "FastAPI Basics": {
        "question": "How does FastAPI automatically generate its OpenAPI / Swagger documentation?",
        "options": [
            "By executing a separate doc generator script.",
            "FastAPI reads python type hints and Pydantic models in route handler signatures to generate JSON schemas dynamically.",
            "By scraping comments in the source files.",
            "By calling external API registries."
        ],
        "answerIndex": 1,
        "explanation": "FastAPI parses the endpoint function declarations and uses Pydantic model schemas to compile standard OpenAPI specs automatically."
    },
    "Pydantic": {
        "question": "What does Pydantic do when you pass a numeric string (like '42') to an int field?",
        "options": [
            "It raises a ValidationError immediately.",
            "It coerces the string to the integer 42 where possible.",
            "It keeps it as a string.",
            "It ignores the type hint."
        ],
        "answerIndex": 1,
        "explanation": "Pydantic performs type coercion automatically to convert input types (like string representations of numbers) into correct types."
    },
    "Dependency Injection": {
        "question": "How does FastAPI's Depends simplify application testing?",
        "options": [
            "It automatically creates SQLite databases.",
            "It allows overriding dependencies with mocks, avoiding calls to actual databases or external services.",
            "It speeds up API route routing.",
            "It compiles route handlers."
        ],
        "answerIndex": 1,
        "explanation": "Depends is a framework-native lookup mechanism, allowing unit tests to override dependencies cleanly without editing code."
    },
    "File Handling": {
        "question": "Why is pathlib.Path preferred over the older os.path module for file operations?",
        "options": [
            "It runs 10x faster.",
            "It provides an object-oriented path interface and handles platform-independent operations automatically.",
            "It automatically writes files asynchronously.",
            "It is only compatible with AWS S3."
        ],
        "answerIndex": 1,
        "explanation": "pathlib models paths as object classes and overloads division operators (/), resolving Windows vs Unix slashes automatically."
    },
    "Package Structure": {
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

# Split the AI section into concepts
subsections = re.split(r'\n(###\s+[^\n]+)', ai_section)

output_subsections = []

# Intro section transformation:
intro = subsections[0]
intro_parsed = intro.replace(
    "* **Ecosystem Domination**",
    '<InfoCard title="Ecosystem Domination">'
).replace(
    "* **Syntax Simplicity**",
    '</InfoCard>\n<InfoCard title="Syntax Simplicity">'
).replace(
    "* **C-Bindings Performance**",
    '</InfoCard>\n<InfoCard title="C-Bindings Performance">'
).replace(
    "* **First-Class Framework Support**",
    '</InfoCard>\n<InfoCard title="First-Class Framework Support">'
)
# Close the last card
intro_parsed = re.sub(
    r'(<InfoCard title="First-Class Framework Support">.*?)(\n---|\n##|$)',
    r'\1\n</InfoCard>\n\2',
    intro_parsed,
    flags=re.DOTALL
)

output_subsections.append(intro_parsed)

concept_idx = 1
total_concepts = 26

for i in range(1, len(subsections), 2):
    title = subsections[i].replace("###", "").strip()
    body = subsections[i+1] if i+1 < len(subsections) else ""
    
    # Check if this is a concept (has the 8 headings)
    headers = re.findall(r'####\s+(\d+\.\s+[^\n]+)', body)
    if len(headers) >= 7:
        # Parse concept
        sections = {}
        pattern = r'####\s+\d+\.\s+([^\n]+)\n(.*?)(?=\n####\s+\d+\.|$)'
        matches = re.findall(pattern, body, re.DOTALL)
        for h, content in matches:
            sections[h.strip()] = content.strip()
            
        what_is = sections.get('What is it?', '')
        why = sections.get('Why do we need it?', '')
        syntax = sections.get('Syntax', '')
        simple_ex = sections.get('Simple Example', '')
        agent_ex = sections.get('AI Agent Example', '')
        best_practices = sections.get('Best Practices', '')
        common_mistakes = sections.get('Common Mistakes', '')
        iq = sections.get('Interview Questions', '')
        
        # Get raw codes
        def get_code(text):
            m = re.search(r'```(?:python|bash|toml)?\n(.*?)```', text, re.DOTALL)
            return m.group(1).strip() if m else text.strip()
            
        syntax_code = get_code(syntax)
        simple_code = get_code(simple_ex)
        agent_code = get_code(agent_ex)
        
        is_python = "```python" in syntax or "```python" in simple_ex or ("```" not in syntax and "```" not in simple_ex)
        use_playground = is_python and title.lower() not in ['packages', 'virtual environments', 'pip', 'uv', 'poetry', 'package structure']
        
        tabs_str = ""
        if use_playground:
            tabs_str = f"""<Tabs>
  <Tab label="Syntax & Example">

{syntax}

{simple_ex}

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      initialCode={json.dumps(simple_code)} 
      instruction="Run this interactive python example and see the console output."
    />
  </Tab>
</Tabs>"""
        else:
            tabs_str = f"""{syntax}

{simple_ex}"""

        # For best practices and common mistakes
        def list_to_items(text):
            items = re.findall(r'^\s*[\*\-]\s*(.*?)$', text, re.MULTILINE)
            return "\n".join(f"- {item}" for item in items)
            
        bp_list = list_to_items(best_practices)
        cm_list = list_to_items(common_mistakes)
        
        # For interview questions
        iq_matches = re.findall(r'\*\*Q:\*\*\s*(.*?)\n\*\*A:\*\*\s*(.*?)(?=\n\*\*Q:|$)', iq, re.DOTALL)
        if not iq_matches:
            iq_matches = re.findall(r'Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|$)', iq, re.DOTALL)
            
        iq_blocks = []
        for q, a in iq_matches:
            iq_blocks.append(f'<InterviewQuestion q={json.dumps(q.strip())} a={json.dumps(a.strip())} />')
        
        iq_str = ""
        if iq_blocks:
            iq_str = f"""<InterviewQuestions>
  {" ".join(iq_blocks)}
</InterviewQuestions>"""

        # Quiz
        quiz_data = quizzes.get(title, None)
        quiz_str = ""
        if quiz_data:
            quiz_str = f"""<Quiz 
  question={json.dumps(quiz_data["question"])} 
  options={{{json.dumps(quiz_data["options"])}}} 
  answerIndex={{{quiz_data["answerIndex"]}}} 
  explanation={json.dumps(quiz_data["explanation"])} 
/>"""

        # Build output
        concept_body = f"""
### {title}
<ProgressTracker currentSection={{{concept_idx}}} totalSections={{{total_concepts}}} />

<InfoCard title="Concept Overview">
{what_is}

**Why do we need it?**
{why}
</InfoCard>

{tabs_str}

<InfoCard title="AI Agent Integration">
{agent_ex}
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
        output_subsections.append(concept_body)
        concept_idx += 1
    else:
        # Non-concept section or tail section
        sec_title = subsections[i].strip()
        sec_body = subsections[i+1]
        
        if "Agent Architecture with Python" in sec_title:
            sec_body = sec_body.replace(
                "### 2. Multi-Agent Supervisor (`ep02_production_supervisor.py`)",
                "<AgentArchitectureDiagram />\n### 2. Multi-Agent Supervisor (`ep02_production_supervisor.py`)"
            )
        elif "Understanding Decorator-Based Agent Frameworks" in sec_title:
            sec_body = sec_body.replace(
                "The decorator extracts the function's metadata",
                "<DecoratorVisualizer decoratorName=\"@app.tool\" functionName=\"get_balance\" args=\"user_id\" returns=\"100.0\" />\n\nThe decorator extracts the function's metadata"
            )
        elif "Common Patterns Used in AI Agent Frameworks" in sec_title:
            headers = ["Pattern", "Description", "Code Example"]
            rows = [
                ["Model Context Protocol (MCP)", "Standardized protocol to list and call tools using JSON-RPC over HTTP/SSE.", "ep04_lambda_mcp_server.py"],
                ["Supervisor Delegation", "A parent agent routes tasks to specialized child agents, shielding tools.", "ep02_production_supervisor.py"],
                ["Token Budgeting", "Tracking and limiting token usage to prevent infinite routing loops.", "ep02_production_supervisor.py"],
                ["Identity Propagation", "Passing user identity claims (JWT) down to sub-agent tools for validation.", "ep05_auth_middleware.py"],
                ["Episodic Vector Memory", "Saving conversation snippets in vector stores and retrieving them using cosine similarity.", "ep12_semantic_memory.py"]
            ]
            comp_table = f'<ComparisonTable headers={{{json.dumps(headers)}}} rows={{{json.dumps(rows)}}} />'
            sec_body = re.sub(r'\|\s+\*\*Pattern\*\*.*?\|\s+`ep12_semantic_memory.py`\s+\|', comp_table, sec_body, flags=re.DOTALL)
            
        output_subsections.append(f"\n{sec_title}\n{sec_body}")

# Join back
new_ai_section = "".join(output_subsections)
final_content = header + "# Python for AI Agents (Beginner to Advanced)\n" + new_ai_section

with open(path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Conversion completed successfully!")
