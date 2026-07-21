import re

def generate_line_explanation(line_num, line_str):
    stripped = line_str.strip()
    
    # 1. Comment line
    if stripped.startswith("#"):
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** This is a documentation comment line starting with `#`. Python ignores comments during execution.
- **Why it is required:** It explains the purpose of the script to human developers and maintains clean code documentation.
- **What happens if removed:** The code will run identically, but human readers won't have immediate context on what this code block accomplishes.
- **Analogy:** Think of a comment like a sticky note attached to a blueprint—it helps the builders understand the design without altering the physical building.
- **Beginner Concept:** In Python, any text after `#` is ignored by the Python interpreter.
"""

    # 2. Blank line (if meaningful)
    if not stripped:
        return f"""Line {line_num}
```python

```
**Explanation:**
- **What this line does:** This is a blank vertical spacing line.
- **Why it is required:** It visually separates logical sections of code (such as imports, setup, and function definitions) to improve readability.
- **What happens if removed:** Python will execute the code fine, but lines of code will bunch together, making it harder for engineers to read.
- **Analogy:** Like paragraphs in a textbook, spacing gives your eyes a natural pause between concepts.
"""

    # 3. Import from package
    if stripped.startswith("from ") and " import " in stripped:
        parts = stripped.split(" import ")
        pkg = parts[0].replace("from ", "").strip()
        obj = parts[1].strip()
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** This line imports the `{obj}` class from the `{pkg}` package.
- **Why it is required:** Python does not automatically load every external library into memory. We must explicitly import `{obj}` so our program can use its pre-built capabilities.
- **What keywords mean:** `from` specifies the source library module (`{pkg}`), and `import` selects the specific tool (`{obj}`).
- **What happens if removed:** Python will throw a `NameError: name '{obj}' is not defined` as soon as we try to instantiate or use it.
- **Analogy:** Think of importing like opening your toolbox and picking out a specialized torque wrench (`{obj}`) from the storage tray (`{pkg}`).
- **Connection:** This makes the `{obj}` blueprint available for the next lines of code.
"""

    # 4. Standard import library
    if stripped.startswith("import "):
        mod = stripped.replace("import ", "").strip()
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Imports Python's built-in `{mod}` module into the current program workspace.
- **Why it is required:** Provides access to essential system utilities (such as logging, environment variables, or HTTP handlers) offered by `{mod}`.
- **What keywords mean:** `import` tells Python to load the module named `{mod}`.
- **What happens if removed:** Functions or variables referencing `{mod}` (like `{mod}.getenv` or `{mod}.getLogger`) will fail with a `NameError`.
- **Analogy:** Like plugging in a peripheral cable—it connects built-in system capabilities to your script.
"""

    # 5. App instantiation (app = BedrockAgentCoreApp())
    if " = BedrockAgentCoreApp(" in stripped or stripped.startswith("app = "):
        var_name = stripped.split("=")[0].strip()
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Creates a new instance of `BedrockAgentCoreApp` and assigns it to the variable `{var_name}`.
- **Why it is required:** `{var_name}` serves as the main application object that manages agent lifecycle events, routes triggers, and holds configuration state.
- **What variable stores:** `{var_name}` stores the active `BedrockAgentCoreApp` object.
- **What happens if removed:** We would have no central application object to register our execution handlers or deploy to AWS.
- **Analogy:** Think of this as powering on the central control unit of an autonomous robot before programming its movements.
"""

    # 6. Logger initialization (logger = logging.getLogger(...))
    if "logging.getLogger(" in stripped or "logging.basicConfig(" in stripped:
        if "basicConfig" in stripped:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Configures the default logging framework settings, setting the minimum log severity level to `logging.INFO`.
