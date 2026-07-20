import os
import re
import time
import argparse
from google import genai
from google.genai import types

# Standard headings required for the pedagogical template
STANDARD_HEADINGS = [
    "### What This Code Does",
    "### Code Walkthrough"
]

def parse_markdown_blocks(content):
    """
    Splits markdown content into code and text segments.
    Returns list of dicts: [{'type': 'text', 'content': str}, {'type': 'code', 'lang': str, 'code': str}]
    """
    parts = content.split("```")
    segments = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            segments.append({"type": "text", "content": part})
        else:
            # Code block segment
            lines = part.split("\n", 1)
            lang = lines[0].strip()
            code = lines[1] if len(lines) > 1 else ""
            segments.append({"type": "code", "lang": lang, "code": code})
    return segments

def rebuild_markdown(segments):
    """Reconstructs the markdown string from segments."""
    parts = []
    for seg in segments:
        if seg["type"] == "text":
            parts.append(seg["content"])
        else:
            parts.append(f"```{seg['lang']}\n{seg['code']}```")
    return "".join(parts)

def is_explained(text_segment):
    """Checks if the next text segment already contains the standardized explanation."""
    content = text_segment.get("content", "")
    return "What This Code Does" in content and "Code Walkthrough" in content

def get_chapter_title(content):
    """Extracts the first heading (H1) as the chapter title."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "AWS Bedrock AgentCore Module"

def get_mock_explanation(lang, code, block_idx):
    """Provides high-quality pre-defined/mock explanations for Chapter 1 testing."""
    if "from bedrock_agent_core import BedrockAgentCoreApp" in code and "Hello from Bedrock AgentCore!" in code:
        return """
### What This Code Does
This code block implements the absolute minimum "Hello World" entrypoint for an AWS Bedrock AgentCore application. It initializes the core application framework and registers a single invocation handler that responds with a status code of 200 and a simple greetings payload.

### Code Walkthrough
* **Line 2: `from bedrock_agent_core import BedrockAgentCoreApp`**: Imports the primary application framework class from the Bedrock AgentCore package.
* **Line 4: `app = BedrockAgentCoreApp()`**: Instantiates the global application object which manages runtime configurations, middleware, routing, and communication channels.
* **Line 6: `@app.invoke`**: A decorator that registers the decorated function as the session execution handler. Whenever the runtime microVM receives an execution invoke signal, this function is triggered.
* **Line 7-11: `def handler(payload, context): ...`**: Defines the handler callback, accepting the incoming `payload` (input parameters) and execution `context` (session information), returning a JSON-serializable dictionary with `statusCode` and `response`.
"""
    elif "IntroAgent" in code:
        return """
### What This Code Does
This code block implements an intermediate Bedrock AgentCore execution handler. It establishes standard Python logging to output runtime details, reads dynamic parameters from the incoming `payload`, extracts session metadata (`session_id`) from the execution `context`, and outputs a personalized response indicating session tracking.

### Code Walkthrough
* **Line 2: `import logging`**: Imports Python's built-in logging utility.
* **Line 4-5: `logging.basicConfig(...)` & `logger = ...`**: Configures console logging and registers a named logger instance for application tracing.
* **Line 8: `@app.invoke`**: Registers the handler callback.
* **Line 10-11: `prompt = payload.get("prompt", "")` & `session_id = ...`**: Safely extracts the prompt input from the payload and retrieves the session identifier from the runtime context, falling back to local defaults if missing.
* **Line 12: `logger.info(...)`**: Writes structured telemetry log statements to help track request processing.
* **Line 13-16: `return ...`**: Returns the response payload containing the session and prompt values.
"""
    elif "ProductionIntroAgent" in code:
        return """
### What This Code Does
This code block implements a production-grade AgentCore handler incorporating input validation, environment-variable-driven configuration switches, exception handling, and error response sanitization.

