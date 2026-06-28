# AuraDocs — AI Assistant Communication Log

> **Purpose:** This file is a shared conversation log between AI assistants working on this project.
> When starting a new session, **read this file first** to understand what has been done and follow the same conventions.

---

## From Claude @ 2026-06-28T01:03-04:00:

### What This Project Is

**AuraDocs** is a local-first documentation portal with an AI chat assistant. It reads markdown files from `doc_replica_*` folders and renders them in a web UI. There are two sub-projects:

1. **AuraDocs Portal** (`aura_docs/`) — Full-stack React + FastAPI app
2. **Bedrock Developer Handbook** (`sample_notes_bedrock_aws/`) — Standalone HTML/JS handbook built from official AWS docs, study notes, and YouTube tutorial transcripts

### Architecture

```
wscs_bedrock/
├── doc_replica_amazon/          # KB: AWS Bedrock official docs (markdown)
├── doc_replica_notes/           # KB: Personal study notes (markdown)
├── aura_docs/                   # The AuraDocs web app
│   ├── backend/
│   │   ├── app.py               # FastAPI server (serves docs, chat, playground)
│   │   ├── rag_engine.py        # Gemini-powered RAG semantic search
│   │   └── requirements.txt     # Python deps
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx           # Main layout (KB selector, routing)
│       │   ├── components/
│       │   │   ├── Sidebar.jsx   # Collapsible nav tree
│       │   │   ├── DocReader.jsx # Markdown renderer + interactive widgets
│       │   │   └── ChatPanel.jsx # AI Q&A chat panel
│       │   ├── utils/
│       │   │   └── markdownParser.js  # Custom regex-based markdown→HTML parser
│       │   └── index.css         # Full design system (themes, glassmorphism)
│       ├── vite.config.js        # Vite config with proxy to backend:8000
│       └── package.json
├── docker-compose.yml            # Docker orchestration (needs path fix for Windows)
├── talk.md                       # THIS FILE — AI communication log
└── README.md                     # Project overview
```

### Key Conventions

#### Backend (`aura_docs/backend/`)
- **WORKSPACE_DIR**: Set via env var or defaults to grandparent of `app.py`. This is the root directory scanned for `doc_replica_*` folders.
- **KB Discovery**: Auto-detects any `doc_replica_*` folder in WORKSPACE_DIR. No config needed.
- **KB Name Mapping** (app.py line ~30):
  ```python
  mapping = {
      "notes": "Nishu @Work",
      "amazon": "AWS Bedrock User Guide",
      "terraform": "Terraform AWS Provider",
      "boto3": "Boto3 (Python SDK) Docs",
      "general": "General Bedrock Skills"
  }
  ```
  Unmapped folders get auto-titled from their suffix.
- **Navigation**: First tries `toc-contents.json` in the KB folder, then falls back to filesystem walking.
- **Document resolution**: Handles `.html` → `.md` fallback, and recursive search for flat TOC references pointing to nested files.
- **RAG**: Uses Google GenAI SDK (`text-embedding-004` for embeddings, `gemini-2.5-flash` for generation). Needs `GEMINI_API_KEY` env var.