- **Why it is required:** Without basic configuration, log output messages might be suppressed or formatted inconsistently.
- **Analogy:** Like setting up the recording sensitivity on a security camera system.
"""
        else:
            var_name = stripped.split("=")[0].strip()
            name_str = re.search(r'getLogger\((.*?)\)', stripped).group(1)
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Creates a dedicated logger object named {name_str} and stores it in the variable `{var_name}`.
- **Why it is required:** Structured logging allows developers to track incoming session activity, diagnose errors, and monitor agent decisions in AWS CloudWatch.
- **What variable stores:** `{var_name}` holds the logger object for writing diagnostic messages.
- **Where logs go:** Log messages written by `{var_name}` appear in the terminal during local testing and in Amazon CloudWatch Logs when deployed.
- **Analogy:** Think of `{var_name}` as the flight data recorder (black box) recording every step of the journey.
"""

    # 7. Decorator (@app.invoke or @app.tool)
    if stripped.startswith("@"):
        dec_name = stripped.strip()
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** This is a Python **decorator** named `{dec_name}`.
- **What is a decorator:** A decorator is a special modifier starting with `@` that wraps the function defined immediately below it, giving it extra powers.
- **Why decorators are used:** They register functions with frameworks without altering the core function code.
- **What `{dec_name}` registers:** It registers the function directly below it as the official entrypoint handler for Bedrock AgentCore invocation events.
- **What happens when AgentCore receives a request:** AgentCore automatically detects the `@app.invoke` tag and routes the incoming payload directly into the registered function.
- **Analogy:** Like putting a "Push Button Here to Start Machine" sticker on an ignition switch.
"""

    # 8. Function definition (def handler(payload, context):)
    if stripped.startswith("def "):
        func_match = re.search(r'def\s+(\w+)\((.*?)\):', stripped)
        func_name = func_match.group(1) if func_match else "function"
        params = func_match.group(2) if func_match else ""
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Defines a new function named `{func_name}` that accepts parameters `({params})`.
- **Keyword explanation:** `def` is short for "define". It tells Python that a reusable block of code begins here.
- **Parameters explained:**
  - `payload`: A Python **dictionary** containing the user's input prompt, parameters, and query fields.
  - `context`: An object containing runtime metadata (such as active AWS session ID, caller IAM identity, and request timestamps).
- **Return value:** Returns a structured dictionary containing HTTP status codes and agent response text.
- **Why the function exists:** It contains the core decision-making logic executed whenever the agent is invoked.
- **Analogy:** Think of `{func_name}` like a recipe—`payload` and `context` are the ingredients passed in, and the returned dictionary is the finished meal.
"""

    # 9. Try block
    if stripped.startswith("try:"):
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Starts a `try` block for defensive error handling.
- **Why it is required:** Production applications must gracefully handle unexpected failures (like missing parameters or database timeouts) without crashing the entire server.
- **What keyword means:** `try` tells Python: "Attempt to execute the indented lines below. If an error occurs, jump straight to the `except` block."
- **Analogy:** Like wearing a safety harness before stepping onto a high platform—if you slip, the harness catches you.
"""

    # 10. Except block
    if stripped.startswith("except ") or stripped.startswith("except:"):
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Catches exceptions and errors that occurred inside the preceding `try` block.
- **Why it is required:** Prevents unhandled exceptions from returning raw stack traces or breaking the container runtime.
- **What happens when an error occurs:** Python captures the error object into variable `e`, logs the error details, and returns a clean 500 error response to the client.
- **Analogy:** Like an emergency backup generator switching on immediately when main power cuts out.
"""

    # 11. Variable assignment / Method call inside function
    if "=" in stripped and not stripped.startswith("return"):
        var_part, val_part = stripped.split("=", 1)
        var_name = var_part.strip()
        val_name = val_part.strip()
        
        # Check payload.get()
        if "payload.get(" in val_name:
            key_match = re.search(r'payload\.get\((.*?)\)', val_name)
            args = key_match.group(1) if key_match else ""
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Safely retrieves data from the `payload` dictionary using `.get()` and stores the value in variable `{var_name}`.
- **Method details (`payload.get({args})`):**
  - `payload`: The dictionary containing request parameters.
  - `.get()`: A safe lookup method that retrieves a key without throwing a `KeyError` if the key is missing.
  - Arguments `{args}`: Specifies the target key name and the fallback default value returned if the key does not exist.
- **What variable stores:** `{var_name}` stores the retrieved input value (or default fallback).
- **Why it is required:** Protects the agent against missing input fields sent by client applications.
- **Analogy:** Like asking a receptionist for a package—if the package isn't on the shelf, they hand you a default notification card instead of crashing the office.
"""
        
        # Check getattr(context, ...)
        if "getattr(" in val_name:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Safely reads an attribute from the `context` object using `getattr()` and stores it in variable `{var_name}`.
- **Method details:** `getattr(context, attribute_name, default_value)` inspects `context` for the requested property. If present, it returns the attribute; otherwise, it returns the default value.
- **What variable stores:** `{var_name}` holds the session identifier string.
- **Why it is required:** Ensures the code works both in local testing (where context might be mocked) and in production AWS microVM runtimes.
- **Analogy:** Checking someone's ID card for their badge number, defaulting to "Visitor" if no badge number is printed.
"""

        # Check os.getenv
        if "os.getenv(" in val_name:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Reads an environment variable from the operating system using `os.getenv()` and assigns it to `{var_name}`.
