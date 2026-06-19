# AWS Bedrock Documentation Markdown Downloader

The goal is to download all documentation pages of the AWS Bedrock User Guide in Markdown format, preserving the nested navigation structure defined by the site's Table of Contents (`toc-contents.json`). We will create a Python script to perform this download concurrently with retries, and document the process in a new helper/skill file `markdown_download.md`.

## User Review Required

> [!IMPORTANT]
> The complete AWS Bedrock User Guide contains over 2,000 pages. Downloading all of them will take some time and make thousands of requests to the AWS documentation server. We have built-in resume capability, concurrency, rate limiting, and retry mechanisms in the script to ensure it is efficient, gentle on the servers, and robust against failures.

> [!NOTE]
> The terminal command execution environment is sandboxed and does not have internet access. Therefore, the download script must be executed on your local machine outside the sandbox. We will request `unsandboxed` permission to run the script or provide instructions for you to run it directly.

## Open Questions

None at this stage. The requirements are clear, and we have verified that AWS serves raw `.md` files directly.

## Proposed Changes

### Scraping and Downloading Tooling

---

#### [NEW] [download_docs.py](file:///Users/nishantsaxena/workspace/wscs_bedrock/download_docs.py)
A Python script that:
1. Downloads `toc-contents.json` using `urllib` or a local copy if already fetched.
2. Traverses the nested JSON structure.
3. Maps each page `href` from `.html` to `.md` and retrieves it from `https://docs.aws.amazon.com/bedrock/latest/userguide/`.
4. Saves files to a structured folder directory tree under `bedrock_userguide_markdown/` matching the navigation titles.
5. Employs a thread pool for concurrent downloads, exponential backoff retries, and resume capability.

#### [NEW] [markdown_download.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/markdown_download.md)
The documentation/skill helper file explaining how the script works, how to run it, configuration parameters, and recovery steps if it stops.

## Verification Plan

### Automated Tests
- We will test the script on a subset of the pages (e.g., first 10 pages) to verify the directory structure and file contents are correctly retrieved and structured.
- Run `python3 download_docs.py --dry-run` to output the folder tree and count without downloading.

### Manual Verification
- Verify the generated `bedrock_userguide_markdown/` folder structure and check that files like `Models at a glance/Amazon/Nova Premier.md` are correctly populated.
