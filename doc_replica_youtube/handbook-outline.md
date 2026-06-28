# 34-Topic Syllabus & Transcript Directory

This directory maps all 34 handbook sections to their core concepts and video lessons.

---

## Part 1: Bedrock Foundations

| Topic ID | Topic Name | Description | Key Focus Area |
|----------|------------|-------------|----------------|
| **1** | Introduction to Serverless AI | Bedrock serverless value prop, unified API, regional setup. | Infrastructure |
| **2** | Navigating the Model Playground | AWS web console overview, system prompts, playground parameters. | Interactive testing |
| **3** | Controlling Persona via System Prompts | Setting guardrails, boundaries, rules, and tones using prompts. | Prompt Engineering |
| **4** | Programmatic Inference (Converse API) | Invoking models using Python (`boto3`) and Converse API. | API Invocation |
| **5** | Inference Configurations | Adjusting parameters (Temperature, Max Tokens, topP). | Generation Tuning |
| **6** | State in Multi-Turn Conversations | Handling conversation history arrays in a stateless API environment. | State Management |
| **7** | Tokens & Cost Optimization | Calculating input/output tokens, optimizing pricing strategy. | Cost Management |
| **8** | Tool Use (Function Calling) Concept | Theoretical workflow of executing local code on behalf of the model. | Extensibility |
| **9** | Implementing Tool Schemas | Writing JSON parameter schemas for the model to parse. | Data Schemas |
| **10** | Orchestrating the Tool Call Loop | Handling two-step invocation cycles in Python. | Integration Loops |
| **11** | Tool Use (Function Calling) Practice | End-to-end coding script using Converse API and mock tool execution. | Practical Coding |
| **12** | Advanced: Multi-Tool Routing | Giving the model multiple choices of tools and checking selections. | Routing Logic |
| **13** | Text Embeddings & Vectors | Converting language to vector dimensions via embedding models. | Vector Embeddings |
| **14** | Ingesting Documents (Chunking & Storing) | Preprocessing files, dividing text, storing vectors. | Ingestion Pipeline |
| **15** | Semantic Search & Document Retrieval | Searching vectors to feed relevant context back to prompts. | Retrieval (RAG) |
| **16** | RAG (Retrieval-Augmented Gen) Flow | Full retrieval-generation loop to answer questions from PDFs. | RAG |
| **17** | Introduction to Bedrock Guardrails | Understanding Guardrails, block policies, and compliance filters. | Safety |
| **18** | Filtering Content & PII Data | Masking personal info and detecting harmful input/output categories. | Security |
| **19** | Custom Deny Lists | Defining custom keyword blocklists to prevent model leaks. | Compliance |
| **20** | Testing Guardrails Programmatically | Invoking Guardrails using `boto3` parameters in Converse API. | Safety Testing |
| **21** | Introduction to Bedrock Agents | Multi-step agent concepts, planning loops, automated execution. | Agents |
| **22** | Registering Agent Knowledge Bases | Linking RAG sources directly to autonomous agent nodes. | Agent Search |
| **23** | Creating Agent Action Groups | Binding tool APIs to the agent planning controller. | Agent Actions |
| **24** | Building & Deploying Agents | Compiling and publishing agent configurations. | Orchestration |

---

## Part 2: Bedrock Agent Core

| Topic ID | Topic Name | Description | Key Focus Area |
|----------|------------|-------------|----------------|
| **25** | Introduction to Agent Core Runtime | Understanding the orchestrator state machine. | Agent Runtime |
| **26** | Agent Memory & State Persistent Storage | Retaining multi-turn variables across multiple sessions. | Persistence |
| **27** | Customizing Prompt Templates | Overriding pre-processing, orchestration, and post-processing steps. | Template Overrides |
| **28** | Integrating APIs & Action Groups | Binding OpenAPI specifications to Lambda routing targets. | Action Groups |
| **29** | Agent Observability & Trace Details | Extracting logic traces, reasoning steps, and logs. | Tracing |
| **30** | Identity & Access Policies | Creating secure IAM policies for Agent executions. | Authorization |
| **31** | Agent Gateway Implementations | Designing API entry points to trigger agent sessions. | Network Access |
| **32** | Model Benchmarking & Evaluations | Quantifying performance outputs on validation data. | Quality Control |
| **33** | Compliance & System Policies | Setting enterprise security gates on production agents. | Policies |
| **34** | Local Testing & Playground Console | Running interactive dry-runs in the AWS console. | Local Validation |

---

## Access & Links
- **Video Course Link**: [AWS Bedrock & Agent Core Course (YouTube)](https://www.youtube.com/watch?v=y1slHK9R_Vg)
- **Local Handbook Index**: [data.js](file:///c:/Users/nishu/workspace/sample_notes_bedrock_aws/data.js) contains the exact definitions and implementation examples for these 34 skills.