### Code Walkthrough
* **Line 2: `import os`**: Imports the OS interface to read container environment variables.
* **Line 6: `try...except Exception`**: Wraps the entire handler execution in a try-except block to catch all unhandled errors and return clean error responses.
* **Line 8-10: `if not prompt:`**: Performs basic input validation, returning a `400 Bad Request` if the mandatory `"prompt"` field is absent.
* **Line 12: `environment = os.getenv("APP_ENV", "development")`**: Dynamically reads the current execution environment (development, staging, production) from environment settings.
* **Line 16: `logger.error(...)`**: Catches and records detailed error stack traces locally while hiding details from the end-user.
"""
    elif "python --version" in code:
        return """
### What This Code Does
This command snippet verifies that the local environment has Python and Git installed, which are the fundamental command-line dependencies required to run the AgentCore CLI and local development scripts.

### Code Walkthrough
* **Line 1: `python --version`**: Queries the active Python interpreter to verify its version.
* **Line 2: `git --version`**: Queries the local Git installation to verify that version control is configured.
"""
    elif "version: \"1.0\"" in code:
        return """
### What This Code Does
This configuration file defines deployment parameters for the AgentCore application, mapping the agent's logical name, its target foundation model on Bedrock, and its execution IAM role.

### Code Walkthrough
* **Line 1: `version: "1.0"`**: Specifies the configuration schema version.
* **Line 3: `name: "bedrock-intro-agent"`**: The unique name identifier for the agent service deployment.
* **Line 4: `model: "anthropic.claude-3-5-sonnet-v2"`**: Specifies the Bedrock Model ID to invoke for the agent's core cognitive reasoning loop.
* **Line 5: `execution_role_arn: ...`**: Configures the IAM Role that the runtime container will assume to acquire secure temp AWS credentials.
"""
    # Fallback default mock
    return f"""
### What This Code Does
This is a code block in language `{lang}` which forms part of Block {block_idx}.

### Code Walkthrough
* Core imports, functions, and structures are configured to enable specific tasks in this module.
"""

def generate_explanation(client, model, chapter_title, lang, code, block_idx, context=""):
    """Queries Gemini to generate code explanations."""
    if not client:
        return get_mock_explanation(lang, code, block_idx)

    prompt = f"""You are an expert technical writer and AI engineer.
We are building a production-ready developer handbook for AWS Bedrock AgentCore.
Your task is to write a detailed, production-grade pedagogical explanation for the code snippet below.

The code snippet is from Chapter: {chapter_title}
Context around the code: {context}

Here is the code block (language: {lang}):
```{lang}
{code}
```

Please generate a deep-dive explanation with exactly these 2 standardized headings. Do not output anything else (like intro or outro text), start directly with the first heading. Use markdown `###` for headings:

