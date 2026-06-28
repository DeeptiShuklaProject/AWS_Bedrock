# YouTube Course Transcripts & Portions Guide

This document provides a detailed breakdown of the structured JSON database used by our video transcript player and future AI agents. It describes the transcript schema and explains every portion of the AWS Bedrock developers courses.

---

## 1. Standardized Transcript JSON Schema

Each course video in the `doc_replica_youtube/` directory is accompanied by a `transcript.json` database. This structured format enables timeline synchronization in the UI and feeds context to search agents.

### Schema Fields
- `video_url` (string): The YouTube URL of the course.
- `title` (string): The title of the developer class.
- `duration` (string): Overall duration of the lesson.
- `timeline` (array): List of segments containing:
  - `timestamp` (string): Human-readable time (`HH:MM:SS` or `MM:SS`).
  - `seconds` (integer): Cumulative seconds for seeking in the player.
  - `label` (string): Section title.
  - `text` (string): Detailed summary of what is taught in this segment.

```json
{
  "video_url": "https://www.youtube.com/...",
  "title": "Video Title",
  "duration": "Duration",
  "timeline": [
    {
      "timestamp": "0:00:00",
      "seconds": 0,
      "label": "Section Title",
      "text": "Detailed transcript description..."
    }
  ]
}
```

---

