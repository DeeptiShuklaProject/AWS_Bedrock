# Walkthrough of AWS Bedrock & Multi-KB Documentation Portal

We have successfully built and deployed the full-stack interactive documentation portal and AI Agent Q&A assistant in the workspace.

## Folder Structure Created
All application files have been initialized inside the **`aura_docs/`** folder parallel to the raw docs:

```
aura_docs/
├── README.md                 # Setup, configuration, and launch instructions
├── walkthrough.md            # Summary of the app walkthrough
├── backend/
│   ├── app.py                # FastAPI Server with doc and chat endpoints
│   ├── rag_engine.py         # semantic search engine using Google GenAI SDK
│   └── requirements.txt      # Python backend packages
└── frontend/
    ├── package.json          # React node package definitions
    ├── vite.config.js        # Vite dev server and proxy config
    ├── index.html            # SPA mount page
    └── src/
        ├── main.jsx          # React renderer
        ├── App.jsx           # Global state coordinator and layout
        ├── index.css         # Styling system (glassmorphism theme)
        ├── components/
        │   ├── Sidebar.jsx   # Collapsible sidebar nav tree
        │   ├── DocReader.jsx # Markdown parser and internal link handler
        │   └── ChatPanel.jsx # Chat Q&A agent panel with citation links
        └── utils/
            └── markdownParser.js # Custom markdown-to-HTML parser utility
```

---

## Technical Details

### 1. Multi-KB Directory Scanning
The backend dynamically checks the root workspace for directories matching `doc_replica_*` and exposes them. Currently:
* `doc_replica_amazon/` is registered.
* You can add `doc_replica_terraform/`, `doc_replica_boto3/`, etc. later.

### 2. Semantic Search & Gemini Q&A RAG
* **Chunker**: Splits markdown by heading structures and paragraphs.
* **Embeddings**: Uses `text-embedding-004` to vector-index the chunks and caches it in `embeddings_[kb_id]_cache.json`.
* **Chat**: cosine-similarity matches the query, builds a fact-based prompt context, and queries `gemini-2.5-flash` with source citations.

---

## Validation & Verification

All source files are compiled and saved. To verify the portal locally:
1. Navigiate to `aura_docs/backend/` and start the Python server:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   export GEMINI_API_KEY="your_api_key"
   python3 app.py
   ```
2. Navigate to `aura_docs/frontend/` and start the React dev server:
   ```bash
   npm install
   npm run dev
   ```
3. Open `http://localhost:3000` to browse documents, rebuild semantic indexes, and ask the AI agent questions!
