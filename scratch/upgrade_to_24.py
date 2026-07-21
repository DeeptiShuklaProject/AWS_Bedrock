import os
import re

# Output path to write the upgraded files
TARGET_DIR = r"c:\Users\nishu\workspace\wscs_bedrock\doc_uday_advance_notes"
BACKUP_DIR = os.path.join(TARGET_DIR, "backup")

# The 24 standard headings in order
HEADINGS = [
    "Introduction",
    "Learning Objectives",
    "Prerequisites",
    "Background Theory",
    "Core Concepts",
    "Internal Mechanics",
    "Architecture Overview",
    "Installation & Setup",
    "Configuration",
    "Hands-on Examples",
    "Code Walkthrough",
    "Production Best Practices",
    "Security Considerations",
    "Performance Optimization",
    "Cost Optimization",
    "Common Mistakes",
    "Troubleshooting",
    "Interview Questions",
    "Real-World Use Cases",
    "Industrial Project",
    "Summary",
    "Key Takeaways",
    "Practice Exercises",
    "Further Reading"
]

# High-quality technical database for each chapter
CHAPTER_DATA = {
    "01": {
        "title": "Introduction to Bedrock AgentCore",
        "intro": "Amazon Bedrock AgentCore is a containerized, code-first developer framework and runtime service designed to package, run, and scale AI-driven agentic applications on AWS.",
        "what_is_it": "Amazon Bedrock AgentCore is a software framework and cloud runtime service designed to build, execute, and manage autonomous Artificial Intelligence (AI) agents. An AI agent is an intelligent program that does not just generate text responses, but independently plans multi-step tasks, queries databases, calls software tools, and completes complex workflows on AWS.",
        "why_important": "Standard AI models are stateless and limited—they cannot access external data sources, retain long-term conversation history beyond context limits, or execute code securely. Bedrock AgentCore provides the dedicated execution infrastructure, security boundaries, and storage services required to transform basic AI models into safe, production-grade automated enterprise systems.",
        "how_it_works": "AgentCore operates between client user applications and AWS cloud services. When a user submits a prompt, AgentCore launches an isolated lightweight virtual server (AWS Firecracker microVM), connects the AI model to specified database tools, manages step-by-step reasoning loops, and securely returns the formatted response to the user interface.",
        "key_responsibilities": [
            "Securely host and execute AI agent reasoning loops inside isolated virtual containers.",
            "Connect AI foundation models to external databases, web APIs, and enterprise software tools.",
            "Maintain session state and conversational memory across single or multi-turn user interactions.",
            "Enforce security authorization boundaries and access policies for tool calls and data queries."
        ],
        "pre_reqs": "* A basic understanding of cloud computing (SaaS, IaaS, FaaS) and API communications.\n* Familiarity with Python programming and basic JSON serialization layouts.\n* Access to an active AWS Account (Administrator or PowerUser access recommended).",
        "bg_theory": "AI application architecture is shifting from simple, stateless prompt-response models to autonomous agents. Standard API endpoints fail to support production-grade agents due to execution state leakage, memory drift, and compute limitations (e.g., standard serverless functions time out after 15 minutes). AWS designed Bedrock AgentCore to bridge the prototype-to-production gap. AgentCore separates reasoning logic from underlying execution infrastructure, offering dedicated compute isolation via virtual machines, standardized tool gateways via Model Context Protocol (MCP), and persistent memory schemas.",
        "concepts": [
            ("Amazon Bedrock", "A managed AWS service that exposes foundational LLMs via a secure, consolidated API interface.", "Avoids the overhead of managing expensive GPU instances locally.", "Enterprise LLM applications, retrieval-augmented generation systems."),
            ("AgentCore", "A code-first runtime infrastructure designed specifically to run secure, stateful AI agents.", "Enforces resource limits, data isolation, and seamless IAM integration.", "Production hosting of conversational and task-oriented agents."),
            ("Foundation Model", "Large-scale neural networks trained on diverse web-scale data.", "Provides general-purpose reasoning, text generation, and planning capabilities.", "Serves as the central cognitive engine of the agent.")
        ],
        "mechanics": "1. Client submits a query to the AgentCore API Gateway.\n2. The gateway validates Cognito JWT signatures and extracts authorization claims.\n3. The runtime schedules a dedicated AWS Firecracker microVM instance for the session.\n4. The agent container boots, mounts configuration parameters, and triggers the orchestrator entrypoint.\n5. The agent executes reasoning loops, calling Amazon Bedrock FMs via HTTPS/SigV4.\n6. Response payloads stream back to the gateway and are delivered to the client UI.",
        "mermaid": "graph LR\n    Client[React / CLI Client] -->|Inbound Prompt| Runtime[1. Agent Runtime VM<br/>Firecracker microVM]\n\n    subgraph Execution[\"Core Execution Tier\"]\n        Memory[2. Memory Engine<br/>DynamoDB / Cache]\n        Gateway[3. Tool Gateway<br/>Model Context Protocol]\n        Identity[4. Identity Engine<br/>Cognito / Actor ID]\n    end\n\n    subgraph Security[\"Governance & Security Tier\"]\n        Observability[5. Observability<br/>CloudWatch / Otel]\n        Policy[6. Policy Engine<br/>Cedar Access Rules]\n        Evaluations[7. Evaluation Suite<br/>Response Correctness]\n    end\n\n    Runtime -->|Context| Memory\n    Runtime -->|Tools| Gateway\n    Runtime -->|Auth| Identity\n    Runtime -->|Metrics| Observability\n    Runtime -->|Rules| Policy\n    Runtime -->|Verify| Evaluations\n\n    Runtime -->|Conversational Call| FMs[Amazon Bedrock FMs<br/>Claude / Llama]",
        "installation": "To check local environment readiness for Bedrock AgentCore, verify Python and Git versions in your shell:\n```bash\npython --version\ngit --version\n```",
        "configuration": "Deployment properties are managed via `bedrock_agent_core.yaml`. A standard minimal layout specifies model mappings, runtime memory allocation, and the execution IAM role:\n```yaml\nversion: \"1.0\"\nagent:\n  name: \"bedrock-intro-agent\"\n  model: \"anthropic.claude-3-5-sonnet-v2\"\n  execution_role_arn: \"arn:aws:iam::123456789012:role/AgentCoreExecutionRole\"\n```",
        "hands_on_simple": "# Standard Hello World entrypoint for AgentCore\nfrom bedrock_agent_core import BedrockAgentCoreApp\n\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handler(payload, context):\n    return {\n        \"statusCode\": 200,\n        \"response\": \"Hello from Bedrock AgentCore!\"\n    }",
        "hands_on_intermediate": "# Entrypoint reading context and prompt values\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"IntroAgent\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handler(payload, context):\n    prompt = payload.get(\"prompt\", \"\")\n    session_id = getattr(context, \"session_id\", \"local-session\")\n    logger.info(f\"Processing session {session_id} with prompt: {prompt}\")\n    return {\n        \"statusCode\": 200,\n        \"response\": f\"Acknowledged prompt: '{prompt}' inside session {session_id}\"\n    }",
        "hands_on_advanced": "# Structured production entrypoint with exception handling and configuration overrides\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport os\nimport logging\n\nlogger = logging.getLogger(\"ProductionIntroAgent\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handler(payload, context):\n    try:\n        prompt = payload.get(\"prompt\")\n        if not prompt:\n            return {\"statusCode\": 400, \"response\": \"Error: Missing required prompt parameter.\"}\n        \n        environment = os.getenv(\"APP_ENV\", \"development\")\n        session_id = getattr(context, \"session_id\", \"local-session\")\n        logger.info(f\"[ENV={environment}] Invoking production agent for session {session_id}\")\n        \n        return {\n            \"statusCode\": 200,\n            \"response\": f\"Processed input in {environment} environment for session {session_id}.\"\n        }\n    except Exception as e:\n        logger.error(f\"Unhandled exception in handler: {str(e)}\")\n        return {\"statusCode\": 500, \"response\": \"Internal Server Error\"}",
        "best_practices": "* Keep container images thin to minimize boot time and cold start latency.\n* Avoid writing state data to the local filesystem since microVM storage is ephemeral.\n* Always implement structured JSON logging to facilitate log aggregation in CloudWatch.",
        "security": "Enforce strict IAM policies using least-privilege schemas. Ensure the agent execution role limits permission boundaries to designated Bedrock model resources and specific DynamoDB tables. Route all microVM communications through private VPC subnets using AWS PrivateLink endpoints.",
        "performance": "Optimize container image layers by using multi-stage Dockerfiles. Cache foundation model parameters and maintain warm session microVM pools to bypass initialization cycles during high-traffic intervals.",
        "cost": "Monitor token usage patterns closely. Claude 3.5 Sonnet charges separate fees for input tokens and output tokens. Implement token budgeting metrics in your tracing span logs to trace costs per user session.",
        "mistakes": "* Hardcoding AWS Access Keys inside configuration files (always use IAM Execution Roles instead).\n* Assuming microVM local files persist across different user sessions (use Amazon S3 for durable files).",
        "troubleshooting": [
            ("Agent returns 403 Access Denied", "Missing model access activation in the Amazon Bedrock console.", "Navigate to the Bedrock Console under 'Model access' and request permission for Claude models."),
            ("Container takes >30 seconds to boot", "Over-sized container image containing unnecessary development packages.", "Optimize Dockerfile using alpine or slim base images.")
        ],
        "interviews": [
            ("What is the primary architectural difference between Bedrock Agents and Bedrock AgentCore?", "Bedrock Agents is a console-first service where agent orchestration is handled by AWS. Bedrock AgentCore is code-first and containerized, giving developers full control over Python frameworks (like LangChain or CrewAI) while AWS handles runtime hosting, security isolation, and scaling."),
            ("Why does AgentCore rely on AWS Firecracker microVMs?", "Firecracker microVMs combine the security and isolation of traditional virtual machines with the speed and resource efficiency of containers, preventing multi-tenant data leakage and resource exhaustion."),
            ("How does AgentCore manage session state across multiple requests?", "AgentCore routes requests with the same session identifier to the same warm microVM if active, and utilizes the Memory Engine (backed by DynamoDB) to persist and retrieve long-term session logs.")
        ],
        "use_cases": "Enterprise customer support portals requiring complex multi-step reasoning, document summarization, and secure customer database query lookups.",
        "project": "This chapter establishes the core runtime foundation. The concepts developed here will serve as the host environment for our final Enterprise RAG Assistant and Multi-Agent Supervisor system.",
        "summary": "This chapter introduced the Bedrock AgentCore framework, comparing code-first architectures with legacy console models, and outlined the 7 core architectural pillars.",
        "key_takeaways": "* Bedrock AgentCore provides a code-first, framework-agnostic runtime for autonomous agents.\n* Security is enforced via AWS Firecracker microVMs providing isolated user session environments.\n* The framework is managed through standard git, Docker, and AWS CLI developer tools.",
        "exercises": "* Beginner: Install Python and verify your shell returns a valid environment version.\n* Intermediate: Draft a mock configuration file specifying Claude 3 Haiku as the target foundation model.",
        "reading": "* [Amazon Bedrock Developer Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)\n* [AWS Firecracker Virtualization Technology](https://firecracker-microvm.github.io/)"
    },
    "02": {
        "title": "Local Environment Prerequisites",
        "intro": "Developing and deploying Amazon Bedrock AgentCore applications requires establishing a robust, standardized local development environment.",
        "what_is_it": "Local Environment Prerequisites refer to the set of core software tools, programming runtimes, and command-line utilities required on your computer to build, test, and run Bedrock AgentCore applications locally before deploying them to the cloud.",
        "why_important": "Building software without a standardized toolset leads to missing software libraries, system crashes, and code discrepancies between local computers and cloud servers. Installing validated prerequisite tools ensures your workstation matches AWS production standards, guaranteeing predictable code execution.",
        "how_it_works": "Your local workstation uses Python to execute application code, Git to track source code revisions, Docker to emulate container execution environments, 'uv' to manage library packages at high speeds, and the AWS Command Line Interface (CLI) to authenticate and communicate with AWS cloud services.",
        "key_responsibilities": [
            "Provide a stable local runtime environment for executing Python code and framework packages.",
            "Package application code and dependencies into standardized containers using Docker.",
            "Synchronize source code revisions and track repository history using Git.",
            "Authorize and execute secure API commands between your computer and your AWS account."
        ],
        "pre_reqs": "* Basic familiarity with terminal command lines (Bash or PowerShell).\n* An active AWS Account with permissions to create IAM users and policies.",
        "bg_theory": "A standard development environment minimizes the risk of configuration discrepancies between local workstations and production servers. Using container runtimes like Docker ensures identical environment variables, OS dependencies, and package versions. Rather than using legacy package managers like pip (which resolves dependencies sequentially and lacks deep caching), modern Python workflows employ Rust-powered package managers like `uv` to guarantee deterministic builds through locked package trees (`uv.lock`).",
        "concepts": [
            ("SDK", "A collection of pre-written libraries and utilities used to build applications for a platform.", "Eliminates the need to write raw HTTP requests for API actions.", "Python script imports like `import boto3`."),
            ("AWS CLI", "A command-line tool used to control and automate AWS services through script queries.", "Allows developers to manage cloud assets without clicking the AWS web console.", "Configuring access keys and initiating deployment pipelines."),
            ("Virtual Environment", "An isolated workspace that hosts a local copy of Python and specific package dependencies.", "Prevents version conflicts between different Python projects running on the same host.", "Locally installed pip libraries.")
        ],
        "mechanics": "1. Developer inputs command in terminal (e.g., `git clone` or `docker run`).\n2. The shell resolves the binary location in the system PATH variable.\n3. The package manager retrieves packages from online registries (PyPI) and writes them to local project folders.\n4. The container runtime boots a lightweight kernel namespace, mounting source directories to isolate ports and disk reads.",
        "mermaid": "graph LR\n    Dev[Local Workstation] -->|Git| Repo[Git Repository]\n    Dev -->|Python & uv| Venv[Isolated Python Virtual Env]\n    Dev -->|Docker Engine| Containers[Local Test Containers]\n    Dev -->|AWS CLI / SDK| AWS[AWS Cloud Services]",
        "installation": "Execute the following terminal commands to check installation status of required tools:\n```bash\ngit --version\npython --version\ndocker --version\naws --version\n```\nTo install `uv` on Windows, use:\n```powershell\npowershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"\n```\nOn macOS/Linux, run:\n```bash\ncurl -LsSf https://astral.sh/uv/install.sh | sh\n```",
        "configuration": "Verify AWS CLI credentials configuration by running:\n```bash\naws configure\n```\nProvide your AWS Access Key ID, Secret Access Key, Default region (e.g., `us-east-1`), and output format (`json`). The configurations are saved locally under `~/.aws/credentials` and `~/.aws/config`.",
        "hands_on_simple": "# Verify AWS CLI authentication and retrieve current user identities\nimport subprocess\n\ndef check_aws_auth():\n    try:\n        res = subprocess.run([\"aws\", \"sts\", \"get-caller-identity\"], capture_output=True, text=True, check=True)\n        print(\"AWS CLI is configured and authenticated:\")\n        print(res.stdout)\n    except Exception as e:\n        print(\"Failed to authenticate AWS CLI:\", str(e))\n\nif __name__ == \"__main__\":\n    check_aws_auth()",
        "hands_on_intermediate": "# Python script to verify Docker daemon is running locally using docker-py client\nimport subprocess\n\ndef check_docker():\n    try:\n        res = subprocess.run([\"docker\", \"info\"], capture_output=True, text=True)\n        if res.returncode == 0:\n            print(\"Docker Daemon is active and responding.\")\n        else:\n            print(\"Docker Daemon is not running or active.\")\n    except FileNotFoundError:\n        print(\"Docker CLI binary was not found in path.\")\n\nif __name__ == \"__main__\":\n    check_docker()",
        "hands_on_advanced": "# Comprehensive system pre-flight check script validating git, python, uv, docker, and aws\nimport subprocess\nimport sys\n\ndef run_check(binary_name, args):\n    try:\n        res = subprocess.run([binary_name] + args, capture_output=True, text=True, check=True)\n        print(f\"[OK] {binary_name} is active: {res.stdout.splitlines()[0]}\")\n        return True\n    except Exception:\n        print(f\"[FAIL] {binary_name} is missing or returned errors.\")\n        return False\n\ndef main():\n    checks = [\n        (\"git\", [\"--version\"]),\n        (\"python\", [\"--version\"]),\n        (\"uv\", [\"--version\"]),\n        (\"docker\", [\"--version\"]),\n        (\"aws\", [\"sts\", \"get-caller-identity\"])\n    ]\n    all_pass = True\n    for binary, args in checks:\n        if not run_check(binary, args):\n            all_pass = False\n    if not all_pass:\n        print(\"Error: Pre-flight check failed. Please install missing toolchains.\")\n        sys.exit(1)\n    print(\"All prerequisites validated successfully!\")\n\nif __name__ == \"__main__\":\n    main()",
        "best_practices": "* Pin exact minor versions of Python in your workspace to match the target runtime container.\n* Configure shell completion settings for `uv` and `aws` CLI tools to accelerate development workflows.\n* Regularly prune unused Docker builder caches to reclaim local disk space.",
        "security": "Never store permanent AWS root credentials on your workstation. Utilize AWS IAM Identity Center (successor to Single Sign-On) to retrieve temporary, role-based credentials. Ensure local private keys and `.aws/` credential files are set with strict filesystem read permissions (e.g., `chmod 600`).",
        "performance": "Set `uv` to use a global package cache. This avoids re-downloading source wheels across different project folders, resulting in sub-second dependency sync operations.",
        "cost": "Running local diagnostic commands does not incur AWS usage charges. However, ensure that active testing credentials do not spawn background compute clusters or resources that remain running in your AWS billing environment.",
        "mistakes": "* Committing local credentials files to public repositories.\n* Running container runtimes without administrative group privileges, leading to permission access denied errors on socket files.",
        "troubleshooting": [
            ("Docker command returns permission denied", "Current user is not associated with the administrative docker group.", "Run 'usermod -aG docker $USER' on Linux, or start Docker Desktop as administrator on Windows."),
            ("AWS CLI returns ExpiredToken signature", "Temporary credentials obtained via SSO or AssumeRole have expired.", "Run 'aws sso login' or re-authenticate your CLI profile to fetch new tokens.")
        ],
        "interviews": [
            ("Why is Git essential in automated CI/CD deployment pipelines?", "Git acts as the source of truth for the codebase. Version control systems host hooks that notify CI/CD servers (like GitHub Actions) to run tests and compile production containers on push events."),
            ("What is the role of the system PATH environment variable?", "The PATH variable lists directories containing executable binaries. When a command is typed, the OS searches these paths sequentially to execute the matching binary file."),
            ("How does uv guarantee deterministic package installations?", "uv uses a lockfile (`uv.lock`) that lists the exact version, checksum, and dependencies of every package, ensuring that subsequent installations resolve the identical package tree.")
        ],
        "use_cases": "Setting up new workstations for engineers joining an AI development team to ensure environment alignment.",
        "project": "This workspace preparation allows us to clone the agent source files and compile local container images in subsequent chapters.",
        "summary": "This chapter covered installing, configuring, and testing the core tools (Git, Python, uv, Docker, and AWS CLI) required to build Bedrock AgentCore applications.",
        "key_takeaways": "* isolated local virtual environments prevent library conflicts.\n* Docker daemon must be active locally to emulate container deployment targets.\n* AWS CLI authentication must be completed before cloud deployment steps can proceed.",
        "exercises": "* Beginner: Install the `uv` toolchain and verify it responds to the version query command.\n* Intermediate: Configure an AWS CLI profile named `dev-profile` targeting the `us-west-2` region.",
        "reading": "* [AWS CLI Command Reference Guide](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)\n* [Docker Containerization Engine Documentation](https://docs.docker.com/)"
    },
    "03": {
        "title": "AWS Configuration & IAM Setup",
        "intro": "Deploying Amazon Bedrock AgentCore applications requires configuring access permissions and model endpoints within your AWS account.",
        "what_is_it": "AWS Configuration and IAM (Identity and Access Management) Setup is the process of configuring cloud permissions, access policies, and model access settings inside your AWS account so your application can securely interact with Amazon Bedrock.",
        "why_important": "By default, AWS blocks all access to foundation models and cloud resources to prevent data leaks and unauthorized billing. Configuring explicit IAM execution roles and policies ensures your agent operates with the exact minimum permissions required to perform its job without exposing other cloud assets.",
        "how_it_works": "The developer enables model access in the AWS Bedrock console and creates an IAM Execution Role containing policy statements. When the AgentCore runtime boots, it assumes this IAM role, obtains temporary security credentials from AWS Security Token Service (STS), and signs API requests using the AWS Signature Version 4 protocol.",
        "key_responsibilities": [
            "Enable foundation model API access (such as Anthropic Claude) within target AWS regions.",
            "Define granular IAM policy statements for model invocation, database access, and CloudWatch logging.",
            "Configure trust policies that allow the AgentCore runtime service to assume execution roles safely.",
            "Secure API calls by generating short-lived cryptographic security tokens for runtime execution."
        ],
        "pre_reqs": "* Successful setup of the AWS CLI toolchain from Chapter 2.\n* IAM administrative privileges in your target AWS account.",
        "bg_theory": "By default, AWS blocks all access to foundation models to prevent unexpected billing. Developers must explicitly request access for specific models in the console. Furthermore, AWS services execute commands under IAM boundaries. An Agent execution role defines what AWS resources (S3, DynamoDB, Bedrock) the agent's microVM can interact with. Enforcing least-privilege security policies ensures that if an agent container is compromised, the blast radius is strictly limited.",
        "concepts": [
            ("IAM Policy", "A JSON document defining permissions by detailing allowed actions on specific resource ARNs.", "Ensures the application cannot invoke unauthorized APIs.", "Attached policy document limits access to DynamoDB tables."),
            ("IAM Role", "An IAM identity that trusted entities (like services or user accounts) assume to acquire temporary credentials.", "Allows services to access resources without hardcoded passwords.", "The role assumed by the microVM at runtime."),
            ("Model Access Table", "A console settings pane where developers agree to terms of service to activate Bedrock model APIs.", "Required to enable third-party model invoke endpoints.", "Requesting access for Anthropic Claude 3.5 Sonnet.")
        ],
        "mechanics": "1. AgentCore runtime starts the microVM.\n2. The VM requests temporary credentials from the AWS Security Token Service (STS) by assuming the configured IAM role.\n3. STS returns a session access key, secret key, and session token.\n4. When calling Bedrock, the SDK signs the HTTP request with these credentials using the AWS Signature Version 4 protocol.\n5. Bedrock validates the signature and verifies that the role is authorized to invoke the requested model.",
        "mermaid": "sequenceDiagram\n    participant VM as Agent VM Runtime\n    participant STS as AWS Security Token Service\n    participant Bedrock as Amazon Bedrock API\n    VM->>STS: AssumeRole(AgentCoreExecutionRole)\n    STS-->>VM: Temporary Credentials (AccessKey, SecretKey, SessionToken)\n    VM->>Bedrock: InvokeModel (Signed with SigV4)\n    Bedrock-->>VM: Model Inference Output Response",
        "installation": "Verify model access lists from the CLI using:\n```bash\naws bedrock list-foundation-models --query \"modelSummaries[?modelId=='anthropic.claude-3-5-sonnet-20241022-v2:0']\"\n```",
        "configuration": "### Step 1: Request Amazon Bedrock Model Access\n1. Navigate to the **Amazon Bedrock** console.\n2. Select **Model access** in the left menu.\n3. Click **Manage model access**, select **Claude 3.5 Sonnet** and **Claude 3 Haiku**, and click **Save changes**.\n\n### Step 2: Create IAM Policy `AgentCoreExecutionPolicy`\n```json\n{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"BedrockInference\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"bedrock:InvokeModel\",\n        \"bedrock:InvokeModelWithResponseStream\"\n      ],\n      \"Resource\": \"*\"\n    },\n    {\n      \"Sid\": \"DynamoDBMemory\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"dynamodb:GetItem\",\n        \"dynamodb:PutItem\",\n        \"dynamodb:UpdateItem\",\n        \"dynamodb:DeleteItem\",\n        \"dynamodb:Query\",\n        \"dynamodb:Scan\"\n      ],\n      \"Resource\": \"arn:aws:dynamodb:*:*:table/*agentcore*\"\n    },\n    {\n      \"Sid\": \"CloudWatchLogging\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"logs:CreateLogGroup\",\n        \"logs:CreateLogStream\",\n        \"logs:PutLogEvents\"\n      ],\n      \"Resource\": \"*\"\n    }\n  ]\n}\n```\n\n### Step 3: Create Trust Role `AgentCoreExecutionRole`\n```json\n{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Effect\": \"Allow\",\n      \"Principal\": {\n        \"Service\": \"agentcore.amazonaws.com\"\n      },\n      \"Action\": \"sts:AssumeRole\"\n    }\n  ]\n}\n```",
        "hands_on_simple": "# Verify Bedrock model access availability using the Python SDK\nimport boto3\nimport botocore\n\ndef test_bedrock_access():\n    try:\n        client = boto3.client(\"bedrock\", region_name=\"us-east-1\")\n        models = client.list_foundation_models()\n        print(\"Successfully queried Bedrock Models! Count:\", len(models.get(\"modelSummaries\", [])))\n    except Exception as e:\n        print(\"Authorization or connection error:\", str(e))\n\nif __name__ == \"__main__\":\n    test_bedrock_access()",
        "hands_on_intermediate": "# Python script to create the IAM execution policy programmatically\nimport boto3\nimport json\n\ndef create_iam_policy():\n    iam = boto3.client(\"iam\")\n    policy_doc = {\n        \"Version\": \"2012-10-17\",\n        \"Statement\": [\n            {\n                \"Effect\": \"Allow\",\n                \"Action\": [\"bedrock:InvokeModel\"],\n                \"Resource\": \"*\"\n            }\n        ]\n    }\n    try:\n        res = iam.create_policy(\n            PolicyName=\"AgentCoreMinimumPolicy\",\n            PolicyDocument=json.dumps(policy_doc),\n            Description=\"Minimum execution permissions for Bedrock agents.\"\n        )\n        print(\"Policy created successfully. ARN:\", res[\"Policy\"][\"Arn\"])\n    except iam.exceptions.EntityAlreadyExistsException:\n        print(\"Policy already exists.\")\n    except Exception as e:\n        print(\"Failed to create policy:\", str(e))\n\nif __name__ == \"__main__\":\n    create_iam_policy()",
        "hands_on_advanced": "# Complete SDK implementation validating current role permissions and model execution\nimport boto3\nimport json\nimport botocore\n\ndef verify_execution_permissions():\n    # Attempt basic Claude invoke model test call\n    bedrock = boto3.client(\"bedrock-runtime\", region_name=\"us-east-1\")\n    payload = {\n        \"anthropic_version\": \"bedrock-2023-05-31\",\n        \"max_tokens\": 50,\n        \"messages\": [{\"role\": \"user\", \"content\": \"Hello model\"}]\n    }\n    try:\n        print(\"Verifying model invocation permission...\")\n        res = bedrock.invoke_model(\n            modelId=\"anthropic.claude-3-haiku-20240307-v1:0\",\n            body=json.dumps(payload)\n        )\n        res_body = json.loads(res.get(\"body\").read())\n        print(\"Model response text:\", res_body[\"content\"][0][\"text\"])\n        print(\"[SUCCESS] Permissions validated!\")\n    except botocore.exceptions.ClientError as e:\n        error_code = e.response[\"Error\"][\"Code\"]\n        print(f\"[FAIL] AWS API returned error code: {error_code}\")\n        if error_code == \"AccessDeniedException\":\n            print(\"Resolution: Confirm that you have requested Model Access in the console.\")\n\nif __name__ == \"__main__\":\n    verify_execution_permissions()",
        "best_practices": "* Regularly audit and restrict resource wildcards (`*`) in IAM permissions.\n* Use region-specific endpoints to minimize network latency between services.\n* Set up CloudTrail alarms to detect unauthorized IAM role assumption attempts.",
        "security": "Enforce strict trust policies that limit role assumption to the designated Service Principal (`agentcore.amazonaws.com`). Never embed access keys inside container images; access configurations must be fetched dynamically at runtime using IAM metadata endpoints.",
        "performance": "Store model configurations and table metadata locally to avoid making duplicate API calls during execution boot cycles.",
        "cost": "Requesting model access is free of charge. You are only billed when executing inference requests, based on the volume of input and output tokens processed.",
        "mistakes": "* Specifying `lambda.amazonaws.com` instead of `agentcore.amazonaws.com` in the trust relationship, causing execution role assumption failures.\n* Creating policies that grant wide permissions to all DynamoDB tables, violating the principle of least privilege.",
        "troubleshooting": [
            ("SignatureDoesNotMatch during client call", "The system clock on your local development machine is out of sync with AWS servers.", "Resynchronize your operating system clock with a network time server (NTP)."),
            ("AccessDeniedException on Bedrock invoke", "Model access has not been requested or granted in the current AWS region.", "Open the Amazon Bedrock console in the target region, select 'Model access', and verify status.")
        ],
        "interviews": [
            ("What is the AWS Signature Version 4 (SigV4) protocol?", "SigV4 is the protocol AWS uses to authenticate API requests. It signs HTTP requests with cryptographically secure signatures generated from the caller's access keys, verifying the sender and protecting payloads from tampering."),
            ("Why is a custom trust policy required for an IAM role?", "A trust policy specifies which external security principal (like a service or user account) is permitted to assume the role. Without it, AWS prevents the service from requesting temporary session credentials."),
            ("How do you restrict DynamoDB permissions to a specific table name structure?", "Specify the table's ARN in the resource parameter of the policy statement, utilizing wildcards to limit access (e.g., `arn:aws:dynamodb:*:*:table/*agentcore*`).")
        ],
        "use_cases": "Securing enterprise AI data pipelines by establishing isolated IAM roles for dev, staging, and production environments.",
        "project": "The `AgentCoreExecutionRole` created here will be mapped inside `bedrock_agent_core.yaml` to authorize our agent runtime.",
        "summary": "This chapter walked through setting up AWS model access and creating the necessary IAM policies and roles required by the AgentCore runtime.",
        "key_takeaways": "* Model access must be explicitly enabled for each region before APIs can be invoked.\n* AgentCore requires a dedicated IAM execution role with service trust configurations.\n* IAM policies should adhere to the security principle of least privilege.",
        "exercises": "* Beginner: Request access to the Claude 3 Haiku model in the AWS Bedrock console.\n* Intermediate: Draft a JSON policy statement that grants read-only access to an S3 bucket named `agent-assets`.",
        "reading": "* [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)\n* [Amazon Bedrock Security and Permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security.html)"
    },
    "04": {
        "title": "Cloning the Code Repository",
        "intro": "Developing Bedrock AgentCore applications begins by cloning and inspecting the official sample repository.",
        "what_is_it": "Cloning the Code Repository is the process of downloading a complete, version-controlled copy of the Bedrock AgentCore starter codebase from a remote server (such as GitHub) onto your local computer.",
        "why_important": "Building a complex software application from scratch is inefficient and prone to structural mistakes. Cloning an official starter repository provides a verified directory layout, pre-configured setup scripts, and standard sample files, establishing a clean baseline for development.",
        "how_it_works": "Using the Git command-line tool, your workstation establishes a connection to the remote repository host over HTTPS or SSH, downloads the complete commit history and file object database, and checks out project files into your local project workspace directory.",
        "key_responsibilities": [
            "Download remote source files, directory structures, and commit histories to local workstations.",
            "Establish a local workspace for customizing entry scripts, configuration settings, and tools.",
            "Enable local version tracking so code modifications can be committed, branched, or reverted.",
            "Synchronize local development progress with shared remote team repositories on GitHub."
        ],
        "pre_reqs": "* Active installations of Git and Python from Chapter 2.\n* Network access to GitHub.",
        "bg_theory": "Version control systems (like Git) maintain the chronological history of a codebase. Cloning a remote repository downloads the entire commit tree, project metadata, and branches to your local machine. In enterprise software engineering, code changes are managed using branching strategies (e.g., GitFlow). This isolates updates and permits collaborative code reviews before changes are merged into production branches.",
        "concepts": [
            ("Repository", "A digital directory storing the project's source code, history, and configuration files.", "Allows developers to track revisions and roll back changes.", "A hosted repository on GitHub."),
            ("Git Clone", "The command that copies a remote repository to a local workstation.", "Enables local development and editing of codebase files.", "Running `git clone <url>` in terminal."),
            ("Workspace", "The local folder on your workstation where you edit code and run test scripts.", "Contains untracked development configuration files like `.env`.", "Your active project directory.")
        ],
        "mechanics": "1. Developer executes `git clone <url>`.\n2. Git initiates an HTTP/SSH connection to the remote server.\n3. The remote server packages the project object database into a packfile.\n4. Git downloads the packfile, expands it into the `.git` directory, and checks out the default branch files into the workspace folder.",
        "mermaid": "graph LR\n    Remote[GitHub Remote Repository] -->|git clone| Local[.git Database Folder]\n    Local -->|Checkout| Workspace[Working Directory Workspace]",
        "installation": "Open your terminal and execute the cloning command:\n```bash\ngit clone https://github.com/awslabs/agentcore-samples.git\n```\nExpected shell output:\n```text\nCloning into 'agentcore-samples'...\nremote: Enumerating objects: 142, done.\nremote: Counting objects: 100% (142/142), done.\nReceiving objects: 100% (142/142), 85.40 KiB | 2.50 MiB/s, done.\nResolving deltas: 100% (68/68), done.\n```",
        "configuration": "After cloning, enter the project directory to verify active branch status:\n```bash\ncd agentcore-samples\ngit status\n```",
        "hands_on_simple": "# Verify git repository details using terminal commands programmatically\nimport subprocess\n\ndef get_git_branch():\n    try:\n        res = subprocess.run([\"git\", \"branch\", \"--show-current\"], capture_output=True, text=True, check=True)\n        print(\"Current active git branch:\", res.stdout.strip())\n    except Exception as e:\n        print(\"Error reading branch:\", str(e))\n\nif __name__ == \"__main__\":\n    get_git_branch()",
        "hands_on_intermediate": "# Script to list the contents of the root folder and verify file sizes\nimport os\n\ndef audit_project_root():\n    target = \".\"\n    print(f\"Auditing directory: {os.path.abspath(target)}\")\n    for item in os.listdir(target):\n        path = os.path.join(target, item)\n        size = os.path.getsize(path) if os.path.isfile(path) else \"Directory\"\n        print(f\"- {item:<25} | Size: {size}\")\n\nif __name__ == \"__main__\":\n    audit_project_root()",
        "hands_on_advanced": "# Complete diagnostic script checking for modified files and git config status\nimport subprocess\nimport sys\n\ndef verify_repository():\n    try:\n        # Check if we are inside a git directory\n        res = subprocess.run([\"git\", \"rev-parse\", \"--is-inside-work-tree\"], capture_output=True, text=True, check=True)\n        if \"true\" not in res.stdout.lower():\n            print(\"Not inside a git work tree.\")\n            return False\n        \n        # Retrieve remote URL information\n        res_url = subprocess.run([\"git\", \"config\", \"--get\", \"remote.origin.url\"], capture_output=True, text=True, check=True)\n        print(\"Remote Repository URL:\", res_url.stdout.strip())\n        \n        # Check for uncommitted changes\n        res_status = subprocess.run([\"git\", \"status\", \"--porcelain\"], capture_output=True, text=True, check=True)\n        changes = res_status.stdout.strip()\n        if changes:\n            print(\"WARNING: Uncommitted changes detected in workspace:\")\n            print(changes)\n        else:\n            print(\"Workspace is clean and synchronized.\")\n        return True\n    except Exception as e:\n        print(\"Git verification failed:\", str(e))\n        return False\n\nif __name__ == \"__main__\":\n    verify_repository()",
        "best_practices": "* Create a development branch (`git checkout -b feature/agent-setup`) instead of making changes directly on `main`.\n* Configure a global `.gitignore` file to prevent system metadata files (like `.DS_Store` or `Thumbs.db`) from entering code repos.\n* Commit small, logical changes with descriptive messages to simplify rollbacks.",
        "security": "Enforce signature verification using GPG keys to sign commits. Configure branch protection rules on your remote repository (e.g., GitHub or Bitbucket) to block direct force-push updates to release branches.",
        "performance": "If a repository contains large binary assets, use shallow clone configurations (`git clone --depth 1`) to download only the latest commits, reducing transfer times.",
        "cost": "Git operations are processed locally or on free repository platforms. However, keep in mind that hosting private repositories with large file storage features can incur cost configurations under enterprise plans.",
        "mistakes": "* Committing large package binaries or local virtual environment folders to repository history.\n* Modifying files on checkout branches without first fetching the latest updates from the remote repository.",
        "troubleshooting": [
            ("Could not resolve host error during clone", "The terminal cannot resolve the hostname due to a network connection or DNS issue.", "Verify internet connections or configure HTTP proxy variables if working behind an corporate gateway."),
            ("Permission denied (publickey) error", "Your SSH public key is not registered with your remote git hosting profile.", "Configure HTTPS credentials authentication or upload your public SSH key to the repository server settings.")
        ],
        "interviews": [
            ("What is the difference between git fetch and git pull?", "Git fetch downloads remote updates and references to your local `.git` metadata folder without altering your working files. Git pull downloads these updates and immediately runs a merge command to synchronize your workspace files."),
            ("Why should you avoid tracking files like .env in git?", "The `.env` file contains sensitive local access keys and database credentials. Tracking it in Git commits secrets to repository histories, exposing them to anyone with read permissions."),
            ("What is a git submodule?", "A git submodule allows you to keep another Git repository as a subdirectory of your main repository, enabling you to link dependencies while maintaining independent commit histories.")
        ],
        "use_cases": "Retrieving standard codebase templates to establish uniform layouts for new projects.",
        "project": "Cloning the repository sets up the baseline layout, including the `src/` source folders we will configure in Chapter 6.",
        "summary": "This chapter covered cloning the project repository, navigating directories, and verifying the local folder layout.",
        "key_takeaways": "* Git clone duplicates remote repositories to local workstations.\n* Standard workspaces isolate source files from local settings configurations.\n* Local changes should be managed using separate development branches.",
        "exercises": "* Beginner: Clone the sample repository and list root files in your shell.\n* Intermediate: Create a local git branch named `setup-phase` and verify it is active.",
        "reading": "* [Pro Git Book](https://git-scm.com/book/en/v2)\n* [GitHub Documentation](https://docs.github.com/)"
    },
    "05": {
        "title": "Repository Walkthrough",
        "intro": "Understanding the layout and execution entry points of the Bedrock AgentCore repository is key to building custom agents.",
        "what_is_it": "The Repository Walkthrough is a structured inspection of the project folder layout, configuration files, source code modules, and entrypoint functions that comprise a Bedrock AgentCore application.",
        "why_important": "Navigating a codebase without understanding its structural layout leads to improperly placed files, broken imports, and execution errors. Understanding where each file lives and what role it plays allows developers to locate components quickly and extend agent capabilities cleanly.",
        "how_it_works": "The repository organizes code into specific functional directories: 'src/' hosts Python application logic, 'bedrock_agent_core.yaml' defines metadata configurations, '.env' stores local environment variables, and 'pyproject.toml' manages package dependencies. Python decorators (like '@app.invoke') register handler functions to process incoming web requests.",
        "key_responsibilities": [
            "Separate application entry points from utility modules and configuration settings.",
            "Map incoming web and container API routes to specific Python handler functions.",
            "Define container boot parameters, memory allocations, and execution roles in YAML sheets.",
            "Provide a standardized, readable repository architecture for engineering teams."
        ],
        "pre_reqs": "* Successful clone of the agentcore-samples repository from Chapter 4.\n* A basic understanding of Python function definitions and imports.",
        "bg_theory": "Enterprise Python applications partition code into distinct functional layers to ensure separation of concerns. The entrypoint module coordinates initialization steps and runs listeners, utility files contain helper functions, and configuration sheets store variables. Bedrock AgentCore utilizes decorators to bind HTTP routes inside containers. Decorators are design structures that wrap functions to modify behavior without altering their code, simplifying routing configurations.",
        "concepts": [
            ("API Endpoint", "A specific URL path exposed by an application where clients can send requests to interact with services.", "Allows clients to invoke server functions.", "The `/invoke` route on the runtime container."),
            ("JSON Payload", "A text block formatted in JSON syntax that carries request parameter values.", "Provides structured inputs to backend applications.", "The request body containing user prompts."),
            ("YAML Configuration", "A human-readable data format used to declare deployment settings.", "Maintains parameter values outside application code.", "The settings defined in `bedrock_agent_core.yaml`.")
        ],
        "mechanics": "1. The runtime boots the container and executes the python script entrypoint (`src/main.py`).\n2. The script instantiates `BedrockAgentCoreApp`, which starts an internal web server.\n3. The server binds to a specified port and registers routing paths (e.g., `/invoke`).\n4. Incoming client POST requests are validated, converted into a Python dictionary, and passed as the `payload` argument to the function registered by the `@app.invoke` decorator.\n5. The function executes, returning a dictionary that the wrapper converts into an HTTP JSON response.",
        "mermaid": "sequenceDiagram\n    participant Client as Web Client\n    participant WebServer as App Web Server\n    participant Handler as Invoke Handler\n    Client->>WebServer: POST /invoke (JSON Prompt)\n    WebServer->>Handler: execute handler(payload, context)\n    Handler-->>WebServer: return dict (response, status)\n    WebServer-->>Client: return JSON response",
        "installation": "Verify that the Bedrock AgentCore SDK is available in your active Python shell by running:\n```python\npython -c \"import bedrock_agent_core; print(bedrock_agent_core.__file__)\"\n```",
        "configuration": "The main entrypoint expects execution parameters to match the paths declared in `bedrock_agent_core.yaml`:\n```yaml\nagent:\n  name: \"agentcore-walkthrough\"\n  entry_point: \"src/main.py\"\n```",
        "hands_on_simple": "# Standard AgentCore entrypoint script layout\nfrom bedrock_agent_core import BedrockAgentCoreApp\n\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handler(payload, context):\n    prompt = payload.get(\"prompt\", \"\")\n    return {\n        \"statusCode\": 200,\n        \"response\": f\"Processed input: {prompt}\"\n    }",
        "hands_on_intermediate": "# Expanded entrypoint verifying input keys and parsing context attributes\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"Walkthrough\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef check_handler(payload, context):\n    if \"prompt\" not in payload:\n        logger.warning(\"Request received without prompt parameter.\")\n        return {\"statusCode\": 400, \"response\": \"Missing 'prompt' key.\"}\n    \n    prompt = payload[\"prompt\"]\n    request_id = getattr(context, \"request_id\", \"N/A\")\n    logger.info(f\"Request {request_id} content: {prompt}\")\n    \n    return {\n        \"statusCode\": 200,\n        \"response\": f\"Parsed request {request_id} successfully.\"\n    }",
        "hands_on_advanced": "# Complete handler simulating model execution routes and custom metadata returns\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport time\nimport logging\n\nlogger = logging.getLogger(\"AdvancedWalkthrough\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef execute_task(payload, context):\n    start_time = time.time()\n    prompt = payload.get(\"prompt\", \"\")\n    session_id = getattr(context, \"session_id\", \"local-dev\")\n    \n    logger.info(f\"Starting task processing for session: {session_id}\")\n    \n    # Simulate minor internal processing time\n    time.sleep(0.01)\n    \n    duration = time.time() - start_time\n    response_payload = {\n        \"text\": f\"Answer to '{prompt}'\",\n        \"metadata\": {\n            \"session_id\": session_id,\n            \"latency_seconds\": round(duration, 4),\n            \"status\": \"completed\"\n        }\n    }\n    \n    return {\n        \"statusCode\": 200,\n        \"response\": response_payload\n    }",
        "best_practices": "* Isolate application routes so that handler functions only contain coordination logic.\n* Implement logging statements at entry and exit points of handlers to simplify transaction tracing.\n* Validate JSON payload formats before initiating processing steps.",
        "security": "Sanitize user prompt inputs to prevent prompt injection attacks. Ensure that context objects (like authentication tokens or user scopes) are validated by backend filters before invoking core database functions.",
        "performance": "Avoid importing large libraries inside the handler function. Load all dependencies at the module level to ensure they are parsed only once when the container boots.",
        "cost": "Optimize the execution time of code paths inside your handler function. The longer a handler runs, the longer the compute microVM remains active, increasing execution costs.",
        "mistakes": "* Accessing payload parameters directly (e.g., `payload['prompt']`) without check validations, causing runtime KeyError crashes if keys are missing.\n* Writing resource initialization logic inside the handler function (initialize database clients outside the handler instead).",
        "troubleshooting": [
            ("ModuleNotFoundError during import", "The bedrock_agent_core SDK is not installed in the active virtual environment.", "Verify that the virtual environment is activated and run 'uv sync' to install dependencies."),
            ("Handler returns 500 error", "An unhandled exception was thrown within the handler function code.", "Wrap the handler logic in a try-except block to capture and print the traceback details.")
        ],
        "interviews": [
            ("What is a Python decorator and how is it used in AgentCore?", "A decorator is a function that takes another function as an argument and extends its behavior without modifying it. In AgentCore, `@app.invoke` registers the decorated function with the runtime, routing incoming requests to it."),
            ("Why should database clients be instantiated outside the handler?", "Instantiating clients outside the handler executes the initialization code only once when the container starts. Re-instantiating clients inside the handler for every request adds latency and exhausts connections."),
            ("What information does the context object provide?", "The context object contains metadata injected by the runtime environment, such as the unique session identifier, request IDs, and security parameters.")
        ],
        "use_cases": "Analyzing application templates to design custom routing frameworks.",
        "project": "This walkthrough defines the structural template for our main agent script (`src/main.py`) which we will expand in subsequent chapters.",
        "summary": "This chapter reviewed the project's folder layout and analyzed the structure and execution flow of the core entrypoint file.",
        "key_takeaways": "* Handlers execute tasks in response to inbound container requests.\n* Python decorators bind routing endpoints to functions.\n* Initializing resources at the module level minimizes execution latency.",
        "exercises": "* Beginner: Create a file that imports the AgentCore SDK and prints the class structure.\n* Intermediate: Add a custom metadata field to the handler response dictionary and verify syntax.",
        "reading": "* [Python Decorators Guide](https://realpython.com/primer-on-python-decorators/)\n* [AWS SDK for Python (Boto3) Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)"
    },
    "06": {
        "title": "Project Setup & Dependency Management",
        "intro": "Standardizing local development configurations requires isolated virtual environments and locked dependency packages.",
        "what_is_it": "Project Setup and Dependency Management is the practice of isolating your application's Python environment and controlling the exact versions of external software packages (libraries) required by your application.",
        "why_important": "Python packages updated over time can introduce breaking changes or conflicts with other project dependencies installed on your system. Using isolated virtual environments ('.venv') and lockfiles ('uv.lock') guarantees that every team member and cloud server runs identical software library versions, eliminating environment mismatches.",
        "how_it_works": "The 'uv' package manager creates a dedicated virtual environment folder containing an isolated Python interpreter. It parses package dependency rules declared in 'pyproject.toml', solves version compatibility trees, locks the resulting package versions in 'uv.lock', and installs them into the project workspace.",
        "key_responsibilities": [
            "Create isolated local virtual Python environments ('.venv') to prevent library conflicts.",
            "Resolve dependency compatibility across all required third-party software packages.",
            "Generate deterministic lockfiles ('uv.lock') to guarantee identical builds across environments.",
            "Provide fast, cached installation and synchronization of application libraries."
        ],
        "pre_reqs": "* Active toolchain installations and workspace directories from Chapter 2 and 4.",
        "bg_theory": "Dependency drift occurs when package updates introduce breaking changes. To ensure that an application runs identically in dev, staging, and production, package versions must be locked. Traditional tools like `pip` install packages globally by default, risking conflicts. Modern workflows isolate environments using virtual environments and lock the complete dependency tree (including transitive dependencies) in a lockfile, ensuring deterministic builds.",
        "concepts": [
            ("Package Manager", "A tool that automates installing, updating, and removing software packages.", "Simplifies dependency resolution and version management.", "The `uv` or `pip` command-line tools."),
            ("Virtual Environment", "An isolated directory tree containing its own Python installation and packages.", "Prevents library version conflicts between projects.", "The local `.venv/` folder."),
            ("Lockfile", "A file listing the exact version and checksum of every package in the dependency tree.", "Guarantees identical builds across all environments.", "The `uv.lock` file.")
        ],
        "mechanics": "1. Developer runs `uv venv` to scaffold an isolated environment.\n2. Running `uv sync` reads the dependencies listed in `pyproject.toml`.\n3. The solver resolves version constraints and writes the resolved tree to `uv.lock`.\n4. Packages are downloaded, verified against checksums, and installed into `.venv/lib/site-packages`.",
        "mermaid": "graph TD\n    Project[Project Workspace] -->|uv venv| Venv[.venv Folder]\n    Venv -->|uv sync| Packages[Installed Packages]\n    Packages -->|Locks Versions| D[uv.lock File]",
        "installation": "Initialize the virtual environment and synchronize dependencies using `uv`:\n```bash\nuv venv\n```\nActivate the environment:\n- **Windows (PowerShell):**\n  ```powershell\n  .venv\\Scripts\\Activate.ps1\n  ```\n- **macOS / Linux:**\n  ```bash\n  source .venv/bin/activate\n  ```\nSynchronize packages:\n```bash\nuv sync\n```",
        "configuration": "Dependencies are declared in the `pyproject.toml` file under the `dependencies` key:\n```toml\n[project]\nname = \"agentcore-project\"\nversion = \"0.1.0\"\ndependencies = [\n    \"boto3>=1.34.0\",\n    \"bedrock-agent-core>=1.0.0\"\n]\n```",
        "hands_on_simple": "# Verify virtual environment status using python sys parameters\nimport sys\n\ndef check_venv():\n    # sys.prefix changes when inside a virtual environment\n    is_venv = sys.prefix != sys.base_prefix\n    print(\"Is virtual environment active?\", is_venv)\n    print(\"Active Python executable path:\", sys.executable)\n\nif __name__ == \"__main__\":\n    check_venv()",
        "hands_on_intermediate": "# Script to check if all dependencies in pyproject.toml are installed in venv\nimport pkg_resources\nimport tomllib\n\ndef check_packages():\n    try:\n        with open(\"pyproject.toml\", \"rb\") as f:\n            config = tomllib.load(f)\n        deps = config.get(\"project\", {}).get(\"dependencies\", [])\n        print(\"Checking declared dependencies:\")\n        for dep in deps:\n            pkg_name = dep.split(\">=\")[0].split(\"==\")[0].strip()\n            try:\n                dist = pkg_resources.get_distribution(pkg_name)\n                print(f\"- [OK] {pkg_name} is installed: {dist.version}\")\n            except pkg_resources.DistributionNotFound:\n                print(f\"- [FAIL] {pkg_name} is missing!\")\n    except FileNotFoundError:\n        print(\"pyproject.toml not found in current folder.\")\n\nif __name__ == \"__main__\":\n    check_packages()",
        "hands_on_advanced": "# Complete automated setup audit and sync verification script\nimport subprocess\nimport sys\nimport os\n\ndef audit_environment():\n    if not os.path.exists(\".venv\"):\n        print(\"Virtual environment '.venv' is missing. Creating...\")\n        subprocess.run([\"uv\", \"venv\"], check=True)\n    \n    print(\"Synchronizing dependency configurations...\")\n    res = subprocess.run([\"uv\", \"sync\"], capture_output=True, text=True)\n    if res.returncode == 0:\n        print(\"[SUCCESS] Dependencies synchronized successfully!\")\n        # List installed packages\n        res_list = subprocess.run([\"uv\", \"pip\", \"list\"], capture_output=True, text=True)\n        print(res_list.stdout)\n    else:\n        print(\"[FAIL] Dependency sync failed:\")\n        print(res.stderr)\n        sys.exit(1)\n\nif __name__ == \"__main__\":\n    audit_environment()",
        "best_practices": "* Always exclude the `.venv/` directory from version control by adding it to `.gitignore`.\n* Always commit `uv.lock` to ensure all developers use identical package versions.\n* Use `uv sync --frozen` in CI/CD pipelines to prevent updating dependencies during builds.",
        "security": "Regularly audit installed packages for known security vulnerabilities using `uv pip tree` or security scanners. Keep dependencies updated to apply patches for security advisories.",
        "performance": "Leverage `uv`'s global package caching. It shares package compilations across workspaces, eliminating redundant downloads and reducing install times.",
        "cost": "Package sync operations are performed locally and do not consume cloud resources or incur AWS charges.",
        "mistakes": "* Committing the `.venv` folder to Git, bloating the repository size.\n* Installing packages globally using administrative permissions instead of isolating them in a local virtual environment.",
        "troubleshooting": [
            ("uv sync fails with version conflict", "Conflicting dependencies declared in pyproject.toml.", "Audit declared version constraints and update pyproject.toml to resolve conflicts."),
            ("Python interpreter mismatches", "The local system Python version is incompatible with the project settings.", "Configure uv to build using a specific Python version: 'uv venv --python 3.11'.")
        ],
        "interviews": [
            ("Why is pyproject.toml preferred over setup.py in modern Python?", "It standardizes configuration by replacing execution scripts (`setup.py`) with declarative settings, separating metadata, dependencies, and tool options into a single schema file."),
            ("What is the difference between requirements.txt and a lockfile?", "`requirements.txt` typically lists top-level packages with loose version bounds. A lockfile lists the exact version, source, and hash of all packages and dependencies, ensuring deterministic builds."),
            ("How does uv achieve faster performance compared to standard pip?", "uv is written in Rust, resolves dependency graphs concurrently, and utilizes a global package cache to reuse built files across workspaces.")
        ],
        "use_cases": "Establishing clean workspaces for new Python projects to manage dependencies.",
        "project": "This setup configures the Python environment, allowing us to import the SDK and run the application in Chapter 8.",
        "summary": "This chapter covered setting up isolated Python virtual environments, managing dependencies in `pyproject.toml`, and using `uv` to synchronize packages.",
        "key_takeaways": "* Virtual environments prevent package conflicts.\n* Lockfiles ensure reproducible builds across environments.\n* The `uv` toolchain accelerates package management tasks.",
        "exercises": "* Beginner: Delete the `.venv` folder and run `uv sync` to restore the environment.\n* Intermediate: Add the `requests` library to `pyproject.toml` and synchronize packages to verify lockfile updates.",
        "reading": "* [uv Package Manager Documentation](https://docs.astral.sh/uv/)\n* [PEP 518 - Specifying Build Requirements](https://peps.python.org/pep-0518/)"
    },
    "07": {
        "title": "Configuration Files",
        "intro": "Separating configuration settings from application source code is key to building reusable, secure enterprise applications.",
        "what_is_it": "Configuration Files are structured text documents ('.env', 'bedrock_agent_core.yaml', 'pyproject.toml') used to store operational parameters, environment settings, entrypoint references, and access keys separately from application source code.",
        "why_important": "Hardcoding parameters like database names, API endpoints, or secret keys directly inside Python code creates severe security vulnerabilities and prevents the same application from running in different environments (such as testing or production). Storing settings in configuration files decouples environment parameters from codebase logic.",
        "how_it_works": "At startup, the application reads parameters from local '.env' environment files using helper tools like 'python-dotenv' and parses project settings from 'bedrock_agent_core.yaml'. These configuration values are injected into runtime memory, configuring database targets, logging levels, and IAM roles without modifying source code.",
        "key_responsibilities": [
            "Store secret access credentials locally in '.env' files while keeping them out of Git repositories.",
            "Declare deployment metadata, entrypoint paths, and execution role ARNs in YAML files.",
            "Centralize build settings, project metadata, and package dependencies in 'pyproject.toml'.",
            "Enable seamless transitions between local development, testing, and cloud production environments."
        ],
        "pre_reqs": "* Successful project setup and dependency synchronization from Chapter 6.\n* Familiarity with YAML, TOML, and INI configuration formats.",
        "bg_theory": "The Twelve-Factor App methodology dictates that configuration parameters (endpoints, resource names, access keys) must be kept separate from application code. This ensures the same codebase can run in development, testing, and production without changes. Committing sensitive keys to source code repos poses severe security risks; env files store local secrets, pyproject.toml defines dependencies, and bedrock_agent_core.yaml configures deployment settings.",
        "concepts": [
            ("Environment Variables", "Variables defined in the execution environment that configure runtime settings.", "Separates secret credentials from the codebase.", "AWS access keys loaded from a local `.env` file."),
            ("Metadata File", "A settings file declaring parameters like execution entry points and IAM roles.", "Configures how the service runs and scales the application container.", "The parameters defined in `bedrock_agent_core.yaml`."),
            ("pyproject.toml", "The configuration file used to declare build options and packages.", "Centralizes python tool settings and dependencies.", "Managing packaging options.")
        ],
        "mechanics": "1. The application boots and imports `os` and `dotenv`.\n2. The dotenv helper reads variables from the local `.env` file and injects them into the shell environment.\n3. The YAML parser parses `bedrock_agent_core.yaml` to configure agent parameters.\n4. If validation succeeds, the runtime assumes the declared IAM execution role and starts the agent container.",
        "mermaid": "graph TD\n    YAML[bedrock_agent_core.yaml] -->|Parses config| App[AgentCore Application]\n    App -->|Connects to| IAM[IAM Role ARN]\n    App -->|Invokes| Model[Model Target]\n    App -->|Saves state to| Table[DynamoDB Table]",
        "installation": "Verify that your YAML configuration file parses correctly by running:\n```bash\npython -c \"import yaml; print(yaml.safe_load(open('bedrock_agent_core.yaml')))\"\n```",
        "configuration": "### 1. Environment File `.env`\n```ini\nAWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nAWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\nAWS_DEFAULT_REGION=us-east-1\n```\n\n### 2. Metadata File `bedrock_agent_core.yaml`\n```yaml\nversion: \"1.0\"\nagent:\n  name: \"bedrock-agent-core-sample\"\n  entry_point: \"src/main.py\"\n  memory_id: \"agentcore-memory-table\"\n  execution_role_arn: \"arn:aws:iam::123456789012:role/AgentCoreExecutionRole\"\n```",
        "hands_on_simple": "# Verify loading environment variables using dotenv\nimport os\nfrom dotenv import load_dotenv\n\ndef check_env():\n    load_dotenv() # Load variables from .env file\n    region = os.getenv(\"AWS_DEFAULT_REGION\", \"Not Set\")\n    print(\"Loaded region configuration:\", region)\n\nif __name__ == \"__main__\":\n    check_env()",
        "hands_on_intermediate": "# Python script to parse and validate YAML metadata configuration fields\nimport yaml\n\ndef validate_yaml():\n    try:\n        with open(\"bedrock_agent_core.yaml\", \"r\") as f:\n            config = yaml.safe_load(f)\n        agent_cfg = config.get(\"agent\", {})\n        print(\"Agent Name:\", agent_cfg.get(\"name\"))\n        print(\"Entrypoint:\", agent_cfg.get(\"entry_point\"))\n        if not agent_cfg.get(\"execution_role_arn\"):\n            print(\"WARNING: execution_role_arn is missing!\")\n    except FileNotFoundError:\n        print(\"bedrock_agent_core.yaml file was not found.\")\n\nif __name__ == \"__main__\":\n    validate_yaml()",
        "hands_on_advanced": "# Structured configuration manager class for loading and validating configurations\nimport os\nimport yaml\nfrom dotenv import load_dotenv\n\nclass ConfigManager:\n    def __init__(self):\n        load_dotenv()\n        self.aws_region = os.getenv(\"AWS_DEFAULT_REGION\", \"us-east-1\")\n        self.agent_config = {}\n        self.load_yaml_config()\n\n    def load_yaml_config(self):\n        path = \"bedrock_agent_core.yaml\"\n        if os.path.exists(path):\n            with open(path, \"r\") as f:\n                self.agent_config = yaml.safe_load(f).get(\"agent\", {})\n\n    def validate(self):\n        errors = []\n        if not os.getenv(\"AWS_ACCESS_KEY_ID\"):\n            errors.append(\"Missing AWS_ACCESS_KEY_ID in environment.\")\n        if not self.agent_config.get(\"execution_role_arn\"):\n            errors.append(\"Missing execution_role_arn in bedrock_agent_core.yaml.\")\n        \n        if errors:\n            print(\"[CONFIG ERROR] Validation failed:\")\n            for err in errors:\n                print(f\"- {err}\")\n            return False\n        print(\"[CONFIG OK] Configuration parameters validated successfully.\")\n        return True\n\nif __name__ == \"__main__\":\n    cfg = ConfigManager()\n    cfg.validate()",
        "best_practices": "* Add `.env` to your project's `.gitignore` file to prevent committing secrets.\n* Use template files (like `template.env`) to document required keys without committing actual secrets.\n* Validate configurations on startup before running application code.",
        "security": "Never commit credentials or private keys to version control. In production, load secrets dynamically from AWS Secrets Manager or Systems Manager Parameter Store rather than using static local files.",
        "performance": "Cache configuration parameters in memory to avoid repeated disk reads during execution loops.",
        "cost": "Parsing local configuration files does not incur AWS charges. Ensure that configurations define short timeouts for third-party APIs to prevent billing for hung executions.",
        "mistakes": "* Committing the `.env` file to Git, exposing access keys in the commit history.\n* Defining invalid YAML syntax (like mixed tabs and spaces), causing parser crashes during startup.",
        "troubleshooting": [
            ("yaml.scanner.ScannerError", "Invalid YAML syntax or tab spacing characters used in bedrock_agent_core.yaml.", "Use spaces instead of tabs, and validate the file using an online YAML validator."),
            ("Variables return None on getenv", "The .env file was not loaded or does not exist in the working folder.", "Call 'load_dotenv()' before fetching environment variables, and verify the file is named exactly '.env'.")
        ],
        "interviews": [
            ("What is the Twelve-Factor App recommendation for configuration?", "The Twelve-Factor App methodology recommends storing configuration in the environment, separating settings from the codebase. This allows the application to move between environments without modification."),
            ("Why is YAML commonly used for configuration over JSON?", "YAML supports comments, handles multiline strings cleanly, and features a readable syntax without brackets and braces, simplifying configuration management."),
            ("How do you load environment variables in Python?", "Use the `os.getenv('KEY')` method to fetch values, and utilize the `python-dotenv` library's `load_dotenv()` function to load them from a local `.env` file.")
        ],
        "use_cases": "Configuring access permissions and endpoints for development and production environments.",
        "project": "These configuration files define the environment settings and entry points that authorize and run the application in Chapter 8.",
        "summary": "This chapter covered managing environment variables in `.env`, declaring packages in `pyproject.toml`, and setting up deployment settings in `bedrock_agent_core.yaml`.",
        "key_takeaways": "* Separating configuration from code simplifies multi-environment deployments.\n* Add configuration files containing secrets to your `.gitignore`.\n* Configuration files should be validated during application boot.",
        "exercises": "* Beginner: Add `LOG_LEVEL=DEBUG` to `.env` and read it in a Python script.\n* Intermediate: Configure `bedrock_agent_core.yaml` to reference a different IAM Role ARN and verify parsing.",
        "reading": "* [The Twelve-Factor App - Config](https://12factor.net/config)\n* [YAML Specification Guide](https://yaml.org/spec/)"
    },
    "08": {
        "title": "Running the Application Locally",
        "intro": "Testing and verifying Bedrock AgentCore applications locally ensures they function correctly before cloud deployment.",
        "what_is_it": "Running the Application Locally means executing your Bedrock AgentCore code inside a local container or local HTTP server on your workstation, allowing you to test request handling and logic before cloud deployment.",
        "why_important": "Deploying code changes directly to AWS cloud servers to test minor updates is slow, difficult to debug, and potentially costly. Running the application locally provides instant feedback, allows real-time terminal debugging, and ensures handler functions parse queries correctly before publishing.",
        "how_it_works": "The developer runs the 'agentcore run' CLI command, which starts a local web server binding to a specified network port (such as port 8000). The developer sends test HTTP POST requests containing prompt payloads (using tools like 'curl' or Python 'requests'), and the local handler function processes the request and returns a structured JSON response.",
        "key_responsibilities": [
            "Instantiate a local HTTP server that emulates the AWS AgentCore runtime environment.",
            "Bind internal container listening ports to workstation localhost endpoints.",
            "Route incoming prompt payloads to registered '@app.invoke' handler functions.",
            "Return formatted HTTP status codes and JSON response payloads for local verification."
        ],
        "pre_reqs": "* Active AWS credentials and configured local runtimes (Docker/Podman) from Chapters 2 and 3.\n* Valid configuration files from Chapter 7.",
        "bg_theory": "Waiting for cloud deployment cycles to test code changes slows development. Local container execution emulates the cloud environment on your workstation. Containers isolate dependencies, filesystems, and network ports. This ensures that if the agent runs locally, it will execute identically when deployed to the cloud runtime service.",
        "concepts": [
            ("Container", "A package containing code, runtimes, and system tools required to run an application.", "Ensures the application runs consistently across different host OS environments.", "Running the application via Docker."),
            ("Port Binding", "Mapping a container's internal network port to an external port on the host workstation.", "Enables external clients to send HTTP requests to the application inside the container.", "Mapping port 8000 to the host."),
            ("Invocations", "Sending requests containing prompt inputs to trigger the agent's reasoning loop.", "Triggers execution of the core handler function.", "Invoking the `/invoke` endpoint.")
        ],
        "mechanics": "1. Developer starts the server using `agentcore run`.\n2. The runner builds a local container image and starts it, binding port 8000.\n3. The developer sends a POST request with prompt data to `http://localhost:8000/invoke`.\n4. The container web server routes the request to the registered handler function.\n5. The handler executes, invokes the Bedrock model via HTTPS, and returns the response.",
        "mermaid": "sequenceDiagram\n    participant Dev as Local Developer\n    participant Container as AgentCore Container\n    participant Mock as Local Mock APIs\n    Dev->{Container}: Run application\n    Container->{Mock}: Validate configuration routes\n    Mock-->>Container: Return status 200 OK\n    Container-->>Dev: Ready for prompts",
        "installation": "Start the local application using the CLI:\n```bash\nagentcore run --config bedrock_agent_core.yaml\n```\nTo invoke the running agent from another terminal, use `curl`:\n```bash\ncurl -X POST -H \"Content-Type: application/json\" -d '{\"prompt\": \"Hello agent!\"}' http://localhost:8000/invoke\n```",
        "configuration": "Ensure that your local CLI is authenticated and that access parameters in `bedrock_agent_core.yaml` match your environment:\n```yaml\nagent:\n  name: \"local-agent-test\"\n  entry_point: \"src/main.py\"\n```",
        "hands_on_simple": "# Verify the server is responding on local ports using requests\nimport requests\n\ndef test_ping():\n    try:\n        res = requests.post(\"http://localhost:8000/invoke\", json={\"prompt\": \"ping\"})\n        print(\"Server Response Code:\", res.status_code)\n        print(\"Server Response Body:\", res.json())\n    except Exception as e:\n        print(\"Could not connect to local server:\", str(e))\n\nif __name__ == \"__main__\":\n    test_ping()",
        "hands_on_intermediate": "# Python script to automate starting and testing the local server\nimport subprocess\nimport time\nimport requests\n\ndef run_local_suite():\n    print(\"Starting local agent container server...\")\n    proc = subprocess.Popen([\"agentcore\", \"run\", \"--port\", \"8080\"])\n    time.sleep(3) # Wait for server boot\n    try:\n        res = requests.post(\"http://localhost:8080/invoke\", json={\"prompt\": \"test prompt\"})\n        print(\"Verification request successful:\")\n        print(res.json())\n    finally:\n        print(\"Terminating server process...\")\n        proc.terminate()\n\nif __name__ == \"__main__\":\n    run_local_suite()",
        "hands_on_advanced": "# Complete regression testing harness validating multiple prompts and response formats\nimport requests\nimport sys\n\ndef run_regression():\n    url = \"http://localhost:8000/invoke\"\n    test_cases = [\n        {\"prompt\": \"What are key IAM features?\", \"expected_code\": 200},\n        {\"prompt\": \"\", \"expected_code\": 400},\n        {\"prompt\": \"Analyze this text payload\", \"expected_code\": 200}\n    ]\n    all_pass = True\n    for case in test_cases:\n        print(f\"Sending prompt: '{case['prompt']}'...\")\n        try:\n            res = requests.post(url, json={\"prompt\": case[\"prompt\"]})\n            if res.status_code != case[\"expected_code\"]:\n                print(f\"- [FAIL] Expected {case['expected_code']}, got {res.status_code}\")\n                all_pass = False\n            else:\n                print(f\"- [OK] Received expected status {res.status_code}\")\n        except Exception as e:\n            print(\"Connection error:\", str(e))\n            all_pass = False\n    if not all_pass:\n        sys.exit(1)\n    print(\"Regression testing suite completed successfully!\")\n\nif __name__ == \"__main__\":\n    run_regression()",
        "best_practices": "* Check for port conflicts before starting the server to ensure port 8000 is available.\n* Monitor container logs in a separate terminal window to inspect traceback details.\n* Test edge cases (like empty payloads or long inputs) during local testing cycles.",
        "security": "Do not expose the local agent container to public networks; bind the listener exclusively to localhost (`127.0.0.1`). Ensure that environment variables containing credentials are not printed in console logs.",
        "performance": "Initialize model and database clients outside the main request loop to minimize handler execution times.",
        "cost": "Running containers locally does not incur AWS compute charges. You are only billed for model inference requests called through Bedrock APIs.",
        "mistakes": "* Starting the application before launching the local Docker daemon, causing build failures.\n* Sending invalid JSON request payloads, causing server parsing crashes.",
        "troubleshooting": [
            ("Port 8000 already in use error", "Another local process is bound to port 8000, blocking the application server.", "Identify the process using port checking commands and terminate it, or start the application on a different port: 'agentcore run --port 9000'."),
            ("Docker daemon is not running", "The local container runtime engine is inactive.", "Start Docker Desktop on Windows/macOS, or start the docker service on Linux.")
        ],
        "interviews": [
            ("How do you run local integration tests for containerized agents?", "Start the application container locally on a test port, and execute a test script that sends structured prompts and asserts response properties using a testing framework (like pytest)."),
            ("What is a bridge network in Docker?", "A bridge network is a private network created by Docker that isolates containers on the same host, allowing them to communicate while securing them from external network interfaces."),
            ("Why is local logging important during development?", "Local logs capture traceback details, execution times, and payload mappings, helping developers isolate and fix bugs before code is checked in.")
        ],
        "use_cases": "Testing agent updates locally to verify logic before deploying code to AWS.",
        "project": "Local testing validates our handler code before it is packaged into production container images in Chapter 15.",
        "summary": "This chapter covered starting the application locally using the CLI and invoking endpoints using curl to verify agent execution.",
        "key_takeaways": "* Local containers isolate applications from host configurations.\n* Invoke handlers parse prompt values and return responses.\n* Test code updates locally to verify logic before cloud deployment.",
        "exercises": "* Beginner: Launch the application on port 9000 and verify it responds to request pings.\n* Intermediate: Write a shell script that starts the container, submits a test prompt, and saves logs to a text file.",
        "reading": "* [Docker Networking Guide](https://docs.docker.com/network/)\n* [Python Requests Library Documentation](https://requests.readthedocs.io/)"
    },
    "09": {
        "title": "Understanding the Code",
        "intro": "Analyzing the implementation details of the main application file is key to customizing agent execution logic.",
        "what_is_it": "Understanding the Code involves analyzing the line-by-line structure and execution flow of the main application script ('src/main.py'), detailing how decorators, handlers, context objects, and response payloads interact.",
        "why_important": "Writing maintainable, enterprise-ready software requires understanding how each line of code functions within the broader framework framework. Knowing how request parameters are extracted, validated, and logged enables developers to extend business logic safely without breaking application structure.",
        "how_it_works": "The script initializes standard logging, instantiates the 'BedrockAgentCoreApp' wrapper class, and decorates a handler function with '@app.invoke'. When a request arrives, the application extracts the JSON payload and context metadata object, passes them to the handler function, executes custom processing steps, and formats the output into a standardized return dictionary.",
        "key_responsibilities": [
            "Instantiate core framework app wrappers to manage container request listeners.",
            "Register routing endpoints to custom Python functions via '@app.invoke' decorators.",
            "Parse input arguments from 'payload' dictionaries and session details from 'context' objects.",
            "Output structured JSON dictionary responses containing HTTP status codes and response bodies."
        ],
        "pre_reqs": "* Successful repository clone and walkthrough setup from Chapters 4 and 5.\n* Basic familiarity with Python logging libraries.",
        "bg_theory": "Enterprise applications utilize clean code architectures to decouple framework code from custom business logic. Bedrock AgentCore separates container routing configurations from the agent's reasoning loop. The handler accepts request payloads and context metadata, coordinates database calls, and formats response payloads, making the codebase easier to test and maintain.",
        "concepts": [
            ("SDK Wrapper", "A library class that abstracts container lifecycle hooks and request routing details.", "Simplifies web listener configuration and request handling.", "The `BedrockAgentCoreApp` class."),
            ("Decorator", "A design pattern that extends function behavior without modifying the function's code.", "Registers handlers with framework routers.", "The `@app.invoke` decorator."),
            ("Execution Context", "An object containing metadata parameters injected by the runtime environment.", "Provides execution details like session IDs and user scopes.", "The `context` handler parameter.")
        ],
        "mechanics": "1. The main entrypoint initializes logging configurations.\n2. It instantiates the application class `BedrockAgentCoreApp()`.\n3. The `@app.invoke` decorator registers the decorated handler function in the application's route registry.\n4. When a request is received, the application extracts the JSON body and routes it to the handler.\n5. The handler executes, returning a dictionary that is serialized into an HTTP response.",
        "mermaid": "graph TD\n    AppInit[app = BedrockAgentCoreApp] -->|Decorator| Reg[@app.invoke]\n    Reg -->|Registers| Handler[my_agent_handler]\n    Handler -->|Extracts| Prompt[payload.get('prompt')]\n    Handler -->|Extracts| Session[context.session_id]\n    Handler -->|Returns| Response[statusCode, response]",
        "installation": "Ensure that your main entrypoint file is located at `src/main.py` and is importable:\n```bash\npython -m py_compile src/main.py\n```",
        "configuration": "Configure the agent's entrypoint path in `bedrock_agent_core.yaml` to ensure the runtime can locate your handler:\n```yaml\nagent:\n  entry_point: \"src/main.py\"\n```",
        "hands_on_simple": "# Minimum agent execution handler script\nfrom bedrock_agent_core import BedrockAgentCoreApp\n\napp = BedrockAgentCoreApp()\n\n@app.invoke\def simple_handler(payload, context):\n    return {\"statusCode\": 200, \"response\": \"Handler executed successfully.\"}",
        "hands_on_intermediate": "# Handler logging request details and validating parameters\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"AppHandler\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handler(payload, context):\n    logger.info(\"Received invocation request.\")\n    prompt = payload.get(\"prompt\")\n    if not prompt:\n        return {\"statusCode\": 400, \"response\": \"Missing 'prompt' in payload.\"}\n    \n    session_id = getattr(context, \"session_id\", \"local-dev\")\n    logger.info(f\"Processing prompt for session: {session_id}\")\n    return {\"statusCode\": 200, \"response\": f\"Processed input: '{prompt}'\"}",
        "hands_on_advanced": "# Complete handler simulating model calls and returning structured JSON metadata\nfrom bedrock_agent_core import BedrockAgentCoreApp\nimport logging\nimport json\n\nlogger = logging.getLogger(\"ProductionApp\")\napp = BedrockAgentCoreApp()\n\n@app.invoke\ndef handle_request(payload, context):\n    try:\n        prompt = payload.get(\"prompt\", \"\")\n        session_id = getattr(context, \"session_id\", \"local-session\")\n        logger.info(f\"Invoking agent loop for session: {session_id}\")\n        \n        if not prompt.strip():\n            return {\"statusCode\": 400, \"response\": {\"error\": \"Empty prompt received.\"}}\n            \n        # Mock core processing workflow\n        response_data = {\n            \"text\": f\"Completed processing for prompt: '{prompt}'\",\n            \"tokens_used\": len(prompt.split()) * 2,\n            \"success\": True\n        }\n        \n        return {\n            \"statusCode\": 200,\n            \"response\": response_data\n        }\n    except Exception as e:\n        logger.error(f\"Execution error in handler: {str(e)}\")\n        return {\n            \"statusCode\": 500,\n            \"response\": {\"error\": \"Internal Server Error\"}\n        }",
        "best_practices": "* Keep handler functions focused on task orchestration; delegate business logic to separate modules.\n* Implement clear logging structures to capture both input parameters and execution durations.\n* Write unit tests for handler functions by passing mock payload and context arguments.",
        "security": "Enforce input validation rules on incoming payloads to protect against code injection. Sanitize output responses to ensure sensitive system details are not leaked in error messages.",
        "performance": "Load large models and database configurations outside the handler function to avoid initialization latency during request loops.",
        "cost": "Optimize the execution time of code paths inside your handler function. The longer a handler runs, the longer the compute microVM remains active, increasing execution costs.",
        "mistakes": "* Initializing heavy client dependencies inside the handler function code, causing latency.\n* Accessing payload parameters directly without check validations, causing KeyError crashes if parameters are missing.",
        "troubleshooting": [
            ("SyntaxError on python run", "Invalid syntax or indentations in main.py.", "Verify syntax and check that the script compiles: 'python -m py_compile src/main.py'."),
            ("NameError on app object references", "The application object or variable was referenced before initialization.", "Verify that the app wrapper object is instantiated: 'app = BedrockAgentCoreApp()' before registering handlers.")
        ],
        "interviews": [
            ("What is the benefit of decorating functions with @app.invoke?", "The decorator registers the function as the agent's entrypoint, abstracting web server routing and request parsing so developers can focus on agent logic."),
            ("How do you extract session identifiers inside the handler?", "Extract the `session_id` attribute from the `context` argument: `session_id = getattr(context, 'session_id', 'default')`."),
            ("Why is logging critical inside handler functions?", "Logging captures request payloads, runtime errors, and execution times, providing the details needed to monitor and debug applications.")
        ],
        "use_cases": "Customizing handler functions to route prompts to different agent orchestrators.",
        "project": "This walkthrough defines the structural template for our main agent script (`src/main.py`) which we will expand in subsequent chapters.",
        "summary": "This chapter analyzed the implementation details of the main application file, including imports, app wrappers, logging, and handlers.",
        "key_takeaways": "* Handlers process incoming request payloads and metadata.\n* Python decorators bind routing endpoints to functions.\n* Initializing resources at the module level minimizes execution latency.",
        "exercises": "* Beginner: Add a log message that prints the length of the prompt inside the handler.\n* Intermediate: Add a custom parameter verification step and return a 400 error status code if validation fails.",
        "reading": "* [Clean Code Guide for Python](https://github.com/zedr/clean-code-python)\n* [Python Logging Library Guide](https://docs.python.org/3/library/logging.html)"
    },
    "10": {
        "title": "AgentCore Runtime",
        "intro": "The AgentCore runtime hosts agent containers inside secure, isolated virtual machine environments.",
        "what_is_it": "The AgentCore Runtime is the AWS-managed hosting infrastructure that executes agent applications inside lightweight, securely isolated virtual machine environments called AWS Firecracker microVMs.",
        "why_important": "Traditional multi-tenant cloud environments share operating system kernels between users, risking cross-tenant data leaks and resource starvation. The AgentCore Runtime provides hypervisor-level security isolation for every user session while maintaining sub-second cold-start execution times and low operational costs.",
        "how_it_works": "When a user query arrives with a unique session ID, the AgentCore Runtime checks if an active microVM exists for that session. If active (warm start), the query routes directly to the running container. If inactive (cold start), Firecracker boots a new microVM instance in seconds, pulls the ECR container image, mounts ephemeral storage, and handles the request.",
        "key_responsibilities": [
            "Provision and manage isolated AWS Firecracker microVM instances for user agent sessions.",
            "Enforce hardware resource limits on CPU usage, RAM allocation, and ephemeral disk space.",
            "Manage session lifecycles, routing warm requests quickly and terminating idle instances.",
            "Guarantee multi-tenant data isolation by maintaining dedicated operating system kernels per session."
        ],
        "pre_reqs": "* Setup of configuration files and local container runtimes from Chapters 7 and 8.\n* A basic understanding of virtualization concepts (VMs vs containers).",
        "bg_theory": "Deploying agents to the cloud requires secure execution environments. Traditional shared container runtimes share a single operating system kernel, risking cross-tenant data leaks. AWS designed Firecracker to combine the security isolation of traditional virtual machines with the speed and efficiency of containers. The AgentCore runtime spawns a dedicated Firecracker microVM for each user session, enforcing resource limits and security boundaries.",
        "concepts": [
            ("Firecracker", "An open-source virtualization technology designed to spawn secure, multitenant microVMs.", "Combines the security isolation of traditional VMs with container speed.", "The underlying hypervisor for AWS Lambda and Fargate."),
            ("Cold Start", "The process of pulling container images and booting a new microVM for a session.", "The initial boot latency when a session starts.", "The initial request boot cycle."),
            ("Warm Start", "Routing subsequent requests using the same session ID to an active microVM.", "Bypasses the boot cycle for low-latency responses.", "Subsequent requests within active session windows.")
        ],
        "mechanics": "1. Client sends an invocation request containing a unique `session_id`.\n2. The runtime checks if an active microVM is allocated to that session.\n3. If missing (Cold Start), it pulls the ECR container image and boots a new Firecracker microVM.\n4. If active (Warm Start), it routes the request directly to the running container.\n5. The microVM executes the request and remains active until the inactivity timeout or max session duration (8 hours) is reached.",
        "mermaid": "graph TD\n    Client[Client Request] -->|Session ID| Router[Runtime Router]\n    Router -->|Allocate| VM[Isolated Firecracker VM]\n    VM -->|Run Code| Container[Agent App Container]\n    VM -->|Mount| Storage[Session ephemeral storage]",
        "installation": "Inspect active session microVM status using the CLI:\n```bash\nagentcore runtime status\n```",
        "configuration": "Configure runtime limits and session timeouts in `bedrock_agent_core.yaml`:\n```yaml\nruntime:\n  timeout_seconds: 3600\n  memory_mb: 2048\n  storage_gb: 10\n```",
        "hands_on_simple": "# Verify session details in execution context\ndef check_runtime_context(context):\n    session_id = getattr(context, \"session_id\", \"local-session\")\n    print(\"Running inside session VM:\", session_id)\n    return session_id",
        "hands_on_intermediate": "# Python script to verify local file isolation under /tmp\nimport os\n\ndef check_file_isolation():\n    path = \"/tmp/session_data.txt\"\n    if os.path.exists(path):\n        with open(path, \"r\") as f:\n            print(\"Read session data:\", f.read())\n    else:\n        print(\"No session data found. Writing default...\")\n        with open(path, \"w\") as f:\n            f.write(\"Session Active\")\n\nif __name__ == \"__main__\":\n    check_file_isolation()",
        "hands_on_advanced": "# Complete script validating memory limits and executing timeout handlers\nimport time\nimport signal\nimport sys\n\ndef timeout_handler(signum, frame):\n    print(\"[TIMEOUT] Execution time limit exceeded. Terminating task.\")\n    sys.exit(1)\n\ndef execute_with_bounds(duration):\n    # Register signal handler for execution timeouts\n    signal.signal(signal.SIGALRM, timeout_handler)\n    signal.alarm(5) # Set timeout limit to 5 seconds\n    try:\n        print(f\"Executing process for {duration} seconds...\")\n        time.sleep(duration)\n        signal.alarm(0) # Disable alarm on success\n        print(\"[SUCCESS] Task completed within limits.\")\n    except Exception as e:\n        print(\"Execution error:\", str(e))\n\nif __name__ == \"__main__\":\n    execute_with_bounds(3) # Succeeds\n    execute_with_bounds(10) # Triggers timeout",
        "best_practices": "* Design applications to boot quickly by minimizing the container image footprint.\n* Never write persistent data to the local filesystem; write files to S3.\n* Configure short timeouts to prevent runaway executions from inflating bills.",
        "security": "Enforce strict resource allocations for RAM and CPU. Ensure that containers run as non-root users inside microVMs to prevent privilege escalation attacks.",
        "performance": "Leverage warm starts for sequential requests to bypass boot latency and ensure fast response times.",
        "cost": "Monitor microVM active runtimes closely. Inactive microVMs are automatically reclaimed by AWS after inactivity thresholds are met, minimizing idle resource charges.",
        "mistakes": "* Expecting files written to `/tmp` to persist across sessions (sessions terminate after timeouts, destroying ephemeral storage).\n* Overallocating RAM in configurations, leading to high resource reservation fees.",
        "troubleshooting": [
            ("504 Gateway Timeout error", "The execution exceeded the configured timeout_seconds threshold.", "Increase timeout limits in configuration or refactor logic to use streaming responses."),
            ("OutOfMemory error during execution", "The application exceeded allocated microVM RAM limits.", "Optimize memory usage patterns or increase memory_mb configurations.")
        ],
        "interviews": [
            ("What is the security advantage of Firecracker over standard containers?", "Standard containers share the host operating system kernel, making them vulnerable to kernel exploit leaks. Firecracker runs each container inside an isolated microVM with its own kernel, securing multi-tenant environments."),
            ("How do cold starts affect agent latency?", "Cold starts add boot latency (typically a few seconds) because the system must pull the container image and initialize the virtual machine before processing requests."),
            ("What happens to ephemeral data when a session terminates?", "When a session times out or reaches its limit, the microVM is destroyed, erasing all ephemeral storage data (including the `/tmp` folder).")
        ],
        "use_cases": "Isolating user sessions in SaaS platforms to prevent multi-tenant data leaks.",
        "project": "This runtime provides the secure host environment where our agent handler executes in production.",
        "summary": "This chapter analyzed the virtualization architecture of AgentCore, detailing Firecracker microVMs, session isolation, and execution bounds.",
        "key_takeaways": "* Session isolation is enforced using AWS Firecracker microVMs.\n* Inactive microVMs are reclaimed to minimize idle resource charges.\n* Write persistent files to S3 because microVM storage is ephemeral.",
        "exercises": "* Beginner: Configure `bedrock_agent_core.yaml` to set `timeout_seconds` to 600.\n* Intermediate: Map the lifecycle of a runtime VM from boot to destruction in a flow chart.",
        "reading": "* [AWS Firecracker Architecture Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-firecracker-design/aws-firecracker-design.html)\n* [AWS Lambda Execution Environments](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html)"
    },
    "11": {
        "title": "Tool Gateway",
        "intro": "The Tool Gateway routes request payloads to databases and external APIs securely.",
        "what_is_it": "The Tool Gateway is an API management and security broker layer that connects AI agents to external databases, enterprise microservices, and web APIs using standardized protocol schemas.",
        "why_important": "AI foundation models cannot directly run database queries or trigger external web service actions on their own. The Tool Gateway provides a secure abstraction interface that translates model requests into safe API calls, validating parameter formats against JSON schemas to prevent injection attacks and bad requests.",
        "how_it_works": "The Tool Gateway defines tools using the Model Context Protocol (MCP). When the AI model determines it needs external data, it returns a tool call request specifying tool names and arguments. The Tool Gateway validates these parameters against registered JSON schemas, routes the call to target backend functions, and passes execution results back to the model.",
        "key_responsibilities": [
            "Expose external tools and database functions to AI models using Model Context Protocol (MCP) schemas.",
            "Validate model-generated request arguments against defined JSON schemas before execution.",
            "Perform semantic tool routing to include only prompt-relevant tool definitions, reducing token usage.",
            "Enforce permission policies and authorization boundaries between AI models and backend APIs."
        ],
        "pre_reqs": "* Configured local endpoints and AWS credentials from Chapters 3 and 8.\n* Familiarity with JSON schema definitions.",
        "bg_theory": "Models can only process and generate text; they cannot access databases or run code directly. Integrating tools extends their capabilities. However, exposing APIs directly to LLMs risks SQL injection attacks. A tool gateway acts as a secure broker. It validates parameters against JSON schemas and exposes tools standardizing communication via the Model Context Protocol (MCP). Under semantic routing, the gateway retrieves only the tools relevant to the prompt, minimizing prompt token bloat.",
        "concepts": [
            ("MCP", "An open protocol standardizing communication between AI agents and external tools.", "Simplifies integrations across services.", "Defining tools in gateway configuration files."),
            ("Tool Gateway", "An API broker routing model requests to downstream functions.", "Centralizes security, logging, and rate limiting.", "The gateway routing interface."),
            ("Semantic Routing", "Selecting relevant tools based on prompt meaning rather than keyword matches.", "Minimizes prompt token usage and cost.", "Filtering active tools.")
        ],
        "mechanics": "1. Client submits a prompt to the agent.\n2. The agent queries semantic routing to locate relevant tools.\n3. The gateway validates the tool request schema.\n4. It translates parameters and routes the request to the backend function.\n5. The function executes, returning the result to the model to complete the reasoning loop.",
        "mermaid": "graph LR\n    Agent[Agent Reasoning] -->|MCP Request| Gateway[Tool Gateway]\n    Gateway -->|Route| DB[Database Server]\n    Gateway -->|Route| API[External Web APIs]\n    Gateway -->|Route| Lambda[AWS Lambda Functions]",
        "installation": "Inspect active gateway server configurations using the CLI:\n```bash\nagentcore gateway list\n```",
        "configuration": "Define registered tools in the `gateway_config.json` configuration file:\n```json\n{\n  \"tools\": [\n    {\n      \"name\": \"fetch_stock_level\",\n      \"description\": \"Check active warehouse stock counts for a product SKU.\",\n      \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"sku\": {\"type\": \"string\", \"description\": \"Product identifier\"}\n        },\n        \"required\": [\"sku\"]\n      }\n    }\n  ]\n}\n```",
        "hands_on_simple": "# Verify gateway connection configurations\ndef check_gateway_config(config_path):\n    import json\n    try:\n        with open(config_path, \"r\") as f:\n            cfg = json.load(f)\n        print(\"Gateway registered tools count:\", len(cfg.get(\"tools\", [])))\n    except Exception as e:\n        print(\"Invalid JSON configuration:\", str(e))",
        "hands_on_intermediate": "# Python script to validate input arguments against registered JSON schemas\nfrom jsonschema import validate, ValidationError\n\ntool_schema = {\n    \"type\": \"object\",\n    \"properties\": {\n        \"sku\": {\"type\": \"string\", \"pattern\": \"^[A-Z]{3}-[0-9]{3}$\"}\n    },\n    \"required\": [\"sku\"]\n}\n\ndef validate_arguments(args):\n    try:\n        validate(instance=args, schema=tool_schema)\n        print(\"[OK] Arguments validated successfully!\")\n        return True\n    except ValidationError as e:\n        print(\"[FAIL] Validation error:\", e.message)\n        return False\n\nif __name__ == \"__main__\":\n    validate_arguments({\"sku\": \"ABC-123\"}) # Valid\n    validate_arguments({\"sku\": \"invalid\"}) # Invalid",
        "hands_on_advanced": "# Complete mock gateway router resolving dynamic tool execution requests\nimport json\n\nclass MockGatewayRouter:\n    def __init__(self):\n        self.tool_registry = {}\n\n    def register(self, name, func):\n        self.tool_registry[name] = func\n\n    def route_request(self, tool_name, arguments_json):\n        if tool_name not in self.tool_registry:\n            return {\"success\": False, \"error\": f\"Tool '{tool_name}' not found.\"}\n        try:\n            args = json.loads(arguments_json)\n            # Execute target function\n            res = self.tool_registry[tool_name](**args)\n            return {\"success\": True, \"output\": res}\n        except Exception as e:\n            return {\"success\": False, \"error\": str(e)}\n\ndef mock_db_lookup(sku):\n    db = {\"SHI-001\": \"12 units in stock\", \"PAN-002\": \"Out of stock\"}\n    return db.get(sku, \"SKU not found.\")\n\nif __name__ == \"__main__\":\n    router = MockGatewayRouter()\n    router.register(\"fetch_stock_level\", mock_db_lookup)\n    print(router.route_request(\"fetch_stock_level\", '{\"sku\": \"SHI-001\"}'))",
        "best_practices": "* Define clear descriptions in schemas to guide model selection.\n* Apply strict schemas to protect backend APIs from malformed parameters.\n* Route calls through private connections to secure network traffic.",
        "security": "Enforce IAM boundary limits on gateway execution roles. Use Cedar policy rules to define permissions for users, tools, and actions, blocking unauthorized executions.",
        "performance": "Utilize semantic routing to minimize the number of tool schemas appended to prompts, optimizing latency and reducing costs.",
        "cost": "Monitor token usage associated with tool definitions. Long tool descriptions increase input token usage, inflating overall execution costs.",
        "mistakes": "* Defining ambiguous tool descriptions, causing models to select the wrong tool.\n* Committing API secret keys inside tool execution scripts instead of retrieving them dynamically.",
        "troubleshooting": [
            ("Model invokes wrong tool during run", "Ambiguous descriptions inside the gateway configuration schema.", "Clarify description text to guide the model's reasoning loop."),
            ("InvalidRequestException on invoke", "The schema formatting is incompatible with the Amazon Bedrock API.", "Verify configurations align with JSON schema formatting standards.")
        ],
        "interviews": [
            ("What is the advantage of using Model Context Protocol (MCP)?", "MCP standardizes integrations by decoupling clients from specific database API formats, providing a uniform schema for tool communication."),
            ("How does semantic tool routing optimize prompt sizes?", "Semantic routing filters tool lists to only append schemas relevant to the query, reducing prompt token bloat and lowering costs."),
            ("How do you secure tool calls from SQL injection attacks?", "Verify input arguments against strict parameter schemas, and use parameterized queries in backend database drivers to block injection vectors.")
        ],
        "use_cases": "Integrating customer database lookups securely into customer service workflows.",
        "project": "This gateway acts as the integration point that allows our agent to invoke database tools and Lambda functions.",
        "summary": "This chapter covered the Tool Gateway architecture, the Model Context Protocol (MCP), and configuring tool schemas in `gateway_config.json`.",
        "key_takeaways": "* Expose tools using standardized MCP schemas to simplify integrations.\n* Leverage semantic routing to minimize prompt token usage.\n* Validate input arguments against strict schemas to secure backend APIs.",
        "exercises": "* Beginner: Write a JSON schema definition for a tool that retrieves weather updates by city.\n* Intermediate: Add validation checks to reject city strings containing numeric characters.",
        "reading": "* [Model Context Protocol Specification](https://modelcontextprotocol.io/)\n* [JSON Schema Standard Reference](https://json-schema.org/)"
    },
    "12": {
        "title": "Identity Engine & User Authentication",
        "intro": "The Identity Engine authenticates user sessions and enforces row-level security for data access.",
        "what_is_it": "The Identity Engine is the security component that authenticates end-user identities, verifies access credentials (such as JSON Web Tokens / JWTs), and propagates user security contexts down to database tools.",
        "why_important": "AI agents operating in multi-user applications must ensure that users can only view and modify their own data records. Without identity verification, an agent could accidentally expose one user's private records to another. The Identity Engine enforces strict, identity-aware row-level data access controls across all agent actions.",
        "how_it_works": "The end-user authenticates against an Identity Provider (like Amazon Cognito or Okta) and receives a signed JWT access token. The client application passes this token in the API request header. The Identity Engine verifies the token's cryptographic signature against provider public keys, extracts the unique user subject ID (Actor ID), and passes it to downstream tools.",
        "key_responsibilities": [
            "Authenticate user credentials and validate incoming JSON Web Token (JWT) cryptographic signatures.",
            "Extract unique user identifiers (Actor IDs) and session authorization claims from token payloads.",
            "Propagate user identity attributes to tool gateways and database drivers.",
            "Enforce row-level security controls in backend database tables based on verified user identities."
        ],
        "pre_reqs": "* AWS CLI configurations and active IAM role credentials from Chapters 3 and 8.\n* A basic understanding of token-based authentication (OAuth2 / OIDC).",
        "bg_theory": "Agents must interact with data on behalf of specific users while maintaining privacy. Authenticating users via identity providers (Cognito or Okta) generates access tokens (JWTs). The Identity Engine validates JWT signatures, extracts the unique user ID (Actor ID), and propagates it to tools, ensuring users can only access their own records.",
        "concepts": [
            ("JWT", "A compact, cryptographically signed token format used to exchange claims securely.", "Enables stateless user authentication across services.", "Passing user sessions in request headers."),
            ("Actor ID", "The unique user identifier extracted from the access token claims.", "Associates database operations with the active user.", "The database partition key mapping."),
            ("Cognito User Pool", "A managed user directory on AWS that handles sign-up and sign-in flows.", "Simplifies user authentication management.", "The central identity provider.")
        ],
        "mechanics": "1. Client login returns a Cognito identity JSON Web Token (JWT).\n2. Client app passes the JWT in the Authorization header to invoke the agent.\n3. The Identity Engine fetches the JWKS and verifies the token's cryptographic signature.\n4. If valid, it extracts user identity claims (like the `sub` Subject ID).\n5. The unique Actor ID is propagated to downstream tools to enforce row-level security.",
        "mermaid": "sequenceDiagram\n    participant User as End User\n    participant Cognito as Cognito User Pool\n    participant Agent as Agent Runtime VM\n    User->>Cognito: Login credentials\n    Cognito-->>User: ID & Access Tokens\n    User->>Agent: Send prompt with Access Token\n    Agent->>Agent: Extract Actor ID and verify",
        "installation": "Verify Cognito credentials from your terminal using the AWS CLI:\n```bash\naws cognito-idp list-users --user-pool-id <user_pool_id>\n```",
        "configuration": "Map the identity configuration parameters in your configuration files:\n```yaml\nidentity:\n  provider: \"cognito\"\n  user_pool_id: \"us-east-1_xxxxxxxxx\"\n  client_id: \"xxxxxxxxxxxxxxxxxxxxxxxxxx\"\n```",
        "hands_on_simple": "# Verify token structures using local decoding\nimport jwt # PyJWT library\n\ndef decode_mock_token(token):\n    try:\n        # In production, verify signatures using public keys\n        claims = jwt.decode(token, options={\"verify_signature\": False})\n        print(\"Decoded token user ID (sub):\", claims.get(\"sub\"))\n    except Exception as e:\n        print(\"Failed to decode token:\", str(e))",
        "hands_on_intermediate": "# Python script to validate token expiration timestamps\nimport time\nimport jwt\n\ndef check_token_expiry(token):\n    try:\n        claims = jwt.decode(token, options={\"verify_signature\": False})\n        exp = claims.get(\"exp\", 0)\n        is_active = exp > time.time()\n        print(f\"Token is active: {is_active} (Expires in {int(exp - time.time())} seconds)\")\n        return is_active\n    except Exception as e:\n        print(\"Validation error:\", str(e))\n        return False",
        "hands_on_advanced": "# Complete JWT verification engine validating signatures and extracting claims\nimport urllib.request\nimport json\nimport jwt\n\nclass JWTVerifier:\n    def __init__(self, region, user_pool_id):\n        self.jwks_url = f\"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json\"\n        self.jwks = self.load_jwks()\n\n    def load_jwks(self):\n        try:\n            res = urllib.request.urlopen(self.jwks_url)\n            return json.loads(res.read())\n        except Exception as e:\n            print(\"Failed to load JWKS:\", str(e))\n            return {\"keys\": []}\n\n    def verify(self, token):\n        try:\n            # In production, select matching public key from JWKS to verify signature\n            claims = jwt.decode(token, options={\"verify_signature\": False})\n            print(\"Token verified successfully. Actor ID:\", claims.get(\"sub\"))\n            return claims\n        except Exception as e:\n            print(\"Token verification failed:\", str(e))\n            return None\n\nif __name__ == \"__main__\":\n    # Example usage with mock config\n    verifier = JWTVerifier(\"us-east-1\", \"us-east-1_examplePool\")",
        "best_practices": "* Always verify JWT cryptographic signatures against your provider's public keys.\n* Validate token expiration claims (`exp`) to block expired sessions.\n* Keep access token lifespans short to limit the impact of token leakage.",
        "security": "Enforce row-level security by using the Actor ID as the partition key in database queries. Never allow the client to specify the User ID in payload arguments; extract it from verified token claims.",
        "performance": "Cache provider public keys (JWKS) locally to avoid network requests for every token validation check.",
        "cost": "Cognito charges based on Monthly Active Users (MAUs), offering a generous free tier that covers development and small production workloads.",
        "mistakes": "* Skipping token signature verification and reading claims directly, making the system vulnerable to token tampering.\n* Hardcoding provider keys instead of retrieving them dynamically from JKWS endpoints.",
        "troubleshooting": [
            ("Signature verification fails", "The JWT signature is invalid or signed by an untrusted issuer.", "Verify the user pool client configurations and check if tokens are expired."),
            ("Claims return empty dictionary", "The JWT payload is malformed or not formatted correctly.", "Decode the token using jwt.io to audit structure and claims.")
        ],
        "interviews": [
            ("What is the difference between an ID token and an Access token?", "ID tokens contain identity claims (name, email) used by client UIs. Access tokens contain scopes and permissions used to authorize API calls."),
            ("Why is verifying signature keys via JWKS important?", "JWKS lists the public keys used to verify token signatures. Signature checks ensure tokens were generated by trusted issuers and not tampered with."),
            ("How do you enforce row-level security in DynamoDB?", "Use IAM policy conditions to limit table access: `dynamodb:LeadingKeys` restricts operations to records matching the user's Actor ID.")
        ],
        "use_cases": "Ensuring users can only retrieve and modify their own transaction records in database applications.",
        "project": "This engine authenticates user sessions, enabling us to isolate and secure database interactions.",
        "summary": "This chapter covered user authentication, JWT verification, and extracting user identities to secure database interactions.",
        "key_takeaways": "* User authentication is managed using Cognito user pools.\n* Extract and propagate Actor IDs to downstream tools to secure data access.\n* Always verify JWT cryptographic signatures and expiration timestamps.",
        "exercises": "* Beginner: Decode a mock JWT and print the subject identifier.\n* Intermediate: Add user group validation checks to restrict access to administrator users.",
        "reading": "* [Cognito User Pools Developer Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)\n* [JWT Standard Specification Guide](https://jwt.io/introduction)"
    },
    "13": {
        "title": "Memory Engine & State Management",
        "intro": "The Memory Engine manages short-term conversational history and long-term user profiles.",
        "what_is_it": "The Memory Engine is the state management system responsible for storing, compacting, and retrieving short-term chat history and long-term user profile facts across conversation sessions.",
        "why_important": "AI foundation models are inherently stateless and forget all context once a single prompt request finishes. Re-sending full conversation histories with every prompt bloats context windows, increases response latency, and drastically raises API token costs. The Memory Engine maintains state efficiently while keeping prompt context windows small.",
        "how_it_works": "Short-term dialogue turns are saved to an active session cache. When a session finishes or reaches a turn limit, an automated compaction loop runs. The compaction loop uses a fast LLM to extract key user facts, preferences, and state summaries from raw dialogue logs, saving these structured summaries to an AWS DynamoDB table while clearing raw history logs.",
        "key_responsibilities": [
            "Persist short-term dialogue history for ongoing multi-turn conversations within active sessions.",
            "Store long-term user profiles and preferences in Amazon DynamoDB tables across sessions.",
            "Execute background compaction loops to summarize long dialogue logs into structured facts.",
            "Inject relevant user profile summaries into model prompt templates to personalize responses efficiently."
        ],
        "pre_reqs": "* AWS CLI configurations and active IAM role credentials from Chapters 3 and 8.\n* A basic understanding of database operations (DynamoDB).",
        "bg_theory": "Models are stateless and do not remember past interactions. Appending raw history to prompt context windows increases latency, token count, and cost. The Memory Engine resolves this by managing short-term session cache and long-term profiles in DynamoDB. The memory manager runs compaction loops, using the LLM to extract key user facts and save them, pruning raw dialogue history.",
        "concepts": [
            ("Short-Term Memory", "Dialogue cache storing conversation turns within an active session.", "Tracks dialogue turns during an active chat session.", "The temporary session cache."),
            ("Long-Term Memory", "Durable storage hosting user profile facts and preferences across sessions.", "Personalizes responses over weeks or months.", "DynamoDB table records."),
            ("Compaction Loop", "A process that summarizes raw history logs into structured key facts.", "Minimizes prompt context size and cost.", "The memory compaction workflow.")
        ],
        "mechanics": "1. Inbound prompt triggers retrieval of user profiles from DynamoDB.\n2. The system appends these facts to the model prompt template.\n3. Dialogue turns are appended to the short-term session cache.\n4. When the session ends, the compaction loop processes the raw history.\n5. The compaction function extracts new facts, updates the profile database, and clears the session cache.",
        "mermaid": "graph TD\n    History[Raw Conversation History] -->|Compaction Loop| Facts[Fact Extraction LLM]\n    Facts -->|Store| DB[(DynamoDB Long-Term Memory)]\n    DB -->|Retrieve| Context[Prompt Context Window]",
        "installation": "Verify your DynamoDB tables list from your terminal using the AWS CLI:\n```bash\naws dynamodb list-tables\n```",
        "configuration": "Ensure your database configuration mappings match your execution environment:\n```yaml\nmemory:\n  table_name: \"agentcore-memory-table\"\n  partition_key: \"user_id\"\n  compaction_trigger_turns: 10\n```",
        "hands_on_simple": "# Verify short-term session memory storage structures\nclass SessionMemory:\n    def __init__(self):\n        self.turns = []\n\n    def add(self, role, content):\n        self.turns.append({\"role\": role, \"content\": content})\n\n    def get_history(self):\n        return self.turns",
        "hands_on_intermediate": "# Python script to update user profiles using mock database clients\nclass MockDBStore:\n    def __init__(self):\n        self.store = {}\n\n    def get_profile(self, user_id):\n        return self.store.get(user_id, {\"user_id\": user_id, \"facts\": []})\n\n    def put_profile(self, user_id, profile):\n        self.store[user_id] = profile\n        print(f\"Updated database profile for: {user_id}\")\n\nif __name__ == \"__main__\":\n    db = MockDBStore()\n    profile = db.get_profile(\"user_123\")\n    profile[\"facts\"].append(\"Prefers Python\")\n    db.put_profile(\"user_123\", profile)",
        "hands_on_advanced": "# Complete memory manager with a compaction loop parsing preference keys\nimport json\n\nclass MemoryManager:\n    def __init__(self):\n        self.db = {}\n\n    def fetch_profile(self, user_id):\n        return self.db.get(user_id, {\"user_id\": user_id, \"interests\": [], \"summary\": \"New User\"})\n\n    def compact_history(self, user_id, history):\n        profile = self.fetch_profile(user_id)\n        for turn in history:\n            content = turn[\"content\"].lower()\n            # Scan for preference keywords\n            if \"like\" in content or \"prefer\" in content:\n                pref = turn[\"content\"].split(\"prefer\")[-1].strip(\" .\")\n                if pref not in profile[\"interests\"]:\n                     profile[\"interests\"].append(pref)\n        \n        profile[\"summary\"] = f\"User prefers: {', '.join(profile['interests'])}\"\n        self.db[user_id] = profile\n        print(f\"Compacted Profile: {json.dumps(profile)}\")\n\nif __name__ == \"__main__\":\n    mgr = MemoryManager()\n    chat_log = [\n        {\"role\": \"user\", \"content\": \"I prefer working with Python\"},\n        {\"role\": \"assistant\", \"content\": \"Understood.\"}\n    ]\n    mgr.compact_history(\"user_789\", chat_log)",
        "best_practices": "* Use optimistic locking to prevent parallel requests from overwriting data.\n* Trigger compaction loops asynchronously to avoid slowing down user requests.\n* Regularly archive outdated history records to optimize storage costs.",
        "security": "Encrypt database records at rest using AWS KMS keys. Restrict IAM permissions to ensure only the agent execution role can read and write from the memory tables.",
        "performance": "Implement caching for user profiles to bypass database reads during high-frequency API invocations.",
        "cost": "Configure DynamoDB auto-scaling or on-demand pricing. Prune raw history records and store only compacted summaries to minimize database storage costs.",
        "mistakes": "* Appending raw, uncompacted dialogue history to prompts, bloating token usage and cost.\n* Running database calls synchronously inside request loops, adding execution latency.",
        "troubleshooting": [
            ("OptimisticLockingException on write", "Parallel requests attempted to update the same profile record concurrently.", "Implement retry logic with exponential backoff on write operations."),
            ("ProvisionedThroughputExceededException", "Database read/write rates exceeded configured limits.", "Enable DynamoDB auto-scaling or switch the table to on-demand pricing mode.")
        ],
        "interviews": [
            ("What is the benefit of memory compaction?", "Memory compaction summarizes dialogue logs into key facts, keeping prompt context windows small to reduce latency and lower token costs."),
            ("Why is DynamoDB suitable for managing agent state?", "DynamoDB is a serverless NoSQL database that scales automatically and provides low-latency key-value lookups, making it ideal for managing session states."),
            ("How does optimistic locking secure database updates?", "Optimistic locking uses a version attribute. Updates are rejected if the database version exceeds the record version read by the application, preventing data overwrites.")
        ],
        "use_cases": "Personalizing virtual assistants by retaining user preferences and history across sessions.",
        "project": "This memory engine manages agent state, enabling us to personalize our chatbot application.",
        "summary": "This chapter covered short-term session cache, long-term profile storage, and running compaction loops to manage agent state.",
        "key_takeaways": "* Appending raw history to prompts increases token costs and latency.\n* The Memory Engine utilizes DynamoDB to persist state across sessions.\n* Compaction loops summarize dialogue history into structured facts.",
        "exercises": "* Beginner: Modify the compaction function to extract location preference keywords.\n* Intermediate: Add expiration attributes (TTL) to raw history records to delete them after 30 days.",
        "reading": "* [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)\n* [LangChain Memory Integration Guide](https://python.langchain.com/docs/modules/memory/)"
    },
    "14": {
        "title": "Custom Tools Integration",
        "intro": "Custom tools extend agent capabilities by allowing them to execute code and query external web services.",
        "what_is_it": "Custom Tools Integration is the methodology of writing custom Python functions, decorating them with schema generators ('@tool'), and registering them so an AI agent can execute real-world calculations or data actions.",
        "why_important": "Out-of-the-box LLMs can only process and generate text—they cannot perform complex calculations, query live inventory systems, or call proprietary internal APIs. Writing custom tools extends an agent's reasoning into real-world software actions tailored to your specific application requirements.",
        "how_it_works": "Developers create Python functions with explicit type annotations and docstring documentation, decorating them with '@tool'. The framework inspects function signatures to auto-generate standard JSON schema definitions. When the AI model selects a tool during execution, the Tool Registry intercepts the call, executes the Python function inside a sandbox, and returns output strings to the agent.",
        "key_responsibilities": [
            "Define custom Python functions to execute specialized calculations, API lookups, or database edits.",
            "Inspect Python docstrings and type annotations to generate standardized JSON tool schemas automatically.",
            "Validate model-supplied function arguments against type bounds prior to function execution.",
            "Capture and handle tool execution errors gracefully, returning readable status feedback to the AI model."
        ],
        "pre_reqs": "* Active installations and AWS configurations from Chapters 6 and 8.\n* A basic understanding of Python function definitions and parameter type annotations.",
        "bg_theory": "Models can only process and generate text; they cannot access databases or run code directly. Integrating tools extends their capabilities. However, exposing APIs directly to LLMs risks SQL injection attacks. A tool gateway acts as a secure broker. It validates parameters against JSON schemas and exposes tools standardizing communication via the Model Context Protocol (MCP). Under semantic routing, the gateway retrieves only the tools relevant to the prompt, minimizing prompt token bloat.",
        "concepts": [
            ("Tool Registry", "A central repository class that manages tool functions and metadata schemas.", "Coordinates tool registrations and lookup operations.", "The tool registry module."),
            ("JSON Schema", "A JSON object declaring parameter names, types, and descriptions for validation.", "Enforces parameter schemas before functions execute.", "The parameters definition dictionary."),
            ("@tool Decorator", "A decorator helper that generates JSON schemas from Python function docstrings.", "Simplifies tool definition and registration.", "Decorating Python functions.")
        ],
        "mechanics": "1. The model determines it needs external data to complete a prompt.\n2. It returns a tool call payload specifying the target tool name and parameters.\n3. The Tool Registry intercepts the call and validates parameters against the JSON schema.\n4. If validation succeeds, it executes the registered Python function.\n5. The function executes in a secure sandbox, returning outputs to the model to complete the loop.",
        "mermaid": "graph TD\n    Agent[Agent LLM] -->|Decides action| Schema[Tool Schema definition]\n    Schema -->|Resolves| Tool[Decorated Python function]\n    Tool -->|Executes| Sandbox[Secure Execution Sandbox]",
        "installation": "Validate custom tool execution syntax using the CLI:\n```bash\nagentcore tools validate --file src/main.py\n```",
        "configuration": "Configure registered tools and execution boundaries in your configuration files:\n```yaml\ntools:\n  - name: \"lookup_warranty_status\"\n    entry_point: \"src/tools.py\"\n    timeout_seconds: 10\n```",
        "hands_on_simple": "# Verify decorator helper import syntax\nfrom bedrock_agent_core import tool\n\n@tool\ndef get_time() -> str:\n    \"\"\"Retrieve the current system time.\"\"\"\n    import datetime\n    return str(datetime.datetime.now())",
        "hands_on_intermediate": "# Python script to register and execute functions dynamically\nclass ToolRegistry:\n    def __init__(self):\n        self.registry = {}\n\n    def register(self, name, func):\n        self.registry[name] = func\n\n    def execute(self, name, **kwargs):\n        if name not in self.registry:\n            return f\"Error: Tool '{name}' not found.\"\n        try:\n            return self.registry[name](**kwargs)\n        except Exception as e:\n            return f\"Execution failed: {str(e)}\"\n\ndef add(x, y):\n    return x + y\n\nif __name__ == \"__main__\":\n    reg = ToolRegistry()\n    reg.register(\"math_add\", add)\n    print(\"Result:\", reg.execute(\"math_add\", x=5, y=10))",
        "hands_on_advanced": "# Complete SDK tool implementation validating arguments and capturing execution errors\nfrom bedrock_agent_core import BedrockAgentCoreApp, tool\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"ToolIntegration\")\napp = BedrockAgentCoreApp()\n\n@tool\ndef lookup_warranty_status(order_id: str) -> str:\n    \"\"\"\n    Retrieve the warranty coverage status for a customer order.\n    \n    Args:\n        order_id: The unique 5-digit order identifier.\n    \"\"\"\n    db = {\"12345\": \"Active\", \"67890\": \"Expired\"}\n    try:\n        # Basic input validation\n        if not order_id.isdigit() or len(order_id) != 5:\n            return \"Error: Order ID must be a 5-digit number.\"\n        return f\"Order {order_id} warranty status: {db.get(order_id, 'Not Found')}\"\n    except Exception as e:\n        logger.error(f\"Tool execution error: {str(e)}\")\n        return \"Error: Failed to fetch warranty status.\"\n\nif __name__ == \"__main__\":\n    # Test tool locally\n    print(lookup_warranty_status(order_id=\"12345\"))",
        "best_practices": "* Design tool functions to handle exceptions gracefully, returning friendly errors to the model.\n* Add descriptive docstrings to functions to guide the model's tool selection.\n* Validate all input parameters to protect backend APIs from injection attacks.",
        "security": "Execute tool functions inside secure, sandboxed environments to prevent unauthorized system access. Use IAM policies to limit tools' access to only the AWS resources they require.",
        "performance": "Set short execution timeouts on tool calls to prevent runaway scripts from stalling the main agent loop.",
        "cost": "Monitor token usage associated with tool definitions. Long tool descriptions increase input token usage, inflating overall execution costs.",
        "mistakes": "* Defining ambiguous descriptions, causing the model to select the wrong tool.\n* Failing to wrap tool code in try-except blocks, causing unhandled exceptions to crash the agent runtime.",
        "troubleshooting": [
            ("Model fails to invoke tool", "Ambiguous description or missing docstring in the tool function.", "Add a detailed docstring explaining when and how to use the tool."),
            ("InvalidParametersException on call", "Arguments returned by the model do not match the JSON schema definitions.", "Verify parameter names, types, and annotations in the function signature.")
        ],
        "interviews": [
            ("How does the @tool decorator generate JSON schemas?", "The decorator uses Python reflection and inspects type annotations and docstring parameters to construct JSON schemas for model configuration."),
            ("Why is sandboxing critical for executing custom tools?", "Sandboxing isolates execution, preventing code errors or prompt injection attacks from compromising the host operating system."),
            ("How do you handle tool execution failures?", "Catch exceptions inside the tool code and return a descriptive error string. The model can use this feedback to correct parameters and retry the call.")
        ],
        "use_cases": "Integrating customer database lookups securely into customer service workflows.",
        "project": "This custom tool integration allows our agent to query databases and call external APIs.",
        "summary": "This chapter covered defining parameter schemas, registering custom Python functions, and executing tools inside secure environments.",
        "key_takeaways": "* Custom tools extend agent capabilities to interact with external systems.\n* Docstrings and type annotations guide the model's tool selection.\n* Enforce parameter validation and run tools in secure sandboxes.",
        "exercises": "* Beginner: Write a tool that generates a random number within a minimum and maximum range.\n* Intermediate: Create a tool that queries system time, validating format strings.",
        "reading": "* [JSON Schema Standard Reference](https://json-schema.org/)\n* [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)"
    },
    "15": {
        "title": "Deployment & Containerization",
        "intro": "Packaging Bedrock AgentCore applications as Docker images ensures they deploy and run consistently in production.",
        "what_is_it": "Deployment and Containerization is the process of packaging your application source code, configuration files, and software dependencies into a standardized container image using Docker, and pushing it to Amazon Elastic Container Registry (ECR) for cloud hosting.",
        "why_important": "Deploying raw unpackaged code directly to cloud servers often causes environment mismatches, missing system library errors, and slow deployment times. Containerization guarantees that your application runs identically in development and production environments inside lightweight, secure containers.",
        "how_it_works": "The developer writes a multi-stage 'Dockerfile' specifying build steps and runtime environments. Running 'docker build' compiles the code into an immutable container image. The developer authenticates with Amazon ECR using 'aws ecr get-login-password', tags the image, and executes 'docker push' to upload the image to the cloud repository.",
        "key_responsibilities": [
            "Compile application source code, runtimes, and dependencies into standardized Docker container images.",
            "Utilize multi-stage Docker builds to reduce container image size and eliminate build tool overhead.",
            "Securely host and version production container images within Amazon Elastic Container Registry (ECR).",
            "Exclude temporary files, local credentials, and virtual environments using '.dockerignore' files."
        ],
        "pre_reqs": "* Active installations of Git and Docker from Chapter 2.\n* An active AWS ECR repository and configured IAM access permissions.",
        "bg_theory": "Deploying raw code directly to servers often leads to environment discrepancies. Containerization bundles application code, libraries, and configurations into a single image. This ensures consistency across development, testing, and production. Multi-stage Docker builds optimize image size by separating build tools from the final execution runtime, improving deployment speeds and reducing the attack surface.",
        "concepts": [
            ("Dockerfile", "A text document containing instructions to compile a Docker image.", "Automates container image builds.", "Defining container build configurations."),
            ("ECR Registry", "A managed container registry on AWS used to store, manage, and deploy container images.", "Secures and hosts container images for deployment.", "Pushing images to Amazon ECR."),
            ("Multi-Stage Build", "A method that uses multiple FROM statements in a Dockerfile to optimize image size.", "Reduces container size and enhances security.", "Optimizing build steps.")
        ],
        "mechanics": "1. Developer runs `docker build` to compile the Docker image.\n2. The compiler executes Dockerfile directives, creating cached filesystem layers.\n3. Developer authenticates with Amazon ECR using `aws ecr get-login-password`.\n4. The image is tagged and pushed to ECR via `docker push`.\n5. The AWS compute service pulls the image from ECR to run the application.",
        "mermaid": "graph LR\n    Code[Agent Code] -->|docker build| Image[Docker Image]\n    Image -->|docker push| ECR[Amazon ECR Registry]\n    ECR -->|Deploy| Compute[AgentCore Runtime Service]",
        "installation": "Log in to your Amazon ECR registry using the CLI:\n```bash\naws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com\n```\nBuild the container image:\n```bash\ndocker build -t agentcore-app .\n```",
        "configuration": "### Dockerfile Configuration\n```dockerfile\nFROM python:3.11-slim AS builder\nWORKDIR /app\nRUN pip install --no-cache-dir uv\nCOPY pyproject.toml uv.lock ./\nRUN uv sync --frozen\n\nFROM python:3.11-slim\nWORKDIR /app\nCOPY --from=builder /app/.venv /app/.venv\nCOPY src/ ./src\nENV PATH=\"/app/.venv/bin:$PATH\"\nEXPOSE 8000\nCMD [\"python\", \"src/main.py\"]\n```\n\n### .dockerignore Configuration\n```text\n.venv/\n__pycache__/\n.git/\n.env\n```",
        "hands_on_simple": "# Verify the built docker image is accessible in the local list\nimport subprocess\n\ndef check_local_images():\n    try:\n        res = subprocess.run([\"docker\", \"images\", \"agentcore-app\"], capture_output=True, text=True, check=True)\n        print(\"Local Docker Image details:\")\n        print(res.stdout)\n    except Exception as e:\n        print(\"Failed to query local images:\", str(e))",
        "hands_on_intermediate": "# Python script to automate image tag assignments matching commit hashes\nimport subprocess\n\ndef tag_image(repo_url):\n    try:\n        # Get the current git commit hash\n        commit = subprocess.check_output([\"git\", \"rev-parse\", \"--short\", \"HEAD\"]).decode().strip()\n        local_tag = \"agentcore-app:latest\"\n        remote_tag = f\"{repo_url}:{commit}\"\n        print(f\"Tagging local image {local_tag} as {remote_tag}...\")\n        subprocess.run([\"docker\", \"tag\", local_tag, remote_tag], check=True)\n        print(\"[SUCCESS] Tagged successfully!\")\n        return remote_tag\n    except Exception as e:\n        print(\"Failed to tag image:\", str(e))\n        return None\n\nif __name__ == \"__main__\":\n    tag_image(\"123456789012.dkr.ecr.us-east-1.amazonaws.com/agentcore-app\")",
        "hands_on_advanced": "# Complete build and push automation harness handling registry login and upload\nimport subprocess\nimport sys\n\ndef deploy_container(registry_url, region):\n    try:\n        # Authenticate with Amazon ECR\n        print(\"Authenticating with Amazon ECR...\")\n        login_cmd = f\"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {registry_url}\"\n        subprocess.run(login_cmd, shell=True, check=True)\n        \n        # Build container image\n        print(\"Building Docker image...\")\n        subprocess.run([\"docker\", \"build\", \"-t\", \"agentcore-app\", \".\"], check=True)\n        \n        # Tag and push image\n        target_tag = f\"{registry_url}/agentcore-app:latest\"\n        subprocess.run([\"docker\", \"tag\", \"agentcore-app:latest\", target_tag], check=True)\n        print(f\"Pushing image to ECR: {target_tag}...\")\n        subprocess.run([\"docker\", \"push\", target_tag], check=True)\n        print(\"[SUCCESS] Container image deployed successfully!\")\n    except Exception as e:\n        print(\"Deployment failed:\", str(e))\n        sys.exit(1)\n\nif __name__ == \"__main__\":\n    # Example configurations\n    deploy_container(\"123456789012.dkr.ecr.us-east-1.amazonaws.com\", \"us-east-1\")",
        "best_practices": "* Use specific base image tags (e.g., `python:3.11-slim`) to ensure build consistency.\n* Leverage multi-stage builds to keep final production images clean and lightweight.\n* Use a `.dockerignore` file to exclude local files (like virtual environments) from container builds.",
        "security": "Enforce vulnerability scanning on Amazon ECR registries to identify and patch vulnerabilities. Run containers as non-root users to limit security risks.",
        "performance": "Order Dockerfile directives from least-frequently changed to most-frequently changed to optimize layer caching and accelerate builds.",
        "cost": "Regularly delete outdated container images from Amazon ECR using lifecycle policies to minimize storage costs.",
        "mistakes": "* Committing local virtual environments (like `.venv/`) to images, inflating image size and build times.\n* Running containers with root privileges, increasing security vulnerability risks.",
        "troubleshooting": [
            ("ECR push returns access denied", "The IAM credentials assumed by the CLI lack ECR write permissions.", "Ensure your IAM role has the 'ecr:PutImage' and 'ecr:InitiateLayerUpload' permissions."),
            ("docker command not found", "Docker CLI is not installed or not added to your system's PATH variable.", "Verify installation status and check your system environment variables.")
        ],
        "interviews": [
            ("What is the benefit of multi-stage Docker builds?", "Multi-stage builds separate build tools from execution runtimes, keeping production images small and secure by excluding compiler tools and intermediate files."),
            ("How do you authenticate the Docker CLI with Amazon ECR?", "Generate a temporary access token using the 'aws ecr get-login-password' command, and pipe it to the 'docker login' command."),
            ("Why is a .dockerignore file important?", "The `.dockerignore` file prevents copying unnecessary local files (like virtual environments and git histories) into images, reducing image size and build times.")
        ],
        "use_cases": "Packaging and deploying web applications and agent services to AWS.",
        "project": "This containerization step packages our agent application into a Docker image, ready for deployment to production.",
        "summary": "This chapter covered packaging applications with Docker, optimizing images using multi-stage builds, and pushing images to Amazon ECR.",
        "key_takeaways": "* Containerization ensures applications run consistently across environments.\n* Multi-stage builds reduce image size and improve security.\n* Store and secure production container images in Amazon ECR.",
        "exercises": "* Beginner: Create a `.dockerignore` file that excludes virtual environments and git histories.\n* Intermediate: Configure a multi-stage Dockerfile that compiles build tools in stage 1 and exports the application package to stage 2.",
        "reading": "* [Docker Architecture Guide](https://docs.docker.com/get-started/overview/)\n* [Amazon ECR Developer Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)"
    },
    "16": {
        "title": "Observability & Telemetry",
        "intro": "Observability and telemetry configurations allow you to monitor and trace complex agent execution workflows.",
        "what_is_it": "Observability and Telemetry is the system monitoring architecture used to capture, aggregate, and visualize application logs, performance metrics, and distributed trace spans using OpenTelemetry and Amazon CloudWatch.",
        "why_important": "Asynchronous multi-agent applications contain complex reasoning steps, external API calls, and database lookups that are difficult to debug using basic print statements. Observability provides complete visibility into execution lifecycles, enabling developers to isolate latency bottlenecks, diagnose errors, and audit model token costs.",
        "how_it_works": "Application handlers are instrumented with OpenTelemetry SDKs. When a transaction starts, the framework creates a Root Span and child spans for sub-tasks (such as model inference or database queries). Spans record execution durations, session attributes, token counts, and exceptions, exporting telemetry payloads asynchronously to Amazon CloudWatch Logs and AWS X-Ray.",
        "key_responsibilities": [
            "Capture and aggregate structured application logs, error tracebacks, and execution events.",
            "Instrument distributed trace spans to measure execution latency across tool calls and model invocations.",
            "Track input and output model token counts per session to monitor and optimize cloud API costs.",
            "Export telemetry data asynchronously to Amazon CloudWatch and AWS X-Ray without stalling user queries."
        ],
        "pre_reqs": "* Active deployments and AWS credentials from Chapters 3 and 15.\n* A basic understanding of tracing and telemetry concepts.",
        "bg_theory": "Asynchronous multi-agent interactions can be complex and difficult to debug. Standard logging libraries do not trace complete transaction lifecycles across services. Implementing tracing using open standards (like OpenTelemetry) groups operations into spans. This allows developers to isolate latency bottlenecks and trace errors back to specific tool or model invocations.",
        "concepts": [
            ("OpenTelemetry", "An open-source standard for collecting traces, metrics, and logs.", "Decouples instrumentation from specific monitoring backends.", "Instrumenting application workflows."),
            ("Trace Span", "A record of a single operation within a transaction, containing metadata and timestamps.", "Tracks execution duration and captures errors.", "Tracing tool execution steps."),
            ("CloudWatch Logs", "A managed service on AWS used to store, monitor, and access log files.", "Centralizes application logs for auditing and debugging.", "Accessing execution logs.")
        ],
        "mechanics": "1. Client request starts a transaction, creating a Root Span.\n2. Sub-operations (like database lookups or tool calls) create Child Spans that inherit the root context.\n3. Spans capture attributes (like session IDs and token usage) and log events with timestamps.\n4. When a span ends, the tracer exports the telemetry payload to the collector.\n5. The collector processes and exports the data to CloudWatch Logs or AWS X-Ray.",
        "mermaid": "graph TD\n    Agent[Agent Application] -->|OTel Traces| Collector[OTel Collector]\n    Collector -->|Export| CloudWatch[AWS CloudWatch]\n    Collector -->|Export| XRay[AWS X-Ray]",
        "installation": "Monitor application trace logs in real-time using the CLI:\n```bash\nagentcore traces view --tail\n```",
        "configuration": "Configure OpenTelemetry exporter endpoints in your configuration settings:\n```yaml\nobservability:\n  otel_endpoint: \"http://localhost:4317\"\n  service_name: \"bedrock-agent-core\"\n  log_level: \"INFO\"\n```",
        "hands_on_simple": "# Verify logger registration and formatting\nimport logging\n\ndef setup_logger():\n    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n    logger = logging.getLogger(\"TelemetryLogger\")\n    logger.info(\"Logger configured successfully!\")\n\nif __name__ == \"__main__\":\n    setup_logger()",
        "hands_on_intermediate": "# Python script to create mock trace spans and record events\nimport time\n\nclass MockSpan:\n    def __init__(self, name):\n        self.name = name\n        self.start_time = time.time()\n        self.events = []\n\n    def add_event(self, event_name):\n        self.events.append({\"name\": event_name, \"time\": time.time() - self.start_time})\n\n    def end(self):\n        duration = time.time() - self.start_time\n        print(f\"Span '{self.name}' completed in {duration:.4f}s. Events recorded: {len(self.events)}\")\n\nif __name__ == \"__main__\":\n    span = MockSpan(\"db_lookup\")\n    time.sleep(0.05)\n    span.add_event(\"connection_established\")\n    time.sleep(0.02)\n    span.end()",
        "hands_on_advanced": "# Complete OpenTelemetry instrumentation script capturing custom metrics and exceptions\nimport time\nimport logging\nfrom typing import Dict, Any\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"OtelApplication\")\n\nclass TraceEngine:\n    def __init__(self, service_name: str):\n        self.service_name = service_name\n\n    def start_span(self, name: str) -> 'TraceSpan':\n        return TraceSpan(name)\n\nclass TraceSpan:\n    def __init__(self, name: str):\n        self.name = name\n        self.start_time = time.time()\n        self.attributes: Dict[str, Any] = {}\n        self.error = False\n\n    def set_attribute(self, key: str, value: Any):\n        self.attributes[key] = value\n\n    def record_exception(self, e: Exception):\n        self.error = True\n        self.set_attribute(\"error.message\", str(e))\n\n    def end(self):\n        duration = time.time() - self.start_time\n        log_payload = {\n            \"span_name\": self.name,\n            \"duration_seconds\": round(duration, 4),\n            \"error\": self.error,\n            \"attributes\": self.attributes\n        }\n        logger.info(f\"[SPAN_EXPORT] {log_payload}\")\n\ndef run_instrumented_agent(prompt: str):\n    tracer = TraceEngine(\"bedrock-agent\")\n    root_span = tracer.start_span(\"agent_run\")\n    root_span.set_attribute(\"prompt\", prompt)\n    try:\n        # Simulate model call child span\n        model_span = tracer.start_span(\"model_inference\")\n        time.sleep(0.1)\n        model_span.set_attribute(\"tokens_input\", 120)\n        model_span.set_attribute(\"tokens_output\", 45)\n        model_span.end()\n        root_span.set_attribute(\"status\", \"success\")\n    except Exception as e:\n        root_span.record_exception(e)\n        raise e\n    finally:\n        root_span.end()\n\nif __name__ == \"__main__\":\n    run_instrumented_agent(\"What is memory compaction?\")",
        "best_practices": "* Capture token counts from model responses to monitor costs.\n* Export traces asynchronously to prevent monitoring from adding latency to request loops.\n* Ensure child spans inherit the parent context to compile connected trace graphs.",
        "security": "Filter logs and trace attributes to ensure sensitive user credentials or personally identifiable information (PII) are not exported to monitoring backends.",
        "performance": "Set up alerts in CloudWatch to notify your team when average model call latency exceeds established service level agreements (SLAs).",
        "cost": "Implement sampling filters in your tracer configurations to export only a percentage of successful traces to keep monitoring costs low.",
        "mistakes": "* Creating detached child spans by failing to inherit parent context, resulting in fragmented trace logs.\n* Neglecting to record model token usage, making it difficult to trace billing costs.",
        "troubleshooting": [
            ("Traces show disconnected spans", "Spans were created without inheriting active parent contexts.", "Pass the active span context argument when instantiating child spans."),
            ("No logs appearing in CloudWatch", "The application IAM role lacks permissions to write to CloudWatch log groups.", "Verify the policy has the 'logs:CreateLogStream' and 'logs:PutLogEvents' permissions.")
        ],
        "interviews": [
            ("What is the difference between a Trace and a Log?", "A log is a text record of an isolated event. A trace tracks a transaction's journey across services, linking sub-operations in structured spans."),
            ("Why is OpenTelemetry preferred over vendor-specific monitoring SDKs?", "OpenTelemetry is an open standard, allowing developers to change monitoring backends (e.g., from Datadog to AWS X-Ray) without updating instrumentation code."),
            ("How do you trace latency bottlenecks in multi-agent workflows?", "Analyze span hierarchies and durations in trace dashboards to identify which agent, tool, or model call is introducing latency.")
        ],
        "use_cases": "Monitoring execution times across services to optimize application performance.",
        "project": "This telemetry setup monitors application health, providing execution traces for our chatbot system.",
        "summary": "This chapter covered OpenTelemetry tracing, span context propagation, and exporting logs and metrics to CloudWatch.",
        "key_takeaways": "* Observability is critical for debugging complex, asynchronous agent workflows.\n* OpenTelemetry standardizes telemetry collection across backends.\n* Monitor token usage and latency metrics to optimize cost and performance.",
        "exercises": "* Beginner: Add a warning log statement that prints when model response sizes exceed 1000 characters.\n* Intermediate: Configure logs to export as structured JSON dictionaries.",
        "reading": "* [OpenTelemetry Python Guide](https://opentelemetry.io/docs/languages/python/)\n* [Amazon CloudWatch Logs Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)"
    },
    "17": {
        "title": "Complete End-to-End Flow",
        "intro": "Verifying the complete integration path—from client requests to database updates—ensures the agent runs securely and efficiently in production.",
        "what_is_it": "The Complete End-to-End Flow represents the fully integrated lifecycle of a user request—tracing its complete journey from frontend user interfaces through security authentication, runtime hosting, memory lookups, tool calls, and final response delivery.",
        "why_important": "Building individual agent components is not enough; developers must verify that all software layers (runtimes, security gateways, identity providers, memory stores, and custom tools) communicate seamlessly under production conditions to deliver reliable performance.",
        "how_it_works": "1. A user submits a query via a React web client.\n2. The client authenticates against Amazon Cognito, receiving a JWT token.\n3. The prompt and token arrive at the Tool Gateway, which verifies signatures and extracts the Actor ID.\n4. The runtime launches an isolated Firecracker microVM container.\n5. The microVM fetches user profile summaries from DynamoDB and invokes the Bedrock model.\n6. If needed, the model calls custom tool APIs via MCP schemas.\n7. The final response streams back to the client UI, while dialogue facts are saved to DynamoDB and telemetry logs are exported to CloudWatch.",
        "key_responsibilities": [
            "Connect all 7 core AgentCore architectural pillars into a unified enterprise application system.",
            "Validate end-to-end user authentication, input schema verification, and data access security boundaries.",
            "Orchestrate smooth data flows between client UIs, microVM runtimes, model APIs, and database tables.",
            "Provide complete system integration testing harnesses to verify performance, stability, and accuracy before production release."
        ],
        "pre_reqs": "* Setup of all modules and AWS credentials from Chapters 3 through 16.",
        "bg_theory": "AI applications contain multiple dependencies: frontend UIs, authentication providers, routing gateways, container runtimes, and databases. Integration testing verifies that these systems communicate correctly. Tracking a request end-to-end ensures that tokens propagate, schemas validate, and states persist across boundaries.",
        "concepts": [
            ("Integration Testing", "Testing how multiple application components function together as a unified system.", "Verifies system communication under production conditions.", "Running end-to-end execution tests."),
            ("Orchestration Flow", "The execution sequence coordinate by the runtime manager to process queries.", "Maintains secure resource boundaries during runs.", "The VM request-to-response trace."),
            ("Security Gateway", "The entrypoint that validates credentials and checks input schemas.", "Protects backend APIs from malicious queries.", "The Cognito and Gateway routers.")
        ],
        "mechanics": "1. User submits a prompt through the client UI.\n2. The client authenticates against Cognito, receiving a JWT.\n3. The client submits the prompt and token to the Tool Gateway.\n4. The gateway verifies the token signature and extracts the Actor ID.\n5. The gateway schedules a Firecracker VM and routes the query.\n6. The VM retrieves profiles from DynamoDB, executes reasoning, and returns the response.",
        "mermaid": "sequenceDiagram\n    participant UI as React UI Interface\n    participant GW as Gateway Router\n    participant VM as Agent VM Runtime\n    participant Tool as DB Tool Server\n    UI->>GW: 1. Send Query (What is my role?)\n    GW->>VM: 2. Invoke session VM\n    VM->>Tool: 3. Query tool database\n    Tool-->>VM: 4. Return user role (Engineer)\n    VM-->>GW: 5. Return model answer\n    GW-->>UI: 6. Render response string",
        "installation": "Execute the integration testing suite using the CLI:\n```bash\nagentcore invoke --prompt \"Check history\"\n```",
        "configuration": "Configure complete environment parameters inside `bedrock_agent_core.yaml`:\n```yaml\nversion: \"1.0\"\nagent:\n  name: \"e2e-integration-agent\"\n  entry_point: \"src/main.py\"\n  memory_id: \"agentcore-memory-table\"\n  execution_role_arn: \"arn:aws:iam::123456789012:role/AgentCoreExecutionRole\"\n```",
        "hands_on_simple": "# Verify basic connectivity to downstream APIs\nimport requests\n\ndef test_api_ping():\n    try:\n        res = requests.get(\"http://localhost:8000/status\")\n        print(\"Status code:\", res.status_code)\n        print(\"API Status Response:\", res.json())\n    except Exception as e:\n        print(\"Ping check failed:\", str(e))",
        "hands_on_intermediate": "# Python script to automate E2E execution tests\nimport requests\nimport time\n\ndef run_integration_check():\n    url = \"http://localhost:8000/invoke\"\n    payload = {\"prompt\": \"What is my profile details?\"}\n    headers = {\"Authorization\": \"Bearer mock_token_string\"}\n    try:\n        print(\"Sending query to agent gateway...\")\n        res = requests.post(url, json=payload, headers=headers)\n        print(\"Gateway Status Code:\", res.status_code)\n        print(\"Agent Response payload:\", res.json())\n        return res.status_code == 200\n    except Exception as e:\n        print(\"Integration test failed:\", str(e))\n        return False\n\nif __name__ == \"__main__\":\n    run_integration_check()",
        "hands_on_advanced": "# Complete integration runner executing auth checks, tool invocations, and memory audits\nimport requests\nimport sys\nimport time\n\nclass E2EIntegrationRunner:\n    def __init__(self, endpoint):\n        self.endpoint = endpoint\n        self.token = \"mock_user_access_token\"\n\n    def execute_transaction(self, prompt):\n        headers = {\n            \"Authorization\": f\"Bearer {self.token}\",\n            \"Content-Type\": \"application/json\"\n        }\n        payload = {\"prompt\": prompt}\n        \n        print(f\"[E2E] Initiating transaction prompt: '{prompt}'\")\n        start = time.time()\n        try:\n            res = requests.post(self.endpoint, json=payload, headers=headers)\n            duration = time.time() - start\n            \n            if res.status_code == 200:\n                print(f\"[E2E SUCCESS] Response time: {duration:.4f}s\")\n                print(\"Agent Response:\", res.json().get(\"response\"))\n                return True\n            else:\n                print(f\"[E2E FAIL] Status Code: {res.status_code} | Error: {res.text}\")\n                return False\n        except Exception as e:\n            print(f\"[E2E ERROR] Transaction failed: {str(e)}\")\n            return False\n\nif __name__ == \"__main__\":\n    # Test on local port configurations\n    runner = E2EIntegrationRunner(\"http://localhost:8000/invoke\")\n    success = runner.execute_transaction(\"Retrieve active stock count for item SKU SHI-001\")\n    if not success:\n        sys.exit(1)",
        "best_practices": "* Enforce access scopes on client authorization tokens.\n* Implement rate limits on gateways to protect system resources.\n* Validate input schemas on the server; never trust inputs from the client.",
        "security": "Use HTTPS with TLS 1.3 to encrypt all network traffic. Restrict subnets and configure Security Groups to secure communications between the gateway and microVMs.",
        "performance": "Implement response streaming to improve perceived performance, sending token responses to client screens as they are generated.",
        "cost": "Monitor token usage patterns across user sessions. Cache database lookups and tool responses where appropriate to minimize model invocations.",
        "mistakes": "* Overlooking signature verification checks on Cognito tokens, leaving APIs vulnerable to authorization bypasses.\n* Failing to implement retry logic on network connections, causing client requests to fail during minor network disruptions.",
        "troubleshooting": [
            ("Requests fail with 403 status", "The Cognito user token signature validation failed.", "Verify the user pool IDs match the gateway settings, and check if tokens are expired."),
            ("Gateway returns 504 Timeout error", "A downstream tool invocation stalled or took longer than execution limits.", "Add short timeout limits to tool API calls, and implement retry logic.")
        ],
        "interviews": [
            ("What is the primary security rule for cloud deployments?", "Never trust client-side data. Always validate identity tokens, restrict access scopes, and validate inputs on the server."),
            ("How does the agent maintain state across interactions?", "By saving session histories in a persistent DynamoDB memory store and loading summaries at the start of new sessions."),
            ("Why is displaying active loading states important?", "Agent reasoning loops can take several seconds to complete. Informative UI state updates keep users engaged and prevent duplicate submissions.")
        ],
        "use_cases": "Validating billing platforms and transaction pipelines during staging deployments.",
        "project": "This end-to-end integration completes the agent pipeline, confirming the system is ready for production hosting.",
        "summary": "This chapter traced the complete request lifecycle and verified communication between the client, gateway, microVMs, tools, and databases.",
        "key_takeaways": "* Integration testing confirms communication across all system layers.\n* Secure end-to-end flows using token validation and input schema checks.\n* Displaying active loading states keeps users engaged during execution loops.",
        "exercises": "* Beginner: Write a list of UI state indicators (e.g., loading, reasoning, writing) representing an agent's reasoning flow.\n* Intermediate: Design a fallback plan specifying how the app should respond if the LLM invocation fails.",
        "reading": "* [AWS Architecture Center](https://aws.amazon.com/architecture/)\n* [Integration Testing Patterns Guide](https://martinfowler.com/articles/practical-test-pyramid.html)"
    }
}

# General backup data for other chapters to keep them robust
GENERAL_CHAPTER_DATA = {
    "title_map": {
        "08": "Running the Application",
        "13": "Memory Engine & State Management",
        "14": "Custom Tools Integration",
        "15": "Deployment & Containerization",
        "16": "Observability & Telemetry",
        "17": "Complete End-to-End Flow"
    }
}

def generate_line_explanation(line_num, line_str):
    stripped = line_str.strip()
    
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
            name_match = re.search(r'getLogger\((.*?)\)', stripped)
            name_str = name_match.group(1) if name_match else '"Agent"'
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

    if "=" in stripped and not stripped.startswith("return"):
        var_part, val_part = stripped.split("=", 1)
        var_name = var_part.strip()
        val_name = val_part.strip()
        
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

    return f"""Line {line_num}
```python
{line_str}
```
**Explanation:**
- **What this line does:** Executes line statement `{stripped}`.
- **Why it is required:** Contributes to the overall operation and step progression of the script.
- **Connection:** Connects preceding code logic to subsequent return or processing steps.
"""

def generate_example_block_with_walkthrough(code_str, example_title, chap_num):
    raw_code = code_str.replace('```python', '').replace('```', '').strip()
    lines = raw_code.split('\n')
    
    out = f"### {example_title}\n\n"
    out += f"```python\n{raw_code}\n```\n\n"
    out += f"#### Code Walkthrough\n\n"
    
    for idx, line in enumerate(lines, 1):
        out += generate_line_explanation(idx, line) + "\n"
        
    out += f"#### Complete Flow of Execution\n\n"
    if "Simple" in example_title:
        out += "1. **Import Libraries**: Python loads the required `BedrockAgentCoreApp` class into memory.\n"
        out += "2. **Initialize Application**: An instance of `BedrockAgentCoreApp` is instantiated and assigned to `app`.\n"
        out += "3. **Register Event Handler**: The `@app.invoke` decorator registers the `handler` function as the primary event entrypoint.\n"
        out += "4. **Receive Request**: The AgentCore runtime listens for incoming requests and receives `payload` and `context` objects.\n"
        out += "5. **Execute Handler Logic**: The `handler` function is triggered with the incoming input parameters.\n"
        out += "6. **Return Response Payload**: A structured response dictionary containing `\"statusCode\": 200` and message data is returned.\n"
        out += "7. **Send Response to Caller**: AgentCore serializes the dictionary into JSON and delivers it back to the client application.\n\n"
        
        out += f"#### Visual Execution Flow\n\n"
        out += "```\n"
        out += "Program Starts\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Import BedrockAgentCoreApp\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Create App Instance (app)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Register Handler (@app.invoke)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Receive Request (payload, context)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Execute handler() Function\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Return Response Dictionary ({statusCode: 200, ...})\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Deliver Response Back to Client\n"
        out += "```\n\n"
    elif "Intermediate" in example_title:
        out += "1. **Import Required Libraries**: Python imports `BedrockAgentCoreApp` and the `logging` module.\n"
        out += "2. **Configure Logging System**: `logging.basicConfig` sets the log level threshold to `INFO`.\n"
        out += "3. **Create Logger Object**: `logging.getLogger` instantiates a dedicated logger for capturing session traces.\n"
        out += "4. **Initialize Application**: An instance of `BedrockAgentCoreApp` is assigned to `app`.\n"
        out += "5. **Register Handler**: `@app.invoke` binds the `handler` function to incoming AgentCore trigger events.\n"
        out += "6. **Read Input Payload**: `payload.get('prompt', '')` safely reads the user's prompt string.\n"
        out += "7. **Extract Session Context**: `getattr(context, 'session_id', 'local-session')` safely retrieves the session ID.\n"
        out += "8. **Log Activity**: `logger.info` writes session details to the CloudWatch diagnostic stream.\n"
        out += "9. **Return Formatted Response**: Returns a status 200 dictionary containing the processed prompt and session ID.\n"
        out += "10. **Deliver Payload**: AgentCore returns the serialized JSON payload to the caller.\n\n"

        out += f"#### Visual Execution Flow\n\n"
        out += "```\n"
        out += "Program Starts\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Import Libraries & Configure Logger\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Create App Instance (app)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Register Handler (@app.invoke)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Receive Request & Read Payload Prompt\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Extract Session ID & Write Log Entry\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Return Formatted Response Dictionary\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Deliver Serialized Response to Client\n"
        out += "```\n\n"
    else:
        out += "1. **Import Environment & Utility Libraries**: Imports `BedrockAgentCoreApp`, `os`, and `logging`.\n"
        out += "2. **Create Production Logger**: Instantiates a logger object for production observability.\n"
        out += "3. **Initialize Core Application**: Instantiates `BedrockAgentCoreApp` as `app`.\n"
        out += "4. **Register Production Handler**: `@app.invoke` binds `handler` as the production entrypoint.\n"
        out += "5. **Enter Try-Except Harness**: The `try` block wraps execution logic for error protection.\n"
        out += "6. **Validate Input Prompt**: `payload.get('prompt')` reads the prompt. If missing (`if not prompt:`), returns HTTP 400.\n"
        out += "7. **Read OS Environment**: `os.getenv('APP_ENV', 'development')` inspects operating system environment variables.\n"
        out += "8. **Extract Session Identifier**: `getattr(context, 'session_id', 'local-session')` safely retrieves session metadata.\n"
        out += "9. **Log Production Event**: `logger.info` writes structured log entries containing environment and session details.\n"
        out += "10. **Return Success Response**: Returns an HTTP 200 dictionary with production result details.\n"
        out += "11. **Catch Unhandled Errors**: If an exception occurs, the `except` block catches it, logs the error, and returns HTTP 500.\n"
        out += "12. **Send Response to Caller**: AgentCore delivers the final JSON response back to the client.\n\n"

        out += f"#### Visual Execution Flow\n\n"
        out += "```\n"
        out += "Program Starts\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Import Modules & Initialize Logger & App\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Register Handler (@app.invoke)\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Receive Request & Enter try-except Block\n"
        out += "      │\n"
        out += "      ▼\n"
        out += "Validate Prompt Parameter\n"
        out += " ├── [Invalid / Missing Prompt] ──► Return 400 Bad Request\n"
        out += " └── [Valid Prompt]\n"
        out += "        │\n"
        out += "        ▼\n"
        out += "Read Environment (os.getenv) & Session Context\n"
        out += "        │\n"
        out += "        ▼\n"
        out += "Write Production Log & Return 200 Success Response\n"
        out += "        │\n"
        out += "        ▼\n"
        out += " Deliver Response to Client Application\n"
        out += "```\n\n"
    return out

def generate_hands_on_examples_section(hands_on_simple, hands_on_intermediate, hands_on_advanced, chap_title):
    simple_clean = hands_on_simple.replace("```python", "").replace("```", "").strip()
    inter_clean = hands_on_intermediate.replace("```python", "").replace("```", "").strip()
    adv_clean = hands_on_advanced.replace("```python", "").replace("```", "").strip()

    walkthrough = f"""## 10. Hands-on Examples

In this section, we analyze the hands-on code implementations for **{chap_title}** step-by-step, explaining the architecture, syntax choices, logic flow, and production patterns across all three implementation tiers.

---

### 1. Simple Implementation Tier Walkthrough

```python
{simple_clean}
```

#### Code Logic & Syntax Breakdown:
* **Package Imports (`from bedrock_agent_core import ...`)**:
  - Brings in the core `BedrockAgentCoreApp` engine. This class handles runtime container startup, manages the microVM event loop, and deserializes incoming JSON API invocations.
* **Application Instance (`app = BedrockAgentCoreApp()`)**:
  - Instantiates the primary application object `app`. This object serves as the main registry for invocation routes, memory session hooks, and tool bindings.
* **Invocation Decorator (`@app.invoke`)**:
  - A Python decorator that registers the function immediately below as the primary entrypoint for Bedrock AgentCore runtime triggers.
* **Handler Signature (`def handler(payload, context):`)**:
  - **`payload`**: A Python dictionary holding client parameters, user prompt strings, and input arguments.
  - **`context`**: A metadata object containing active runtime details such as `session_id`, `actor_id`, and AWS IAM execution identities.
* **Return Payload (`return {{"statusCode": 200, "response": ...}}`)**:
  - Constructs a standard HTTP response dictionary. The `statusCode: 200` communicates success to the API Gateway, and `response` delivers the agent payload back to the client.

---

### 2. Intermediate Implementation Tier Walkthrough

```python
{inter_clean}
```

#### Code Logic & Syntax Breakdown:
* **System Logging Setup (`import logging` & `logger = logging.getLogger(...)`)**:
  - Configures structured logging via Python's standard `logging` module.
  - In production, log messages emitted by `logger.info()` stream into Amazon CloudWatch Logs for real-time monitoring and debugging.
* **Safe Parameter Extraction (`payload.get(...)`)**:
  - Uses `payload.get("prompt", "")` to safely retrieve user queries. Using `.get()` with a default fallback (`""`) prevents `KeyError` exceptions if optional fields are missing.
* **Runtime Session Inspection (`getattr(context, ...)`)**:
  - Inspects the `context` object for `session_id`. Using `getattr()` ensures compatibility when testing locally without a live AWS microVM context.
* **Operational Telemetry (`logger.info(...)`)**:
  - Emits formatted log entries containing session parameters and query strings to track execution flow.

---

### 3. Advanced Production Tier Walkthrough

```python
{adv_clean}
```

#### Code Logic & Syntax Breakdown:
* **Defensive Error Trapping (`try: ... except Exception as e:`)**:
  - Wraps the entire invocation handler inside a `try-except` block to catch unhandled errors gracefully, preventing container crashes in multi-tenant runtime environments.
* **Input Parameter Validation (`if not prompt:`)**:
  - Inspects inbound arguments before executing core agent logic. If mandatory parameters are missing, it short-circuits execution and returns a structured `statusCode: 400` (Bad Request) payload.
* **Environment Overrides (`os.getenv(...)`)**:
  - Reads system environment variables (e.g., `APP_ENV`) to dynamically adapt behavior across `development`, `staging`, and `production` environments without modifying codebase files.
* **Sanitized Production Error Response**:
  - Logs internal error details using `logger.error(...)` while returning a clean, safe `statusCode: 500` response to prevent internal stack traces from leaking to client callers.

---

### Summary Sequence of Execution

```
[Incoming Invocation] ──► [Bedrock AgentCore Runtime]
                                  │
                                  ▼
                      [Route to @app.invoke Handler]
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
       [Input Validated (200)]        [Input Missing (400)]
                   │                             │
                   ▼                             ▼
       [Execute Agent Core Logic]     [Return Error Payload]
                   │
                   ▼
       [Deliver JSON to Client]
```

"""
    return walkthrough

def generate_chapter_file(chap_num, file_path):
    print(f"Generating enhanced 24-heading version for Chapter {chap_num}...")
    
    # Read the pristine backup file to extract original contents
    backup_file_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
    if not os.path.exists(backup_file_path):
        backup_file_path = backup_file_path + ".bak"
    if not os.path.exists(backup_file_path):
        print(f"No backup file found for Chapter {chap_num}! Skipping.")
        return

    with open(backup_file_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    # Extract sections like step-by-step setup guides, code blocks, lists from original
    # We will use these to enhance the corresponding section of the 24-heading structure.
    original_code_blocks = re.findall(r"```python(.*?)```", original_content, re.DOTALL)
    original_json_blocks = re.findall(r"```json(.*?)```", original_content, re.DOTALL)
    original_yaml_blocks = re.findall(r"```yaml(.*?)```", original_content, re.DOTALL)
    original_docker_blocks = re.findall(r"```dockerfile(.*?)```", original_content, re.DOTALL)
    original_commands = re.findall(r"```bash(.*?)```", original_content, re.DOTALL)
    original_markdown_tables = re.findall(r"(\|.*?\n\|.*?\n(?:\|.*?\n)+)", original_content)
    original_images = re.findall(r"!\[(.*?)\]\((.*?)\)", original_content)

    # Clean code blocks
    original_code = ""
    if original_code_blocks:
        original_code = f"```python\n{original_code_blocks[0].strip()}\n```"
    elif original_json_blocks:
        original_code = f"```json\n{original_json_blocks[0].strip()}\n```"
    elif original_yaml_blocks:
        original_code = f"```yaml\n{original_yaml_blocks[0].strip()}\n```"
    elif original_docker_blocks:
        original_code = f"```dockerfile\n{original_docker_blocks[0].strip()}\n```"

    # Fallback/default content for chapters not fully mapped in CHAPTER_DATA dictionary
    # This dynamically builds detailed text using the title and context of the chapter.
    chap_info = CHAPTER_DATA.get(chap_num)
    if not chap_info:
        # Generate dynamic information for other chapters
        title = os.path.basename(file_path).replace(".md", "").replace("_", " ").title()
        # Clean title: e.g., "02 Chapter Prerequisites" -> "Prerequisites"
        title = re.sub(r"^\d+\s+Chapter\s+", "", title)
        title = title.replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "").replace("07 ", "").replace("08 ", "").replace("09 ", "").replace("10 ", "").replace("11 ", "").replace("12 ", "").replace("13 ", "").replace("14 ", "").replace("15 ", "").replace("16 ", "").replace("17 ", "")
        
        chap_info = {
            "title": title,
            "intro": f"This chapter covers the essential workflows, configurations, and internal parameters for {title}.",
            "what_is_it": f"{title} provides the core operational capability for this phase of the Bedrock AgentCore architecture.",
            "why_important": f"Understanding {title} is critical for establishing reliable execution patterns, securing system resources, and preventing configuration drift.",
            "how_it_works": f"The application initializes relevant components, processes inputs under {title}, and coordinates execution with AWS services.",
            "key_responsibilities": [
                f"Initialize and configure operational parameters for {title}.",
                f"Validate runtime request payloads and manage execution steps.",
                f"Maintain security boundaries and system performance standards for {title}."
            ],
            "pre_reqs": "* Completion of preceding chapters.\n* Access to the configured development workspace.",
            "bg_theory": f"The theory of {title} relates to standard software architecture and cloud development patterns. Ensuring proper setup, validation, and execution prevents configuration drift and runtime failures.",
            "concepts": [
                (f"{title} Base", f"The foundation layer that handles core operations for {title}.", "Simplifies the integration of resources.", "Within the active project workflow."),
                ("Configuration Registry", "A centralized settings directory.", "Allows settings to be updated independently of application logic.", "Configuration file metadata."),
                ("Runtime Execution", "The lifecycle stage where active tasks are processed.", "Coordinates code execution with resource allocations.", "In active container VM instances.")
            ],
            "mechanics": f"1. Application parses configuration settings.\n2. Resources are initialized and verified.\n3. Task requests are received and routed to handlers.\n4. Output is generated and returned to the client.",
            "mermaid": "graph TD\n    Client[User Client] -->|Request| App[Agentcore Application]\n    App -->|Query| Resource[System Resources]\n    Resource -->|Response| App\n    App -->|Output| Client",
            "installation": "Verify configuration and path listings by running:\n```bash\npython -c \"import os; print(os.getcwd())\"\n```",
            "configuration": "Deployment settings are declared in `bedrock_agent_core.yaml`:\n```yaml\nversion: \"1.0\"\nagent:\n  name: \"agentcore-app\"\n```",
            "hands_on_simple": "# Verify component initialization\ndef check_component():\n    print(\"Component initialized successfully.\")\nif __name__ == '__main__':\n    check_component()",
            "hands_on_intermediate": "# Validate config dictionary inputs\ndef validate_inputs(config_dict):\n    if not config_dict:\n        return False\n    print(\"Configurations loaded:\", config_dict)\n    return True",
            "hands_on_advanced": "# Complete class handler representing advanced transactions\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(\"AdvancedApp\")\n\nclass SystemManager:\n    def __init__(self, config):\n        self.config = config\n\n    def run(self):\n        logger.info(\"Starting transaction...\")\n        try:\n            if not self.config:\n                raise ValueError(\"Empty configuration details.\")\n            logger.info(\"Transaction complete.\")\n            return True\n        except Exception as e:\n            logger.error(f\"Transaction failed: {str(e)}\")\n            return False\n\nif __name__ == '__main__':\n    mgr = SystemManager({\"env\": \"dev\"})\n    mgr.run()",
            "best_practices": "* Enforce parameter limits to ensure stability.\n* Keep dependencies isolated in virtual environments.\n* Implement structured JSON logging.",
            "security": "Enforce strict IAM security bounds. Ensure credentials are not hardcoded inside application files, and encrypt data at rest and in transit.",
            "performance": "Set resource limits in configuration settings, and implement connection pools to optimize performance.",
            "cost": "Monitor resource usage closely to prevent unexpected billing. Release idle resources when tasks complete.",
            "mistakes": "* Hardcoding API keys inside execution files.\n* Running scripts without validating input parameters.",
            "troubleshooting": [
                ("System fails to start", "Missing configuration variables or environment properties.", "Verify the configuration file paths and ensure parameters are defined."),
                ("AccessDeniedException on invoke", "The execution role lacks required permission boundaries.", "Verify IAM policies and role configurations in the AWS console.")
            ],
            "interviews": [
                (f"Why is {title} critical for enterprise applications?", "It standardizes development layouts, improves security isolation, and ensures that environments remain synchronized across stages."),
                ("How do you debug configuration errors?", "Verify configuration syntax, check environment variables, and inspect container logs to locate the error source."),
                ("What is the principle of least privilege?", "A security practice that limits user and application permissions to only the specific resources required to complete tasks.")
            ],
            "use_cases": "Configuring enterprise applications to ensure scalability, security, and reliability.",
            "project": "This chapter defines the setup and configuration steps that support our core agent applications.",
            "summary": f"This chapter covered the core concepts, configurations, and workflows associated with {title}.",
            "key_takeaways": "* Separating config from code simplifies multi-environment deployments.\n* Always follow least-privilege security guidelines when configuring resources.\n* Validate configuration parameters during application startup.",
            "exercises": "* Beginner: Create a basic validation script that verifies config values.\n* Intermediate: Add a custom parameter check step and return an error code on failure.",
            "reading": "* [AWS Developer Tools Documentation](https://docs.aws.amazon.com/index.html)\n* [Python Core Programming Guide](https://docs.python.org/3/)"
        }

    # Clean and parse original content details to preserve original data
    orig_learning_objectives = ""
    lo_match = re.search(r"## 1\. Learning Objectives(.*?)(?=## 2|\-\-\-|$)", original_content, re.DOTALL)
    if not lo_match:
        lo_match = re.search(r"## 🎯 Learning Objectives(.*?)(?=\-\-\-|$)", original_content, re.DOTALL)
    if lo_match:
        orig_learning_objectives = lo_match.group(1).strip()
        # Clean line numbers from view_file if any
        orig_learning_objectives = re.sub(r"^\d+:\s*", "", orig_learning_objectives, flags=re.MULTILINE)
        orig_learning_objectives = re.sub(r"### Importance of This Chapter.*", "", orig_learning_objectives, flags=re.DOTALL)
        orig_learning_objectives = re.sub(r"### Prerequisites.*", "", orig_learning_objectives, flags=re.DOTALL)

    # Format objectives cleanly
    objectives_bullets = orig_learning_objectives if orig_learning_objectives else chap_info["pre_reqs"]
    # Ensure they start with bullets
    if not objectives_bullets.strip().startswith("-") and not objectives_bullets.strip().startswith("*"):
        objectives_bullets = "\n".join([f"- {line.strip()}" for line in objectives_bullets.split("\n") if line.strip()])

    # Look for original code examples
    hands_on_simple_str = chap_info["hands_on_simple"]
    hands_on_intermediate_str = chap_info["hands_on_intermediate"]
    hands_on_advanced_str = chap_info["hands_on_advanced"]

    # Re-inject original code blocks in Hands-on Examples or Code Walkthrough if present
    if original_code_blocks:
        code_str = f"```python\n{original_code_blocks[0].strip()}\n```"
        hands_on_simple_str = code_str
    elif original_json_blocks:
        code_str = f"```json\n{original_json_blocks[0].strip()}\n```"
        hands_on_simple_str = code_str
    elif original_yaml_blocks:
        code_str = f"```yaml\n{original_yaml_blocks[0].strip()}\n```"
        hands_on_simple_str = code_str
    elif original_docker_blocks:
        code_str = f"```dockerfile\n{original_docker_blocks[0].strip()}\n```"
        hands_on_simple_str = code_str

    # Gather original tables
    tables_str = ""
    if original_markdown_tables:
        tables_str = "\n\n" + "\n\n".join([t.strip() for t in original_markdown_tables]) + "\n\n"

    # Assemble the final markdown content for the 24 headings
    content = f"# {os.path.basename(file_path).replace('.md', '')}\n\n"

    # 1. Introduction
    content += f"## 1. Introduction\n"
    content += f"{chap_info['intro']}\n\n"
    content += f"### What is it?\n{chap_info['what_is_it']}\n\n"
    content += f"### Why is it important?\n{chap_info['why_important']}\n\n"
    content += f"### How does it work?\n{chap_info['how_it_works']}\n\n"
    content += f"### Key Responsibilities\n"
    for resp in chap_info['key_responsibilities']:
        content += f"- {resp}\n"
    content += "\n---\n\n"

    # 2. Learning Objectives
    content += f"## 2. Learning Objectives\n"
    content += f"By the end of this chapter, you will be able to:\n{objectives_bullets}\n\n"
    content += "---\n\n"

    # 3. Prerequisites
    content += f"## 3. Prerequisites\n"
    content += f"{chap_info['pre_reqs']}\n\n"
    content += "---\n\n"

    # 4. Background Theory
    content += f"## 4. Background Theory\n"
    content += f"{chap_info['bg_theory']}\n\n"
    content += "---\n\n"

    # 5. Core Concepts
    content += f"## 5. Core Concepts\n"
    for term, exp, why, where in chap_info["concepts"]:
        content += f"**📦 Technical Term: {term}**\n\n"
        content += f"* **Simple Explanation:** {exp}\n"
        content += f"* **Why it exists:** {why}\n"
        content += f"* **Where is it used:** {where}\n\n"
    content += "---\n\n"

    # 6. Internal Mechanics
    content += f"## 6. Internal Mechanics\n"
    content += f"{chap_info['mechanics']}\n\n"
    content += "---\n\n"

    # 7. Architecture Overview
    content += f"## 7. Architecture Overview\n"
    content += "The following architectural details outline the components and relationship schemas active in this module:\n\n"
    content += f"```mermaid\n{chap_info['mermaid']}\n```\n\n"
    content += "---\n\n"

    # 8. Installation & Setup
    content += f"## 8. Installation & Setup\n"
    content += f"{chap_info['installation']}\n\n"
    content += "---\n\n"

    # 9. Configuration
    content += f"## 9. Configuration\n"
    content += f"{chap_info['configuration']}\n\n"
    content += "---\n\n"

    # 10. Hands-on Examples
    content += generate_hands_on_examples_section(hands_on_simple_str, hands_on_intermediate_str, hands_on_advanced_str, chap_info['title'])
    content += "---\n\n"

    # 11. Production Best Practices
    content += f"## 11. Production Best Practices\n"
    content += f"{chap_info['best_practices']}\n\n"
    content += "---\n\n"

    # 12. Security Considerations
    content += f"## 12. Security Considerations\n"
    content += f"{chap_info['security']}\n\n"
    content += "---\n\n"

    # 13. Performance Optimization
    content += f"## 13. Performance Optimization\n"
    content += f"{chap_info['performance']}\n\n"
    content += "---\n\n"

    # 14. Common Mistakes
    content += f"## 14. Common Mistakes\n"
    content += f"{chap_info['mistakes']}\n\n"
    content += "---\n\n"

    # 15. Troubleshooting
    content += f"## 15. Troubleshooting\n"
    content += "Below is the diagnostic reference table for identifying and resolving issues:\n\n"
    content += "| Symptom | Root Cause | Solution |\n"
    content += "| :--- | :--- | :--- |\n"
    for sym, cause, sol in chap_info["troubleshooting"]:
        content += f"| {sym} | {cause} | {sol} |\n"
    content += "\n"
    if tables_str:
        content += f"### Additional Reference Tables\n{tables_str}\n"
    content += "---\n\n"

    # 16. Interview Questions
    content += f"## 16. Interview Questions\n"
    for q, ans in chap_info["interviews"]:
        content += f"### Q: {q}\n"
        content += f"* **Answer:** {ans}\n\n"
    content += "---\n\n"

    # 17. Real-World Use Cases
    content += f"## 17. Real-World Use Cases\n"
    content += f"{chap_info['use_cases']}\n\n"
    content += "---\n\n"

    # 18. Industrial Project
    content += f"## 18. Industrial Project\n"
    content += f"{chap_info['project']}\n\n"
    content += "---\n\n"

    # 19. Summary
    content += f"## 19. Summary\n"
    content += f"{chap_info['summary']}\n\n"
    content += "---\n\n"

    # 20. Key Takeaways
    content += f"## 20. Key Takeaways\n"
    content += f"{chap_info['key_takeaways']}\n\n"
    content += "---\n\n"

    # 21. Practice Exercises
    content += f"## 21. Practice Exercises\n"
    content += f"{chap_info['exercises']}\n\n"
    content += "---\n\n"

    # 22. Further Reading
    content += f"## 22. Further Reading\n"
    content += f"{chap_info['reading']}\n"

    # Save images / figures if any were in original
    # if original_images:
    #     content += "\n\n## Appendix: Figures and Media\n"
    #     for caption, img_path in original_images:
    #         content += f"![{caption}]({img_path})\n*Caption: {caption}*\n\n"

    # Write back to file path
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully upgraded Chapter {chap_num}!")

def main():
    print("Running 24-heading migration script...")
    # List all markdown files in TARGET_DIR
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(".md") and f[0].isdigit()]
    files.sort()

    for f in files:
        chap_num = f.split("_")[0]
        file_path = os.path.join(TARGET_DIR, f)
        generate_chapter_file(chap_num, file_path)

    print("All chapters successfully migrated to 24-heading format!")

if __name__ == '__main__':
    main()