## 2. Video 1: Amazon Bedrock & Agent Core Developer Course (4 Hours)
**URL:** [https://www.youtube.com/watch?v=y1slHK9R_Vg](https://www.youtube.com/watch?v=y1slHK9R_Vg)

### Course Portions Breakdown

#### 0:00:00 - Introduction to Serverless AI
- **Concepts:** Serverless infrastructure vs. self-hosting.
- **Details:** Explains the regional AWS setup for Amazon Bedrock and the core benefits of a serverless API model: on-demand scaling, no hardware management, and pay-per-token pricing.
- **Takeaway:** Bedrock acts as a unified hub hosting foundation models from major AI providers (Anthropic, Meta, Cohere, Amazon) under a single security envelope.

#### 0:15:30 - Navigating the Playground
- **Concepts:** AWS Console, prompt testing, playgrounds.
- **Details:** Walks through the AWS Bedrock Console. Shows how to request model access, launch the Chat/Text/Image playgrounds, and manually interact with models like Claude 3.5 Sonnet and Llama 3.
- **Takeaway:** Playgrounds are essential for fast prompt prototyping and checking model parameters (e.g. system instructions) before writing Python code.

#### 0:32:00 - Controlling Personas (System Prompts)
- **Concepts:** Prompt engineering, system instructions, guardrails.
- **Details:** Demonstrates how system prompts define the AI's persona, capabilities, boundaries, and formatting output styles.
- **Takeaway:** A well-structured system prompt prevents prompt injection, secures response output, and keeps the model focused on business guidelines.

#### 0:50:15 - Programmatic Inference with Converse API
- **Concepts:** Python `boto3` SDK, Converse API.
- **Details:** Explains how to move from playgrounds to code. Teaches the unified `converse` endpoint structure which replaced model-specific payloads.
- **Code Snippet:**
  ```python
  import boto3
  
  bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
  
  response = bedrock.converse(
      modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
      messages=[{"role": "user", "content": [{"text": "Hello!"}]}],
      system=[{"text": "You are a professional assistant."}]
  )
  print(response['output']['message']['content'][0]['text'])
  ```

#### 1:10:00 - Inference Configurations (Temperature & Tokens)
- **Concepts:** Temperature, topP, maxTokens.
- **Details:** Adjusting model creativity and output lengths. A low temperature (e.g. `0.0` or `0.1`) makes output deterministic (best for coding/data mapping), while higher values increase randomness and creativity.
- **Takeaway:** Tuning these configurations is key to managing cost (preventing run-away token generation) and output consistency.

#### 1:28:45 - State in Multi-Turn Chats
- **Concepts:** Stateless REST APIs, chat history state.
- **Details:** Because Bedrock endpoints are stateless, developers must manually keep track of the conversation history. Shows how to append incoming user queries and assistant responses to a running list and pass the list on every API call.
- **Takeaway:** Managing memory requires cleaning or sliding windows to avoid exceeding the context window limit.

#### 1:45:00 - Tokens & Billing Optimization
- **Concepts:** Pricing models, billing optimization.
- **Details:** How to read input and output token counts from the Converse API response metadata. Discusses pricing and token-reduction techniques (like summarizing context or dropping old messages).
- **Takeaway:** Pruning the chat history array prevents compounding costs during long conversations.

#### 2:02:10 - Tool Use (Function Calling)
- **Concepts:** External API integrations, JSON Schemas.
- **Details:** Connects LLMs to local databases or APIs. Teaches how to write parameter schemas in JSON, pass them to the model, parse the model's request to run a tool, execute the function locally, and return the result back to the model.
- **Takeaway:** The model does *not* run the tool itself; it generates the parameters. The developer's runtime is responsible for executing the function and feeding the result back.

#### 2:40:00 - Vector Embeddings & RAG Ingestion
- **Concepts:** Embedding models, vector similarity.
- **Details:** Ingesting unstructured documentation. Explains how text chunking works, generating embeddings using `amazon.titan-embed-text-v2`, and loading them into vector databases.
- **Takeaway:** Embeddings map words into high-dimensional space so semantic similarity can be computed using mathematical methods (e.g. cosine distance).

#### 3:15:30 - Bedrock Guardrails & PII Masking
- **Concepts:** Data protection, content filtering.
- **Details:** Setting up enterprise guardrails to block harmful inputs/outputs and mask sensitive data (SSNs, Phone Numbers, Credit Cards) before it reaches the model or client.
- **Takeaway:** Guardrails run independently of the model, adding a policy compliance layer.

#### 3:40:00 - Bedrock Agent Architectures
- **Concepts:** AI Agents, autonomous orchestration.
- **Details:** Outlines the design of fully autonomous agents that plan, reason, and take action dynamically utilizing action groups (Lambda integrations) and knowledge bases.
- **Takeaway:** Agents use a ReAct (Reasoning and Acting) loop to break down user requests into discrete plan items.

#### 4:00:00 - Bedrock Agent Core
- **Concepts:** Agent Runtime, memory persistence, IAM policies.
- **Details:** Investigates agent trace logs to inspect reasoning steps (pre-processing, orchestration, post-processing). Reviews the session security requirements and IAM role definitions.
- **Takeaway:** Setting up granular IAM permissions is critical to ensure agents can only read/write authorized resources.

---

## 3. Video 2: AWS Bedrock Converse API Deep Dive (45 Minutes)
**URL:** [https://www.youtube.com/watch?v=y1slHK9R_Vg](https://www.youtube.com/watch?v=y1slHK9R_Vg)

### Course Portions Breakdown

#### 0:00 - Introduction
- **Concepts:** Unified Converse API.
- **Details:** Explains the transition from legacy model-specific `invoke_model` payloads to the new `converse` and `converse_stream` schemas.
- **Takeaway:** The Converse API standardizes the message payload structure for all major models on Bedrock.

#### 7:30 - Converse Payload Details
- **Concepts:** Input structuring, system prompts.
- **Details:** Deep dive into structuring system prompts arrays, system lists, message blocks, and the `inferenceConfig` settings block.
- **Takeaway:** Correct message schemas prevent parsing errors when switching foundation models.

#### 18:15 - Streaming Mode Implementation
- **Concepts:** Token streaming, async generators.
- **Details:** Consuming the `converse_stream` endpoint in Python. Reads token chunks in real time as they are generated, improving user experience by reducing perceived latency.
- **Code Snippet:**
  ```python
  response = bedrock.converse_stream(
      modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
      messages=[{"role": "user", "content": [{"text": "Write a long essay."}]}]
  )
  for event in response['stream']:
      if 'contentBlockDelta' in event:
          print(event['contentBlockDelta']['delta']['text'], end='', flush=True)
  ```

#### 30:00 - Multi-Model Benchmarks
- **Concepts:** Speed, cost, latency comparisons.
- **Details:** Comparing response latency and quality between Claude 3.5 Sonnet, Claude 3 Haiku, and Amazon Nova Lite.
- **Takeaway:** Choose Haiku/Nova Lite for fast, cheap conversational tasks; use Sonnet for complex reasoning, tool use, and code generation.

#### 40:20 - Summary & Best Practices
- **Concepts:** Exception handling, throttling.
- **Details:** Handling AWS API rate limits (throttling) using exponential backoff and retry decorators.
- **Takeaway:** Implement error handlers for `ValidationException` and `LimitExceededException` to build stable software.

---

## 4. Video 3: Building RAG & Vector Search on AWS Bedrock (1 Hour)
**URL:** [https://www.youtube.com/watch?v=y1slHK9R_Vg](https://www.youtube.com/watch?v=y1slHK9R_Vg)

### Course Portions Breakdown

#### 0:00 - RAG Core Architectures
- **Concepts:** Retrieval-Augmented Generation.
- **Details:** Why RAG is preferred over fine-tuning for domain knowledge. RAG injects dynamic, verifiable context from documents directly into the prompt.
- **Takeaway:** RAG prevents LLM hallucinations by forcing the model to cite its sources from retrieved documents.

#### 12:15 - Vector Embeddings Generation
- **Concepts:** Numerical embeddings, vector space.
- **Details:** Using `amazon.titan-embed-text-v2` to convert text segments into 1536-dimension float arrays.
- **Takeaway:** Higher dimensions capture deeper semantic relationships but increase storage and search costs.

#### 25:40 - Ingestion & Chunking Pipelines
- **Concepts:** Text splitting, overlap windowing.
- **Details:** Creating recursive character chunking routines in Python. Splitting documents into overlapping windows (e.g. 500 characters with 100 character overlap) to preserve context.
- **Takeaway:** Smart chunking is crucial: too small loses context, too large dilutes similarity matches.

#### 40:00 - Vector Similarity Search
- **Concepts:** Cosine similarity, Top-K.
- **Details:** Querying the database. Converts the user search question into an embedding and performs a vector distance calculation to return the top K relevant chunks.
- **Takeaway:** Combining keyword search (lexical) with vector search (semantic) produces the most accurate results.

#### 52:10 - Context Injection & Synthesis
- **Concepts:** Context assembling, source citation.
- **Details:** Building the final prompt. Wraps the user question with the retrieved chunks and formats system guidelines instructing the model to answer *only* from the context.
- **Takeaway:** Clearly formatting retrieved sources in the prompt structure improves answer quality.
