# Walkthrough of AWS Bedrock Docs Scraper

We have successfully implemented and added the AWS Bedrock documentation markdown downloader tools to the workspace.

## Changes Completed

### Downloader Script
* [download_docs.py](file:///Users/nishantsaxena/workspace/wscs_bedrock/download_docs.py): A concurrent Python script featuring rate limiting, resume capabilities, path-sanitization, and exponential backoff retry mechanisms to safely fetch AWS documentation markups.

### Documentation & Guides
* [markdown_download.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/markdown_download.md): A comprehensive markdown guide for the user detailing how to run, customize, and configure the scraper script locally.
* [implementation_plan.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/implementation_plan.md): The approved design plan for this task.
* [task.md](file:///Users/nishantsaxena/workspace/wscs_bedrock/task.md): The status tracker checklist showing completed progress.

## How to execute

Since the agent terminal environment does not have outgoing internet access, you can run the download locally on your machine:
```bash
python3 download_docs.py
```
This will automatically retrieve the latest TOC, map all documentation links to their raw `.md` equivalents, and save them in the matching directory tree structure inside a new folder named `bedrock_userguide_markdown/`.
