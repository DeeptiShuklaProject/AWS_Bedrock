# AWS Bedrock Docs Replica Downloader

This repository contains tools to download and update a local markdown replica of the AWS Bedrock User Guide, preserving its navigation tree structure.

## Sources
* **Table of Contents (TOC)**: [toc-contents.json](https://docs.aws.amazon.com/bedrock/latest/userguide/toc-contents.json) is used to read the structure of the guide.
* **Target Output**: [doc_replica_amazon/](file:///Users/nishantsaxena/workspace/wscs_bedrock/doc_replica_amazon) holds the downloaded markdown (`.md`) files.

## Updating the Replica
The Python script `download_docs.py` fetches the latest TOC and downloads the latest markdown files to the replica folder.

To update or redownload the files:
```bash
python3 download_docs.py
```
