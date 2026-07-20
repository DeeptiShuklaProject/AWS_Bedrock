# Implementation Plan: Mass-Upgrade product_developer Docs with Quizzes & Playgrounds

This plan describes the automation pipeline to upgrade all 395 markdown files under the `doc_replica_product_developer` course directory with premium interactive widgets, quizzes, and code execution options. It also outlines backend engine upgrades to support running Go and Node.js code snippets.

---

## Proposed Changes

### 1. Backend Infrastructure Upgrades (Multi-Language Execution)

To enable code playgrounds for Go and Node.js files alongside Python and Java, we will configure the Docker environment and uvicorn backend.

#### [MODIFY] [Dockerfile](file:///c:/Users/nishu/workspace/wscs_bedrock/aura_docs/backend/Dockerfile)
- Add `golang-go` and `nodejs` to the apt install command so the container can compile and run Go and Javascript snippets.

#### [MODIFY] [app.py](file:///c:/Users/nishu/workspace/wscs_bedrock/aura_docs/backend/app.py)
- Refactor the `/api/playground/run-code` endpoint to handle:
  - **Go** (`go`): Write to a temporary `main.go` file inside a temporary directory, run `go run main.go`, compile/execute under a 5-second timeout, and clean up.
  - **JavaScript/Node.js** (`javascript`, `js`, `nodejs`): Write to a temporary `index.js`, run `node index.js`, capture output under a 5-second timeout, and clean up.

---

### 2. Automated Pedagogical Migration Script

We will deploy an automated script `enrich_product_developer_docs.py` to recursively scan all 395 markdown documents under `doc_replica_product_developer` and transform them.

#### [NEW] `enrich_product_developer_docs.py` (in workspace root)
The Python migration script will perform the following actions:
1. **Scan**: Recursively locate all `.md` files under `doc_replica_product_developer`.
2. **Parse Code Blocks**: Extract code blocks matching language specifiers: `python`, `java`, `javascript`, `js`, `go`.
3. **Format Playgrounds**:
   - Escape double quotes (`\"`) and newlines (`\n`) for the code block.
   - Wrap the code block in `<Tabs>` separating the static `"Syntax & Example"` and the dynamic `"Interactive Playground"` featuring `<InteractiveExample language="..." initialCode="..." />`.
4. **Context-Aware Quiz Generation**:
   - Read the keywords in the file content.
   - Dynamically generate 1-2 high-quality, relevant multiple-choice questions (e.g., Pandas DataFrame questions for pandas docs, Goroutine questions for Go docs, etc.) with custom options, answers, and explanations.
   - Append the `<Quiz>` components at the end of the file.
5. **Widget Insertion**:
   - Inject a `<ProgressTracker>` and `<InfoCard>` for structural completeness.
6. **Overwrite**: Save the transformed MDX-compliant content back to each file.

---

## Verification Plan

### Automated Verification
- Run a test suite or single manual executions of Go and Node.js code snippets via `curl` / `Invoke-RestMethod` to verify compilation and execution.
- Validate that the modified markdown files contain no unclosed tag structures or parsing syntax issues.

### Manual Verification
- Open the AuraDocs portal in the web browser.
- Navigate to Go Backend, Node.js Backend, and AI/ML guides.
- Verify that the interactive tab appears, the code runs, output displays, and quizzes show the correct responses.