### What This Code Does
[A concise explanation of the code snippet's role in the module.]

### Code Walkthrough
[A line-by-line or section-by-section breakdown of imports, classes, functions, and key operations.]"""

    max_retries = 6
    backoff = 10
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            return response.text
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str or "exhausted" in err_str or "rate limit" in err_str:
                print(f"  Rate limit hit: {e}. Retrying in {backoff} seconds (Attempt {attempt+1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2
            else:
                print(f"Error querying Gemini: {e}")
                print("Falling back to local mock data...")
                return get_mock_explanation(lang, code, block_idx)

    print("Max retries exceeded. Falling back to local mock data...")
    return get_mock_explanation(lang, code, block_idx)


def enrich_file(file_path, client, model, dry_run=False, limit=None, force_mock=False):
    """Enriches a single markdown file with explanations for its code blocks."""
    print(f"Processing: {os.path.basename(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    title = get_chapter_title(content)
    segments = parse_markdown_blocks(content)
    
    modified = False
    blocks_processed = 0
    
    # We loop through the segments. Code blocks are at odd indices.
    for i in range(1, len(segments), 2):
        seg = segments[i]
        lang = seg["lang"].strip()
        code = seg["code"]
        
        # Skip mermaid diagrams
        if lang.lower() == "mermaid":
            continue
            
        # Check if already followed by explanation
        next_text_seg = segments[i+1] if i+1 < len(segments) else None
        if next_text_seg and is_explained(next_text_seg):
            print(f"  Block {blocks_processed+1} ({lang}): Already explained. Skipping.")
            blocks_processed += 1
            continue
            
        blocks_processed += 1
        print(f"  Block {blocks_processed} ({lang}): Needs explanation.")
        
        if dry_run:
            continue
            
        if limit is not None and blocks_processed > limit:
            print(f"  Reached processing limit of {limit} blocks. Stopping.")
            break
            
        # Context extraction: get preceding text snippet
        prev_text = segments[i-1]["content"][-400:] if i-1 >= 0 else ""
        
        # Generate
        effective_client = None if force_mock else client
        explanation = generate_explanation(effective_client, model, title, lang, code, blocks_processed, prev_text)
        
        # Insert explanation into the start of the next text segment
        if next_text_seg:
            orig_text = next_text_seg["content"]
            # Prepend the explanation with proper spacing
            next_text_seg["content"] = f"\n{explanation.strip()}\n\n{orig_text.lstrip()}"
        else:
            # Create a new text segment at the end
            segments.append({"type": "text", "content": f"\n{explanation.strip()}\n"})
            
        modified = True
        
        # Rate limit safety delay
        if client and not force_mock:
            time.sleep(1)

    if modified and not dry_run:
        # Create backup if not already present
        backup_dir = os.path.join(os.path.dirname(file_path), "backup")
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, os.path.basename(file_path) + ".bak")
        if not os.path.exists(backup_path):
            with open(backup_path, "w", encoding="utf-8") as bf:
                bf.write(content)
            print(f"  Created backup at: {backup_path}")
            
        # Save updated file
        new_content = rebuild_markdown(segments)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Successfully updated: {file_path}")
        
    return blocks_processed, modified

def main():
    parser = argparse.ArgumentParser(description="Enrich Bedrock AgentCore course chapters with pedagogical code explanations.")
    parser.add_argument("--file", help="Specific markdown file to enrich (relative to doc_uday_advance_notes/)")
    parser.add_argument("--dry-run", action="store_true", help="Count blocks and check status without generating contents")
    parser.add_argument("--limit", type=int, help="Limit number of code blocks to process in this run")
    parser.add_argument("--force-mock", action="store_true", help="Skip Gemini API and use offline pre-defined explanations")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini API Model ID")
    args = parser.parse_args()

    workspace_dir = r"c:\Users\nishu\workspace\wscs_bedrock"
    docs_dir = os.path.join(workspace_dir, "doc_uday_advance_notes")
    
    # Initialize Gemini client
    client = None
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and not args.force_mock:
        try:
            client = genai.Client(api_key=api_key)
            print("Gemini client successfully initialized.")
        except Exception as e:
            print(f"Error initializing Gemini client: {e}. Falling back to offline mock mode.")
    else:
        print("GEMINI_API_KEY environment variable not found or --force-mock specified. Operating in mock mode.")

    # Determine target files
    files_to_process = []
    if args.file:
        full_path = os.path.join(docs_dir, args.file)
        if os.path.exists(full_path):
            files_to_process.append(full_path)
        else:
            print(f"Error: File not found: {full_path}")
            return
    else:
        for name in os.listdir(docs_dir):
            if name.startswith("0") or name.startswith("1"):
                if name.endswith(".md"):
                    files_to_process.append(os.path.join(docs_dir, name))
        files_to_process.sort()

    print(f"Found {len(files_to_process)} chapters to process.")
    
    total_blocks = 0
    total_modified = 0
    
    for file_path in files_to_process:
        blocks, mod = enrich_file(file_path, client, args.model, args.dry_run, args.limit, args.force_mock)
        total_blocks += blocks
        if mod:
            total_modified += 1
            
    print("==========================================")
    print(f"Run completed. Total blocks verified/processed: {total_blocks}. Files modified: {total_modified}")
    print("==========================================")

if __name__ == "__main__":
    main()
