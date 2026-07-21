import os
import shutil
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running cmd '{cmd}': {result.stderr.decode('utf-8', errors='ignore')}")
    return result.stdout.decode('utf-8', errors='ignore')

# Define directories
root_notes_dir = "doc_uday_advance_notes"
backup_dir = os.path.join(root_notes_dir, "backup")
replica_dir = "doc_replica_aws-bedrock/doc_uday_advance_notes"
replica_backup_dir = os.path.join(replica_dir, "backup")

# 1. Create or refresh the root backup folder
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
os.makedirs(backup_dir, exist_ok=True)

# 2. Get all .md files in the root_notes_dir
md_files = [f for f in os.listdir(root_notes_dir) if f.endswith(".md")]

print("Restoring original files from Git to the backup folder...")
for f in md_files:
    # Get original content from HEAD (before our changes in this session)
    git_path = f"doc_uday_advance_notes/{f}"
    original_content = run_cmd(f"git show 20ab2478455d4536d2bcd4daa9973381f8e0c806:{git_path}")
    if original_content.strip():
        dest_path = os.path.join(backup_dir, f)
        with open(dest_path, "w", encoding="utf-8") as out:
            out.write(original_content)
        print(f"  Restored original: {f}")

# 3. Create or refresh doc_replica_aws-bedrock/doc_uday_advance_notes/ and its backup folder
if os.path.exists(replica_dir):
    shutil.rmtree(replica_dir)
os.makedirs(replica_dir, exist_ok=True)
os.makedirs(replica_backup_dir, exist_ok=True)

# 4. Copy all current (enriched) files to the replica folder
print("\nCopying enriched files to replica directory...")
for f in md_files:
    src_path = os.path.join(root_notes_dir, f)
    dest_path = os.path.join(replica_dir, f)
    shutil.copy2(src_path, dest_path)
    print(f"  Copied enriched: {f}")

# 5. Copy all backup (original) files to the replica backup folder
print("\nCopying original backup files to replica backup directory...")
for f in os.listdir(backup_dir):
    if f.endswith(".md"):
        src_path = os.path.join(backup_dir, f)
        dest_path = os.path.join(replica_backup_dir, f)
        shutil.copy2(src_path, dest_path)
        print(f"  Copied backup: {f}")

# 6. Create the backup.md file in doc_replica_aws-bedrock/
backup_md_path = "doc_replica_aws-bedrock/backup.md"
print(f"\nCreating {backup_md_path}...")
with open(backup_md_path, "w", encoding="utf-8") as out:
    out.write("# AWS Bedrock AgentCore Course Backup Index\n\n")
    out.write("This file lists the backup and restored chapters for the Bedrock AgentCore course.\n\n")
    out.write("## Restored Chapters\n\n")
    out.write("| Chapter Name | Description |\n")
    out.write("| :--- | :--- |\n")
    for f in sorted(md_files):
        if f.startswith("0") or f.startswith("1"):
            out.write(f"| [{f}](./doc_uday_advance_notes/{f}) | Enriched chapter with pedagogical explanations. |\n")
            out.write(f"| [{f} (Original Backup)](./doc_uday_advance_notes/backup/{f}) | Original baseline chapter. |\n")
            
print("Restoration and backup sync completed successfully!")
