# AuraDocs: Multi-KB Documentation Portal & AI Agent Workspace

Welcome! This workspace contains the raw documentation replicas and the interactive full-stack portal for searching and querying them using AI.

## Quick Start
To build and launch the application containers:
1. Open your terminal.
2. Start the services:
   ```bash
   docker compose up --build
   ```
3. Open `http://localhost:3000` in your web browser.

---

## Workspace Directory Map
* **[docker-compose.yml](file:///Users/nishantsaxena/workspace/wscs_bedrock/docker-compose.yml)**: Builds and launches the backend (FastAPI) and frontend (React) containers with local file volume mounting.
* **[list.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/list.md)**: A complete list index of all files worked on and modified so far.
* **[doc_replica_amazon/](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_amazon/)**: Contains the official AWS Bedrock User Guide (.md files).
* **[aura_docs/](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/)**: Contains the full-stack web application.
  * For detailed frontend/backend layout and configuration, see **[aura_docs/README.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/aura_docs/README.md)**.
