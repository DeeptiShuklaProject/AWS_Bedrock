import subprocess
import sys

def run_enrichment():
    print("Executing Bedrock AgentCore handbook documentation enrichment script...")
    # By default, run for Chapter 1 in mock mode as requested
    cmd = [
        sys.executable,
        r"c:\Users\nishu\workspace\wscs_bedrock\scratch\enrich_chapters.py",
        "--file", "01_Chapter_introduction_to_bedrock_agentcore.md"
    ]
    
    # If the user passed arguments to test_enrich.py, pass them along
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    else:
        cmd.append("--force-mock")
        
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    run_enrichment()
