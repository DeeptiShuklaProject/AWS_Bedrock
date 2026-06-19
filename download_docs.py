import os
import json
import urllib.request
import urllib.error
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

BASE_URL = "https://docs.aws.amazon.com/bedrock/latest/userguide/"
TOC_URL = BASE_URL + "toc-contents.json"

def sanitize_name(name):
    """Sanitize the category or page title to be a safe directory/file name."""
    if not name:
        return "unnamed"
    # Replace characters not allowed in filenames
    clean = re.sub(r'[\\/*?:"<>|]', " ", name)
    # Remove extra spaces
    clean = re.sub(r'\s+', " ", clean)
    return clean.strip()

def get_filename_from_href(href):
    """Extract the filename with .md extension from href."""
    if not href:
        return None
    base = os.path.basename(href)
    if base.endswith(".html"):
        return base[:-5] + ".md"
    elif base.endswith(".md"):
        return base
    return base

def extract_jobs(contents, current_path=[], filter_section=None):
    """Recursively traverse the TOC to yield download jobs."""
    jobs = []
    for item in contents:
        title = item.get("title", "")
        href = item.get("href", "")
        sanitized_title = sanitize_name(title)
        
        # Check if we are filtering by top-level section
        if not current_path and filter_section and filter_section.lower() not in title.lower():
            continue
            
        if "contents" in item:
            # Category folder node
            new_path = current_path + [sanitized_title]
            if href:
                filename = get_filename_from_href(href)
                if filename:
                    jobs.append({
                        "url": BASE_URL + href.replace(".html", ".md"),
                        "dest_dir": new_path,
                        "filename": filename,
                        "title": title
                    })
            jobs.extend(extract_jobs(item["contents"], new_path, filter_section))
        else:
            # Leaf page node
            if href:
                filename = get_filename_from_href(href)
                if filename:
                    jobs.append({
                        "url": BASE_URL + href.replace(".html", ".md"),
                        "dest_dir": current_path,
                        "filename": filename,
                        "title": title
                    })
    return jobs

def download_file(url, dest_path, retries=5, backoff=2.0):
    """Download a file with retry logic and exponential backoff."""
    if os.path.exists(dest_path):
        return True, "skipped (already exists)"
        
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                content = response.read()
            with open(dest_path, "wb") as f:
                f.write(content)
            return True, "success"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False, f"failed (404 Not Found)"
            elif e.code in (429, 500, 502, 503, 504):
                time.sleep(backoff * (2 ** attempt))
            else:
                return False, f"failed (HTTP {e.code})"
        except Exception as e:
            time.sleep(backoff * (2 ** attempt))
            
    return False, "failed (max retries reached)"

def main():
    parser = argparse.ArgumentParser(description="AWS Bedrock Documentation Downloader")
    parser.add_argument("--output", default="doc_replica_amazon", help="Destination folder for markups")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent download threads")
    parser.add_argument("--section", default=None, help="Filter to only download this top-level category section")
    parser.add_argument("--dry-run", action="store_true", help="List directories and files without downloading")
    parser.add_argument("--limit", type=int, default=None, help="Limit total number of files to download (for testing)")
    args = parser.parse_args()

    # Step 1: Load or fetch the Table of Contents
    print("Loading Table of Contents...")
    toc_data = None
    
    # Try reading from a local copy in the workspace first, then fall back to fetching online
    local_toc_path = "toc-contents.json"
    if os.path.exists(local_toc_path):
        try:
            with open(local_toc_path, "r", encoding="utf-8") as f:
                toc_data = json.load(f)
            print("Loaded Table of Contents from local toc-contents.json")
        except Exception as e:
            print(f"Warning: Could not parse local toc-contents.json: {e}")
            
    if not toc_data:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(TOC_URL, headers=headers)
            with urllib.request.urlopen(req) as response:
                toc_data = json.loads(response.read().decode('utf-8'))
            print("Fetched Table of Contents from AWS web service.")
            # Cache it locally
            with open(local_toc_path, "w", encoding="utf-8") as f:
                json.dump(toc_data, f, indent=2)
        except Exception as e:
            print(f"Error fetching Table of Contents: {e}")
            return

    # Step 2: Extract download jobs
    print("Parsing table of contents...")
    jobs = extract_jobs(toc_data.get("contents", []), filter_section=args.section)
    
    if args.limit:
        jobs = jobs[:args.limit]
        print(f"Limiting download to the first {args.limit} files.")

    total_jobs = len(jobs)
    print(f"Total files to process: {total_jobs}")

    if args.dry_run:
        print("\n--- Dry Run: Planned Files and Folders ---")
        for i, job in enumerate(jobs[:20], 1):
            rel_dir = os.path.join(*job["dest_dir"]) if job["dest_dir"] else ""
            print(f"{i}. Dir: {rel_dir} | File: {job['filename']} | Title: {job['title']}")
        if total_jobs > 20:
            print(f"... and {total_jobs - 20} more files.")
        return

    # Step 3: Run the downloading process
    print(f"\nStarting download using {args.threads} threads...")
    success_count = 0
    skipped_count = 0
    failed_count = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit all jobs
        futures = {}
        for job in jobs:
            rel_dir = os.path.join(*job["dest_dir"]) if job["dest_dir"] else ""
            dest_dir_full = os.path.join(args.output, rel_dir)
            dest_path = os.path.join(dest_dir_full, job["filename"])
            
            future = executor.submit(download_file, job["url"], dest_path)
            futures[future] = (job, dest_path)
            
        # Track progress
        completed_count = 0
        for future in as_completed(futures):
            completed_count += 1
            job, dest_path = futures[future]
            try:
                success, status = future.result()
                rel_path = os.path.relpath(dest_path, args.output)
                
                if success:
                    if "skipped" in status:
                        skipped_count += 1
                    else:
                        success_count += 1
                    print(f"[{completed_count}/{total_jobs}] SUCCESS: {rel_path} ({status})")
                else:
                    failed_count += 1
                    print(f"[{completed_count}/{total_jobs}] FAILED: {rel_path} ({status})")
            except Exception as e:
                failed_count += 1
                print(f"[{completed_count}/{total_jobs}] ERROR: {job['filename']} -> {e}")

    elapsed_time = time.time() - start_time
    print("\n--- Download Summary ---")
    print(f"Total time: {elapsed_time:.1f} seconds")
    print(f"Success: {success_count}")
    print(f"Skipped (exists): {skipped_count}")
    print(f"Failed: {failed_count}")

if __name__ == "__main__":
    main()
