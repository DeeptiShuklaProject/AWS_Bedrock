import os
import glob
import re

bedrock_dir = r"c:\Users\nishu\workspace\wscs_bedrock\doc_uday_bedrock_notes"

def generate_chapter_quizzes(ch_num, title):
    quizzes = []
    
    topics = [
        ("Architecture & Core Purpose", f"What is the main objective of {title} in AWS Bedrock AgentCore?"),
        ("Security Boundaries", f"How does {title} maintain tenant security and isolation at runtime?"),
        ("Configuration Standards", f"Which configuration standard is recommended when setting up {title}?"),
        ("Error Handling", f"How should exception handling be implemented during {title} operations?"),
        ("Performance Metrics", f"What is the key performance metric to monitor for {title}?"),
        ("Scalability Design", f"How does Bedrock AgentCore scale {title} under heavy user traffic?"),
        ("IAM Access Control", f"Which IAM policy permission is vital for {title}?"),
        ("SDK Integration", f"Which Boto3 SDK module directly interacts with {title}?"),
        ("Session State", f"How does session state interact with {title} across multi-turn requests?"),
        ("Containerization", f"What role does Docker containerization play in {title}?"),
        ("Observability", f"Which OpenTelemetry span metric tracks {title} execution latency?"),
        ("Troubleshooting 403", f"What is the common fix if {title} returns HTTP 403 Access Denied?"),
        ("Troubleshooting 500", f"What is the primary root cause of HTTP 500 internal errors during {title}?"),
        ("ReAct Framework", f"How does {title} integrate into the Thought-Action-Observation loop?"),
        ("Cost Optimization", f"Which practice minimizes operational costs when running {title}?"),
        ("Memory Engine", f"How does {title} retrieve stored context from DynamoDB or vector stores?"),
        ("API Gateway Routing", f"How does the API Gateway format incoming requests before passing to {title}?"),
        ("MicroVM Isolation", f"Why are AWS Firecracker microVMs preferred over traditional containers for {title}?"),
        ("Production Best Practices", f"What is a critical production antipattern to avoid when deploying {title}?"),
        ("Enterprise Integration", f"How does {title} integrate with existing enterprise REST endpoints and microservices?")
    ]

    for idx, (aspect, question_text) in enumerate(topics, 1):
        if idx == 1:
            q = f"What is the primary role of {title} in Bedrock AgentCore?"
            opts = [
                f"To provide hardware-isolated, scalable, and code-first execution for {title}.",
                "To store plain text credentials in Git repos.",
                "To run legacy Windows desktop apps.",
                "To disable security permissions."
            ]
            ans = 0
            exp = f"{title} provides enterprise-grade, code-first runtime logic for Bedrock AgentCore."
        elif idx == 2:
            q = f"How does Bedrock AgentCore enforce security for {title}?"
            opts = [
                "By sharing memory across all tenants.",
                "By hosting session runtimes inside isolated AWS Firecracker microVM containers with scoped IAM roles.",
                "By disabling SSL/TLS encryption.",
                "By running code as root on public servers."
            ]
            ans = 1
            exp = "Firecracker microVMs deliver hardware-level security boundaries between multi-tenant executions."
        elif idx == 3:
            q = f"Which environment variable loading pattern is recommended for {title}?"
            opts = [
                "Hardcoding values in Python source code files.",
                "Using os.getenv() or Pydantic BaseSettings to read environment configuration dynamically.",
                "Storing secrets in public web pages.",
                "Editing binary files manually."
            ]
            ans = 1
            exp = "12-Factor App principles mandate decoupling configuration from application source code via environment variables."
        elif idx == 4:
            q = f"How should runtime errors be handled in {title} handlers?"
            opts = [
                "Allowing exceptions to crash the container process.",
                "Wrapping invocation logic in try-except blocks and returning clean structured error payloads (e.g. 400/500 status codes).",
                "Ignoring all errors completely.",
                "Printing errors to static HTML files."
            ]
            ans = 1
            exp = "Defensive error trapping prevents unhandled runtime exceptions from crashing container workers."
        elif idx == 5:
            q = f"What key metric should be monitored in CloudWatch for {title}?"
            opts = [
                "Invocation latency, token consumption rates, and HTTP error response counts.",
                "Monitor resolution of user monitors.",
                "Keyboard stroke frequency.",
                "Color contrast ratios."
            ]
            ans = 0
            exp = "Tracking latency and token usage guarantees cost control and performance optimization in production."
        elif idx == 6:
            q = f"How does {title} achieve sub-second scaling during high concurrency?"
            opts = [
                "By leveraging pre-warmed Firecracker microVM snapshots and serverless AWS Fargate clusters.",
                "By restarting physical servers manually.",
                "By deleting user databases.",
                "By restricting app usage to one request per minute."
            ]
            ans = 0
            exp = "Pre-warmed microVM snapshots enable sub-second boot times under peak traffic spikes."
        elif idx == 7:
            q = f"Which IAM action is required to invoke foundation models in {title}?"
            opts = [
                "bedrock:InvokeModel and bedrock:InvokeModelWithResponseStream",
                "s3:DeleteBucket",
                "ec2:TerminateInstances",
                "iam:DeleteUser"
            ]
            ans = 0
            exp = "The bedrock:InvokeModel permission permits agents to call Bedrock foundation models."
        elif idx == 8:
            q = f"Which Python SDK client is used for Amazon Bedrock runtime interactions in {title}?"
            opts = [
                "boto3.client('bedrock-runtime')",
                "urllib2.open()",
                "os.system('cmd')",
                "pandas.read_csv()"
            ]
            ans = 0
            exp = "Boto3 bedrock-runtime provides low-latency access to foundation model inference endpoints."
        elif idx == 9:
            q = f"How is session state maintained across multiple request turns in {title}?"
            opts = [
                "By using unique session identifiers mapped to warm microVMs and persistent DynamoDB memory stores.",
                "By clearing memory after every line.",
                "By saving state in browser cookies only.",
                "Session state cannot be maintained."
            ]
            ans = 0
            exp = "AgentCore combines sticky microVM routing with persistent database backends for session continuity."
        elif idx == 10:
            q = f"Why is Docker multi-stage building recommended for {title} container deployments?"
            opts = [
                "It reduces image file sizes by omitting build dependencies from final production runtime containers.",
                "It makes Docker containers slower.",
                "It forces Python to compile to JavaScript.",
                "It deletes Git version history."
            ]
            ans = 0
            exp = "Multi-stage Docker builds produce lightweight images, reducing deployment times and attack surfaces."
        elif idx == 11:
            q = f"Which tracing standard does Bedrock AgentCore use for end-to-end observability of {title}?"
            opts = [
                "OpenTelemetry (OTel) distributed tracing standards",
                "Custom print() text files",
                "Syslog UDP broadcast",
                "Manual paper logbooks"
            ]
            ans = 0
            exp = "OpenTelemetry enables distributed trace collection across model calls, memory lookups, and tool executions."
        elif idx == 12:
            q = f"What is the recommended solution if {title} returns a 403 Forbidden status during Bedrock invocations?"
            opts = [
                "Verify IAM role policies and confirm foundation model access is enabled in the AWS Bedrock Console.",
                "Reinstall the operating system.",
                "Delete the AWS account.",
                "Use an unencrypted connection."
            ]
            ans = 0
            exp = "Model access must be explicitly granted in the AWS Bedrock Console before IAM roles can invoke models."
        elif idx == 13:
            q = f"What is a primary cause of HTTP 500 errors during {title} execution?"
            opts = [
                "Unhandled exceptions in custom Python tool code or missing required payload keys.",
                "Network speeds exceeding 1 Gbps.",
                "Using Python 3.11 instead of Python 2.7.",
                "High GPU availability."
            ]
            ans = 0
            exp = "Uncaught exceptions within tool handlers or missing request keys trigger 500 Internal Server errors."
        elif idx == 14:
            q = f"Where does {title} fit into the ReAct (Reason + Act) loop pattern?"
            opts = [
                "It executes reasoning steps, structures tool parameters, and processes observations.",
                "It bypasses the model completely.",
                "It only runs when offline.",
                "It formats HTML styling tags."
            ]
            ans = 0
            exp = "AgentCore coordinates the continuous cycle of LLM reasoning, tool invocation, and observation processing."
        elif idx == 15:
            q = f"How can API cost be optimized when operating {title} at high volume?"
            opts = [
                "By caching model responses, optimizing prompt lengths, and choosing appropriate foundation model tiers.",
                "By sending empty prompts repeatedly.",
                "By turning off logging.",
                "By disabling database indexes."
            ]
            ans = 0
            exp = "Prompt caching and selecting model size according to task complexity drastically cuts inference spending."
        elif idx == 16:
            q = f"How does the Memory Engine support long-term retrieval in {title}?"
            opts = [
                "By indexing conversational history and vector embeddings into persistent storage like Amazon DynamoDB or OpenSearch.",
                "By storing files in temporary RAM.",
                "By requiring users to re-enter prompts every time.",
                "Memory Engine is not supported."
            ]
            ans = 0
            exp = "Vector stores and DynamoDB backing enable long-term semantic memory retrieval across sessions."
        elif idx == 17:
            q = f"What role does the API Gateway play in front of {title}?"
            opts = [
                "It provides authentication, rate limiting, request validation, and routing to backend microVM workers.",
                "It replaces the foundation model.",
                "It generates synthetic test data.",
                "It compiles Python code into C."
            ]
            ans = 0
            exp = "API Gateways secure entry points and shield agent runtime workers from unauthorized or throttled traffic."
        elif idx == 18:
            q = f"Why are Firecracker microVMs superior to standard Docker containers for multi-tenant {title} workloads?"
            opts = [
                "They offer minimal virtualization overhead with strict hardware-isolated kernel boundaries between tenant workloads.",
                "They require 100GB of RAM to start.",
                "They do not support Linux.",
                "They are slower than full virtual machines."
            ]
            ans = 0
            exp = "Firecracker provides VM-grade security with container-grade startup speed and minimal memory footprint."
        elif idx == 19:
            q = f"What production antipattern should be strictly avoided when designing {title}?"
            opts = [
                "Hardcoding AWS access keys or maintaining stateless logic without error handling.",
                "Using virtual environments.",
                "Writing unit tests for Python code.",
                "Logging trace events to CloudWatch."
            ]
            ans = 0
            exp = "Hardcoded credentials and unhandled exceptions are critical antipatterns in production systems."
        else:
            q = f"How does {title} integrate with enterprise databases and external APIs?"
            opts = [
                "Through standardized Python tool schemas (e.g. Pydantic models) invoked securely via sandboxed tool registries.",
                "By exposing database passwords publicly.",
                "By using manual copy-paste mechanisms.",
                "External integration is unsupported."
            ]
            ans = 0
            exp = "Pydantic-defined tools allow foundation models to execute validated API and database calls safely."

        quizzes.append({
            "question": q,
            "options": opts,
            "answerIndex": ans,
            "explanation": exp
        })
        
    return quizzes

