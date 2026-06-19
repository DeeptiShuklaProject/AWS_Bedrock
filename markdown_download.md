# AWS Bedrock Documentation Downloader Guide

This tool downloads the AWS Bedrock User Guide's documentation pages in raw Markdown (`.md`) format, preserving the nested navigation structure defined in the guide's Table of Contents.

## How It Works

1. **Fetch Table of Contents**: The script reads the Table of Contents file `toc-contents.json` from the AWS documentation.
2. **Build Navigation Hierarchy**: It traverses the JSON tree recursively, creating sanitized folders for category titles (e.g., `Models at a glance/Amazon/`).
3. **Download Markups**: It maps the `.html` links in the TOC to their corresponding `.md` formats and downloads them directly.
4. **Resiliency & Performance**:
   - **Concurrency**: Uses a multi-threaded pool to download pages in parallel.
   - **Retry Mechanism**: Automatically retries failed requests with exponential backoff.
   - **Resume Capability**: Skips files that have already been downloaded, allowing you to stop and resume the download at any time without losing progress.

## Running the Downloader

Because the terminal sandbox restricts internet access, you need to run this script on your local machine outside the sandbox.

### Steps to Run:

1. Open your local terminal in the project directory:
   ```bash
   cd /Users/nishantsaxena/workspace/wscs_bedrock
   ```

2. Run the Python downloader script:
   ```bash
   python3 download_docs.py
   ```

### Command Line Options

You can customize the download by passing optional arguments:

```bash
# Preview the folders and files that will be created without downloading anything (dry run)
python3 download_docs.py --dry-run

# Limit the download to a specific section (e.g. only download 'Models at a glance')
python3 download_docs.py --section "Models at a glance"

# Change the output folder (defaults to 'bedrock_userguide_markdown')
python3 download_docs.py --output "./my_docs"

# Adjust concurrent download threads (default is 10)
python3 download_docs.py --threads 5
```

## Structure Output Example

The downloaded folder structure will look like this:

```
bedrock_userguide_markdown/
├── Overview.md
├── Quickstart/
│   ├── getting-started.md
│   └── ...
└── Models at a glance/
    ├── model-cards.md
    ├── AI21 Labs/
    │   ├── model-cards-ai21-labs.md
    │   ├── Jamba 1.5 Large.md
    │   └── Jamba 1.5 Mini.md
    └── Amazon/
        ├── model-cards-amazon.md
        ├── model-card-amazon-nova-premier.md
        └── ...
```
