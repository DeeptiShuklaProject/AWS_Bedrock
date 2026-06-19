# AWS Bedrock Docs Replica Downloader

All files related to this documentation downloader are located in the [doc_replica_amazon/](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_amazon) folder to keep the repository root clean.

## Source & Hierarchy
* **Table of Contents (TOC)**: [toc-contents.json](https://docs.aws.amazon.com/bedrock/latest/userguide/toc-contents.json) is used to retrieve the navigation structure of the guide.
* **Target Output**: The downloaded markdown files are stored recursively inside the same `doc_replica_amazon/` directory.

## Updating the Markdown Files
The Python script `download_docs.py` will update the `.md` files inside the replica directory:

To update or redownload the files:
```bash
python3 doc_replica_amazon/download_docs.py
```