def generate_chapter_playgrounds(ch_num, title):
    playgrounds = []
    
    playground_configs = [
        ("Initialization & Runtime Setup", 
         f"# Snippet 1: Testing Bedrock AgentCore Runtime Setup for {title}\nimport sys\nimport os\n\nprint('=== AgentCore Runtime Init ===')\nprint('Python Version:', sys.version.split()[0])\nprint('Agent Module:', '{title}')\nprint('Status: Active & Ready')"),
        
        ("Configuration & Environment Variables", 
         f"# Snippet 2: Validating Environment Configuration for {title}\nimport json\nimport os\n\nconfig = {{\n    'AWS_REGION': os.getenv('AWS_REGION', 'us-east-1'),\n    'MODEL_ID': os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet'),\n    'TIMEOUT_SEC': int(os.getenv('TIMEOUT_SEC', '30')),\n    'DEBUG_MODE': os.getenv('DEBUG', 'true').lower() == 'true'\n}}\nprint('Loaded Configuration:')\nprint(json.dumps(config, indent=2))"),

        ("Defensive Error Handling & Payload Parsing", 
         f"# Snippet 3: Defensive Request Handler for {title}\ndef process_request(payload):\n    try:\n        prompt = payload.get('prompt')\n        if not prompt:\n            return {{'statusCode': 400, 'error': 'Prompt parameter is required.'}}\n        session_id = payload.get('session_id', 'default-session')\n        return {{'statusCode': 200, 'message': f'Processed prompt for session: {{session_id}}'}}\n    except Exception as e:\n        return {{'statusCode': 500, 'error': str(e)}}\n\nprint(process_request({{'prompt': 'Execute query', 'session_id': 'sess-102'}}))"),

        ("Boto3 Bedrock Model Invocation Simulation", 
         f"# Snippet 4: Simulating Foundation Model Inference in {title}\nimport json\n\ndef invoke_claude_model(prompt_text):\n    payload = {{\n        'anthropic_version': 'bedrock-2023-05-31',\n        'max_tokens': 1000,\n        'messages': [{{'role': 'user', 'content': prompt_text}}]\n    }}\n    print('Sending payload to Bedrock Converse API for {title}...')\n    response = {{\n        'id': 'msg_01X99',\n        'role': 'assistant',\n        'content': [{{'type': 'text', 'text': f'Agent response generated for input: \"{{prompt_text}}\"'}}]\n    }}\n    return response\n\nres = invoke_claude_model('Summarize system health')\nprint('Model Response:', res['content'][0]['text'])"),

        ("ReAct Reasoning Loop Execution", 
         f"# Snippet 5: ReAct (Reason + Act) Loop Simulation for {title}\ndef run_react_cycle(user_input):\n    print('1. [THOUGHT] Analyzing user query:', user_input)\n    print('2. [ACTION] Selected tool: query_system_database')\n    observation = {{'table': 'logs', 'records_found': 42}}\n    print('3. [OBSERVATION] Tool output received:', observation)\n    print('4. [FINAL ANSWER] Processing complete based on retrieved observation.')\n\nrun_react_cycle('Check database log entries')"),

        ("Pydantic Tool Registration & Schema Validation", 
         f"# Snippet 6: Pydantic Tool Parameter Validation for {title}\nfrom pydantic import BaseModel, Field\n\nclass SystemQuerySchema(BaseModel):\n    target_system: str = Field(description='Name of the subsystem to query')\n    limit: int = Field(default=10, ge=1, le=100)\n\ndef execute_tool(data: SystemQuerySchema):\n    print(f'Executing query on {{data.target_system}} with limit={{data.limit}}...')\n    return {{'status': 'success', 'data': ['Item A', 'Item B']}}\n\nquery = SystemQuerySchema(target_system='AgentCore-Runtime', limit=5)\nprint('Tool Result:', execute_tool(query))"),

        ("MicroVM Session State & Memory Engine", 
         f"# Snippet 7: MicroVM Session & Memory Management in {title}\nclass SessionMemory:\n    def __init__(self):\n        self.history = []\n    def add_message(self, role, content):\n        self.history.append({{'role': role, 'content': content}})\n    def get_context(self):\n        return self.history[-3:]\n\nmem = SessionMemory()\nmem.add_message('user', 'Hello Agent!')\nmem.add_message('assistant', 'How can I assist you?')\nmem.add_message('user', 'Show memory status.')\nprint('Active Memory Context:', mem.get_context())"),

        ("OpenTelemetry Tracing & Telemetry Logging", 
         f"# Snippet 8: OpenTelemetry Trace Event Simulation for {title}\nimport time\n\ndef log_otel_span(span_name, duration_ms, status_code='OK'):\n    telemetry_record = {{\n        'trace_id': '0x4bf92f3577b34da6a3ce929d0e0e4736',\n        'span_id': '0x00f067aa0ba902b7',\n        'name': span_name,\n        'duration_ms': duration_ms,\n        'attributes': {{\n            'http.status_code': 200,\n            'agent.module': '{title}'\n        }}\n    }}\n    print(f'[OTel Span Event] {{span_name}} executed in {{duration_ms}}ms ({{status_code}})')\n    return telemetry_record\n\nlog_otel_span('{title}_Invocation', 142)"),

        ("Docker Container Health Check Simulation", 
         f"# Snippet 9: Container MicroVM Health Status for {title}\ndef check_container_health():\n    status = {{\n        'container_id': 'firecracker-uvm-9901',\n        'health': 'HEALTHY',\n        'memory_allocated_mb': 512,\n        'cpu_usage_pct': 4.2,\n        'active_connections': 1\n    }}\n    print('MicroVM Runtime Status:')\n    for k, v in status.items():\n        print(f'  - {{k}}: {{v}}')\n\ncheck_container_health()"),

        ("End-to-End Execution Pipeline Test", 
         f"# Snippet 10: Complete End-to-End Pipeline Execution for {title}\ndef run_full_pipeline(input_prompt):\n    print(f'1. Gateway: Received request \"{{input_prompt}}\"')\n    print('2. Identity: Authenticated IAM session role')\n    print('3. Runtime: Allocated Firecracker MicroVM container')\n    print('4. Execution: Model invoked ReAct reasoning loop')\n    print('5. Response: 200 OK returned to client')\n    return {{'status': 'SUCCESS', 'result': 'Pipeline completed.'}}\n\nprint(run_full_pipeline('Run complete diagnostic check'))")
    ]

    for title_desc, code_str in playground_configs:
        playgrounds.append({
            "instruction": f"{title_desc} for {title}.",
            "code": code_str
        })
        
    return playgrounds

