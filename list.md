# Completed Work & Project Index

This file tracks all modifications and components built across the workspaces as of June 19, 2026.

---

## 1. AuraDocs: AWS Bedrock Interactive Documentation Portal (`wscs_bedrock/`)

A full-stack, local-first React + Python FastAPI documentation viewer and RAG AI Q&A Agent.

* **Docker Compose Orchestrator**: [docker-compose.yml](file:///Users/nishantsaxena/workspace/wscs_bedrock/docker-compose.yml) (Enables building and running both backend and frontend services inside Docker containers with local volume mounting).

### A. Raw Documentation Replicas
* **Nishu @Work**:
  * Folder: [doc_replica_notes/](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_notes/) (This folder is prioritized and loaded by default on portal startup. Write your personal `.md` notes here).
* **AWS Bedrock User Guide**:
  * Downloader Script: [download_docs.py](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_amazon/download_docs.py)
  * Output Folder: [doc_replica_amazon/](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_amazon/)
  * **Mechanism**: The downloader script fetches the official `toc-contents.json` (available at `https://docs.aws.amazon.com/bedrock/latest/userguide/toc-contents.json`) from Amazon's servers. It parses this JSON to extract the entire Table of Contents (TOC) structure, then systematically crawls and downloads each page as a `.md` file, creating a perfect local replica of 1,058 markdown files mapped according to the official TOC hierarchy.

### B. Backend API Service (`aura_docs/backend/`)
* **API Application**: [app.py](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/backend/app.py)
  * Automatically scans for any folder named `doc_replica_*` in the workspace root.
  * Dynamically generates table-of-contents trees from Sphinx files or falls back to walking the filesystem directories.
  * Exposes document contents and handles RAG chat endpoint routing.
* **Semantic Search / RAG Engine**: [rag_engine.py](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/backend/rag_engine.py)
  * Groups and chunks markdown documents.
  * Interacts with the Google GenAI SDK (`text-embedding-004`) to compile and cache vector search mappings locally.
  * Prompts `gemini-2.5-flash` with the matching text snippets to generate answers constrained strictly to local documentation context.
* **Dependencies List**: [requirements.txt](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/backend/requirements.txt) (FastAPI, Uvicorn, Google GenAI SDK).

### C. Frontend Interface SPA (`aura_docs/frontend/`)
* **React App Entry**: [main.jsx](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/main.jsx) and [App.jsx](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/App.jsx) (Handles state coordination for active Knowledge Base, active document, and chat history).
* **Collapsible Nav Tree**: [Sidebar.jsx](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/components/Sidebar.jsx) (Hierarchical tree viewer supporting nested folders and index pages).
* **Document Viewer**: [DocReader.jsx](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/components/DocReader.jsx) (Markdown parser and HTML renderer with internal linking).
* **Q&A Agent Panel**: [ChatPanel.jsx](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/components/ChatPanel.jsx) (Interface for running natural language queries, rendering markdown answers, and listing clickable source file links).
* **Vite Config & Dev Server**: [vite.config.js](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/vite.config.js) (Configured to proxy `/api` calls to the local FastAPI port).
* **CSS Theme System**: [index.css](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/frontend/src/index.css) (Custom CSS featuring Catppuccin Mocha colors, glassmorphism, custom scrollbars, and micro-animations).

---

## 2. Antigravity Clicker (`wscs_ai/`)

Mac-native auto-clicker app using Vision framework OCR.

* **Vision Coordinate Calculator**: [clicker_engine.py](file:///Users/nishantsaxena/workspace/wscs_ai/antigravity_clicker/clicker_engine.py)
  * Replaced full-line clicking coordinates with word-level calculations via PyObjC `boundingBoxForRange_error_` to fix misalignment (such as clicking to the right of "Submit").
  * Added `"Submit"` to the default target words list.
* **Tkinter GUI Dashboard**: [clicker_app.py](file:///Users/nishantsaxena/workspace/wscs_ai/antigravity_clicker/clicker_app.py)
  * Added `"Submit"` to the GUI startup variables and fallback configuration loader.
* **Headless CLI App**: [clicker_cli.py](file:///Users/nishantsaxena/workspace/wscs_ai/antigravity_clicker/clicker_cli.py)
  * Added `"Submit"` to the `--targets` argument parser defaults.

---

## 3. AuraDocs Architecture

AuraDocs is a **database-free (by default), local-first interactive runtime environment** that joins raw documentation with live code testing.

### A. Local-First & Serverless Database Layout
* **No Database Server**: The application does not require a SQL/NoSQL database server by default. The raw folder trees of markdown (`.md`) files on your hard drive serve directly as the primary data store. (Note: A database will be added in the future, for example, when migrating to a multi-user system).
* **Vector Search Cache**: For RAG search, the backend computes embeddings via the Google GenAI SDK and caches them in a single local JSON file per Knowledge Base:
  `aura_docs/backend/embeddings_[kb_id]_cache.json`
  This enables rapid semantic queries and offline functionality.

### B. Hybrid Rendering ("Two Worlds")
* **Standard Markdown**: The text is parsed to HTML in the frontend using a customized regex parser to maintain compatibility and render elements like headers, lists, code highlight blocks, and tables.
* **Dynamic React Widgets**: The `DocReader.jsx` component splits the document text at custom widget delimiters:
  ` ```widget:[widget-type] `
  ` [JSON Configuration / Code Snippet] `
  ` ``` `
  It parses the data within these delimiters and replaces the static block with fully interactive React components (`ModelParamTesterWidget`, `ApiPlaygroundWidget`, `CodePlaygroundWidget`) in-place.

### C. Local Execution & AWS API Calling
* **Local Code Playground**: When you run Python code in the interactive console, the frontend sends the snippet to the backend (`/api/playground/run-code`). The backend executes the script inside the developer's local environment, redirects `sys.stdout` and `sys.stderr`, and returns the stdout outputs to the console view.
* **AWS Bedrock Integration**: The local backend uses the python `boto3` library to interface with your AWS credentials. When you invoke model queries in the playground, it automatically authenticates using your local `~/.aws` profile credentials and sends the requests directly to Bedrock.

### D. Self-Documenting Agent Skills
* **Autonomous Onboarding**: Future AI agents accessing this repository are guided by the root [README.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/README.md) and [list.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/list.md) to understand the codebase.
* **Orchestration**: The [run.sh](file:///Users/nishantsaxena/workspace/wscs_bedrock/run.sh) and [docker-compose.yml](file:///Users/nishantsaxena/workspace/wscs_bedrock/docker-compose.yml) files act as a runnable blueprint that any agent or developer can use to spin up the portal instantly on any machine.