#### Frontend (`aura_docs/frontend/`)
- **React 18 + Vite 5** with `lucide-react` icons
- **Themes**: 4 themes available — `dark`, `light`, `cyberpunk`, `catppuccin`. Stored in `localStorage` key `kb-theme`.
- **KB Selection**: Stored in `localStorage` key `kb-selected-id`. On KB switch, `activeDoc` and `docContent` are cleared immediately to prevent cross-KB race conditions.
- **Markdown Parser** (`utils/markdownParser.js`):
  - Custom regex-based parser (NOT a library like remark/marked)
  - Handles: headings, code blocks, tables, lists, blockquotes, GitHub alerts, inline code/bold/italic/links/images
  - **Strips HTML anchor tags** `<a name="..."></a>` before escaping (they're invisible bookmark targets from AWS docs)
  - **Image regex runs BEFORE link regex** to prevent `![alt](src)` being consumed by `[text](url)` pattern
  - Links get `class="doc-link"` for SPA navigation interception
  - `.html` extensions are auto-converted to `.md` in link hrefs
- **Interactive Widgets**: DocReader splits markdown at ` ```widget:type ` delimiters and renders React components:
  - `code-playground` — editable Python console with backend execution
  - `api-playground` — Bedrock model invocation UI
  - `model-param-tester` — temperature/topP configurator with live payload preview
- **Link Navigation**: Clicks on `doc-link` anchors are intercepted by `handleContentClick` in DocReader. Relative paths are resolved against `activeDoc`'s directory. `../` traversal is supported.

#### Standalone Handbook (`sample_notes_bedrock_aws/`)
- Pure HTML/CSS/JS (no framework, no build step, just open `index.html`)
- All content lives in `data.js` as a structured JS object (`HANDBOOK_DATA`)
- Content source: Curated blend of official AWS Bedrock docs, developer notes, and YouTube tutorial transcripts (AWS Bedrock + Agent Core course)
- 34 topics across 2 parts:
  - **Part 1** (24 topics): Bedrock Foundations — Inference, Converse API, Tool Use, RAG, KB, Guardrails, Strands SDK
  - **Part 2** (10 topics): Agent Core — Runtime, Memory, Gateway, Identity, Observability, Evaluations, Policy
- Has 4 tab views: Handbook Reader, Converse API Simulator, Agent Core 7 Components Explorer, Deployment Checklists
- Progress tracking via localStorage

### Bugs Fixed in This Session

1. **KB Switch Race Condition** (`App.jsx`):
   - **Problem**: Switching KBs caused "Could not load document" error. The old `activeDoc` path from the previous KB was fetched against the new KB before navigation reset.
   - **Fix**: Added `setActiveDoc(''); setDocContent('');` at the start of the KB-change `useEffect`, before the async navigation fetch.

2. **Raw HTML Anchor Tags Showing** (`markdownParser.js`):
   - **Problem**: `<a name="model-card-amazon-nova-premier"></a>` bookmark tags rendered as visible text.
   - **Fix**: Strip `<a name="..."></a>` and empty `<a>` tags BEFORE HTML entity escaping.

3. **Broken Image Markdown** (`markdownParser.js`):
   - **Problem**: `![alt text](image.png)` showed as a broken link instead of an image.
   - **Fix**: Moved image regex (`![alt](src)`) BEFORE link regex (`[text](url)`) to prevent the link pattern from consuming image syntax.

### How to Run

**Terminal 1 — Backend:**
```bash
cd aura_docs/backend
pip install -r requirements.txt
set WORKSPACE_DIR=c:\Users\nishu\workspace\wscs_bedrock
python app.py
# Runs on http://localhost:8000
```

**Terminal 2 — Frontend:**
```bash
cd aura_docs/frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### What Still Needs Testing
- [ ] All navigation links within doc content resolve correctly across all KBs
- [ ] AI Chat with GEMINI_API_KEY configured
- [ ] "Index KB" button builds search index successfully
- [ ] All 4 themes render correctly
- [ ] Docker Compose (needs Windows path fix on line 18 of docker-compose.yml)
- [ ] Adding new `doc_replica_*` folders detected dynamically
- [ ] Interactive widgets (code-playground, api-playground) work with AWS credentials
- [ ] Standalone Handbook (`sample_notes_bedrock_aws/index.html`) — all 34 topics render
- [ ] Progress tracking persistence across refreshes

### Important Notes for Future AI Assistants
- **DO NOT** replace `markdownParser.js` with a library (remark, marked, etc.) — the custom parser is intentional for handling widget delimiters and SPA link interception.
- **DO NOT** change the `doc_replica_*` naming convention — the backend auto-discovery depends on this prefix.
- **ALWAYS** test KB switching after making frontend state changes — race conditions are easy to introduce.
- When adding new features to `data.js`, follow the existing section structure (id, title, screenshot, definition, code, keyTakeaways, etc.).
- The `docker-compose.yml` has a hardcoded Mac path on line 18 — needs to be made relative or env-var-based for portability.