def format_quiz_jsx(q):
    clean_options = [opt.replace('"', "'") for opt in q['options']]
    options_str = "[" + ", ".join([f'"{opt}"' for opt in clean_options]) + "]"
    exp_str = q['explanation'].replace('"', "'")
    q_str = q['question'].replace('"', "'")
    return f'<Quiz \n  question="{q_str}" \n  options={options_str} \n  answerIndex={q["answerIndex"]} \n  explanation="{exp_str}" \n/>'

def format_playground_jsx(p):
    code_str = p['code'].replace('\\', '\\\\').replace('`', '\\`').replace('"', '\\"')
    inst_str = p['instruction'].replace('"', "'")
    return f'<InteractiveExample \n  language="python"\n  instruction="{inst_str}"\n  initialCode="{code_str}"\n/>'

def enrich_file_bulk(filepath):
    filename = os.path.basename(filepath)
    basename = os.path.splitext(filename)[0]
    
    title_clean = basename.replace("Chapter_", "").replace("_", " ").title()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean existing Quiz and InteractiveExample tags to ensure fresh clean placement
    content = re.sub(r'<Quiz\s+[\s\S]*?\/>\s*\n*', '', content)
    content = re.sub(r'<InteractiveExample\s+[\s\S]*?\/>\s*\n*', '', content)
    # Also clean any extra 'Knowledge Verification Check' headers created previously
    content = re.sub(r'### Knowledge Verification Check[\s\S]*?\n\n', '', content)

    quizzes_list = generate_chapter_quizzes(basename, title_clean)
    playgrounds_list = generate_chapter_playgrounds(basename, title_clean)

    # 1. Distribute 10 interactive playgrounds evenly throughout the markdown file
    sections = re.split(r'(\n(?=##\s+))', content)
    
    new_sections = []
    playground_idx = 0

    for i, sec in enumerate(sections):
        new_sections.append(sec)
        if sec.startswith("\n## ") and playground_idx < 10:
            p_jsx = format_playground_jsx(playgrounds_list[playground_idx])
            new_sections.append(f"\n\n### Hands-on Code Playground #{playground_idx + 1}\n\n{p_jsx}\n\n")
            playground_idx += 1

    content = "".join(new_sections)

    # Append any remaining playgrounds before Section 18 / Summary / Section 15
    while playground_idx < 10:
        p_jsx = format_playground_jsx(playgrounds_list[playground_idx])
        play_block = f"\n\n### Hands-on Code Playground #{playground_idx + 1}\n\n{p_jsx}\n\n"
        if "## 18. Summary" in content:
            content = content.replace("## 18. Summary", f"{play_block}## 18. Summary")
        elif "## 15. Interview Questions" in content:
            content = content.replace("## 15. Interview Questions", f"{play_block}## 15. Interview Questions")
        else:
            content += play_block
        playground_idx += 1

    # 2. Append all 20 Quizzes under Section 15 (Interview Questions)
    quizzes_jsx = "\n\n".join([format_quiz_jsx(q) for q in quizzes_list])
    quiz_block = f"\n\n### Knowledge Verification Check (20 Interactive Quizzes)\n\n{quizzes_jsx}\n\n"

    if "## 15. Interview Questions" in content:
        content = content.replace("## 15. Interview Questions", f"## 15. Interview Questions\n{quiz_block}")
    elif "## 19. Practice Exercises" in content:
        content = content.replace("## 19. Practice Exercises", f"## 19. Practice Exercises\n{quiz_block}")
    else:
        content += f"\n\n---\n\n## Knowledge Verification Check\n{quiz_block}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Enriched {filename} cleanly with 20 Quizzes and 10 Interactive Playgrounds.")

# Run enrichment across all chapter files
chapter_files = glob.glob(os.path.join(bedrock_dir, "Chapter_*.md"))
print(f"Targeting {len(chapter_files)} chapter files for bulk enrichment...")

for cf in sorted(chapter_files):
    enrich_file_bulk(cf)

print("Bulk enrichment complete! All 17 Bedrock AgentCore chapters now contain 20 Quizzes and 10 Interactive Playgrounds each.")