- **Method details:** `os.getenv("APP_ENV", "development")` looks for the OS variable `APP_ENV`. If not set, it defaults to `"development"`.
- **What variable stores:** `{var_name}` stores the environment configuration mode (e.g., `development`, `staging`, `production`).
- **Why it is required:** Allows the same code container to behave appropriately across local, test, and production environments without code edits.
- **Analogy:** Like checking a thermostat to see if the building is set to Heat Mode or Cool Mode.
"""

        # General assignment
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Computes `{val_name}` and assigns the result to variable `{var_name}`.
- **Why it is required:** Stores temporary calculation or formatted data so it can be referenced in log statements or return responses.
- **What variable stores:** `{var_name}` holds the calculated value.
- **Connection:** Provides values used in subsequent logging or response steps.
"""

    # 12. If statement (if not prompt:)
    if stripped.startswith("if "):
        cond = stripped.replace("if ", "").replace(":", "").strip()
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Evaluates a conditional check: `if {cond}:`.
- **Why validation is important:** Ensures required input parameters exist before executing core logic, preventing null pointer or empty data errors downstream.
- **What condition checks:** Checks if `{cond}` evaluates to `True` (e.g., if prompt is empty or missing).
- **What happens if condition is True:** Python enters the indented block directly below to execute fallback error responses.
- **What happens if condition is False:** Python skips the indented error block and proceeds to normal processing.
- **Analogy:** Like a bouncer checking tickets at the door—if you don't have a ticket (`if not ticket:`), you are directed to the ticket booth.
"""

    # 13. Logger call (logger.info(...))
    if stripped.startswith("logger."):
        msg = re.search(r'logger\.\w+\((.*?)\)', stripped)
        msg_str = msg.group(1) if msg else "log message"
        return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Writes an informational log message (`{msg_str}`) to the logging system.
- **Why it is required:** Provides real-time visibility into active agent executions, helping engineers debug production request flows.
- **Where logs go:** Written to standard output streams and captured by AWS CloudWatch Logs.
- **Analogy:** Like a ship captain writing an entry in the official logbook during a voyage.
"""

    # 14. Return statement (return { "statusCode": 200, ... })
    if stripped.startswith("return") or stripped.startswith('"statusCode"') or stripped.startswith('"response"') or stripped == "}" or stripped == "}:":
        if stripped.startswith("return"):
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Initiates a `return` statement to exit the function and pass data back to the caller.
- **What is being returned:** Returns a structured Python **dictionary** representing an HTTP response payload.
- **Who receives it:** The Bedrock AgentCore runtime receives this dictionary, serializes it into JSON, and sends it back to the client application.
- **Why response must be returned:** Without a return statement, the function would return `None`, causing AgentCore to report a blank execution payload to the user.
- **Analogy:** Handing a completed report back to the manager who requested it.
"""
        elif '"statusCode"' in stripped:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Defines the `"statusCode"` key inside the returned response dictionary.
- **Key details:** `"statusCode": 200` (or 400/500). Standard HTTP status codes communicate execution status:
  - `200`: Success.
  - `400`: Bad Request (client input validation error).
  - `500`: Internal Server Error.
- **Why required:** Allows API gateways and front-end clients to know immediately whether the request succeeded or failed.
"""
        elif '"response"' in stripped:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Defines the `"response"` key inside the returned dictionary.
- **Key details:** Holds the string output message, generated answer, or error summary returned by the agent.
- **JSON conversion:** AgentCore converts this dictionary into JSON format (`{{"statusCode": 200, "response": "..."}}`) before transmitting over HTTPS.
"""
        else:
            return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Closes the dictionary or code block structure (`}}`).
- **Why required:** Defines the boundary of the data structure in Python syntax.
"""

    # 15. Catch-all fallback line explanation
    return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Executes line statement `{stripped}`.
- **Why it is required:** Contributes to the overall operation and step progression of the script.
- **Connection:** Connects preceding code logic to subsequent return or processing steps.
"""

print("Test generator script compiled successfully!")
