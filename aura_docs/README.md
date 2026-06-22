# AuraDocs: Knowledge Base Documentation Portal & AI Agent

This folder contains the complete interactive full-stack web application designed to serve local markdown files as a responsive HTML document portal, coupled with a Retrieval-Augmented Generation (RAG) AI Chat Agent powered by Gemini.

## Features
* **Multi-KB Support**: Dynamically detects any directories matching `doc_replica_*` in the workspace root and loads them as selectable Knowledge Bases.
* **collapsible Folder Tree**: An interactive navigation sidebar mirroring the document structure.
* **SPA-like Document Navigation**: Click internal document links without page reloads.
* **AI Chat Assistant Panel**: Talk to an AI Agent that answers questions using the selected KB as context and provides clickable source citations.
* **Zinc Design Theme**: A premium dark-mode styled glassmorphism user interface.

---

## Getting Started

### Prerequisites
1. **Node.js** (v18+) and **NPM** installed.
2. **Python** (v3.8+) installed.
3. A **Gemini API Key** from Google AI Studio.

### Step 1: Set up the Backend
1. Open your terminal and navigate to the backend folder:
   ```bash
   cd aura_docs/backend
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your Gemini API Key environment variable:
   * **macOS / Linux**:
     ```bash
     export GEMINI_API_KEY="your-api-key-here"
     ```
   * **Windows (Command Prompt)**:
     ```cmd
     set GEMINI_API_KEY="your-api-key-here"
     ```
   * **Windows (PowerShell)**:
     ```powershell
     $env:GEMINI_API_KEY="your-api-key-here"
     ```
5. Start the FastAPI server:
   ```bash
   python3 app.py
   ```
   *The backend will run on [http://localhost:8000](http://localhost:8000).*

### Step 2: Set up the Frontend
1. Open a new terminal window and navigate to the frontend folder:
   ```bash
   cd aura_docs/frontend
   ```
2. Install the packages:
   ```bash
   npm install
   ```
3. Start the Vite dev server:
   ```bash
   npm run dev
   ```
   *The frontend portal will open on [http://localhost:3000](http://localhost:3000).*

---

## How to Add New Knowledge Bases (for Different Clients)

The system is designed to be **100% plug-and-play**. To add a new learning topic or client guide:

1. **Create a new folder** at the root of the workspace matching the format `doc_replica_[kb_name]`. For example:
   * `doc_replica_terraform/`
   * `doc_replica_boto3/`
   * `doc_replica_client_x/`
2. **Add your markdown (`.md`) files** inside this new folder. You can organize them into nested folders.
3. **Select it in the dropdown**: When you refresh the web portal, the top-bar dropdown selector will dynamically display the new option (e.g. "Client X").
4. **Re-index for Q&A**: Select the new KB from the dropdown and click the **"Index KB"** button at the top. The backend will parse the files, generate semantic embeddings, and cache them. 
5. **Q&A Enabled**: The AI assistant will immediately begin answering questions specifically using your new client's documentation!
