# AuraDocs Architecture

AuraDocs is a **database-free, local-first interactive runtime environment** that joins raw documentation with live code testing.

---

## 1. Local-First & Serverless Database Layout
* **No Database Server**: The application does not require a SQL/NoSQL database server by default. The raw folder trees of markdown (`.md`) files on your hard drive serve directly as the primary data store. (Note: A database will be added in the future, for example, when migrating to a multi-user system).
* **Vector Search Cache**: For RAG search, the backend computes embeddings via the Google GenAI SDK and caches them in a single local JSON file per Knowledge Base:
  `aura_docs/backend/embeddings_[kb_id]_cache.json`
  This enables rapid semantic queries and offline functionality.

---

## 2. Hybrid Rendering ("Two Worlds")
* **Standard Markdown**: The text is parsed to HTML in the frontend using a customized regex parser to maintain compatibility and render elements like headers, lists, code highlight blocks, and tables.
* **Dynamic React Widgets**: The `DocReader.jsx` component splits the document text at custom widget delimiters:
  ` ```widget:[widget-type] `
  ` [JSON Configuration / Code Snippet] `
  ` ``` `
  It parses the data within these delimiters and replaces the static block with fully interactive React components (`ModelParamTesterWidget`, `ApiPlaygroundWidget`, `CodePlaygroundWidget`) in-place.

---

## 3. Local Execution & AWS API Calling
* **Local Code Playground**: When you run Python code in the interactive console, the frontend sends the snippet to the backend (`/api/playground/run-code`). The backend executes the script inside the developer's local environment, redirects `sys.stdout` and `sys.stderr`, and returns the stdout outputs to the console view.
* **AWS Bedrock Integration**: The local backend uses the python `boto3` library to interface with your AWS credentials. When you invoke model queries in the playground, it automatically authenticates using your local `~/.aws` profile credentials and sends the requests directly to Bedrock.

---

## 4. Self-Documenting Agent Skills
* **Autonomous Onboarding**: Future AI agents accessing this repository are guided by the root [README.md](../../README.md) and [list.md](../../list.md) to understand the codebase.
* **Orchestration**: The [run.sh](../../run.sh) and [docker-compose.yml](../../docker-compose.yml) files act as a runnable blueprint that any agent or developer can use to spin up the portal instantly on any machine.
