import os
import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from rag_engine import RAGEngine

app = FastAPI(title="AuraDocs API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Workspace directory path (parent of all doc_replica_* folders)
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ChatRequest(BaseModel):
    query: str

def get_kb_display_name(kb_id: str) -> str:
    """Map kb_id suffix to a clean display name."""
    mapping = {
        "doc_replica_notes": "Nishu @Work",
        "doc_replica_amazon": "AWS Bedrock User Guide",
        "doc_replica_terraform": "Terraform AWS Provider",
        "doc_replica_boto3": "Boto3 (Python SDK) Docs",
        "doc_replica_general": "General Bedrock Skills",
        "doc_replica_youtube": "YouTube Course Transcripts",
        "doc_replica_aws-bedrock": "AWS Bedrock AgentCore",
        "doc_replica_aws_bedrock": "AWS Bedrock AgentCore",
        "doc_replica_lambda": "AWS Lambda Developer Guide",
        "doc_uday_advance_notes": "Uday Bedrock Notes",
        "doc_bedrock_notes": "Uday Bedrock Notes",
        "doc_uday_bedrock_notes": "Uday Bedrock Notes",
        "doc_deepti_bedrock_notes": "Deepti Bedrock Notes"
    }
    if kb_id in mapping:
        return mapping[kb_id]
    suffix = kb_id.replace("doc_replica_", "").replace("doc_uday_", "")
    return suffix.replace("_", " ").title()

@app.get("/api/config")
def get_config():
    """Return application configuration and features status."""
    return {"has_api_key": bool(os.environ.get("GEMINI_API_KEY"))}

@app.get("/api/kbs")
def list_knowledge_bases():
    """List all available doc_replica_* folders in the workspace."""
    kbs = []
    if os.path.exists(WORKSPACE_DIR):
        for name in os.listdir(WORKSPACE_DIR):
            full_path = os.path.join(WORKSPACE_DIR, name)
            if os.path.isdir(full_path) and name.startswith("doc_"):
                kbs.append({
                    "id": name,
                    "name": get_kb_display_name(name)
                })
    return sorted(kbs, key=lambda x: x["name"])

def build_nav_from_fs(directory: str, current_dir: str) -> List[Dict[str, Any]]:
    """Fallback directory walker to generate a navigation tree from folders of .md files, stripping sorting prefixes."""
    import re
    items = []
    if not os.path.exists(current_dir):
        return items
        
    # Load order.json if it exists to customize ordering
    order = []
    order_path = os.path.join(current_dir, "order.json")
    if os.path.exists(order_path):
        try:
            with open(order_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    order = data
        except Exception as e:
            print(f"Warning: Failed to load order.json in {current_dir}: {e}")

    dir_contents = os.listdir(current_dir)
    files_to_sort = [name for name in dir_contents if not name.startswith(".") and name != "order.json"]
    
    if order:
        # Create a mapping of both exact and lowercase representations from order.json to indices
        order_map = {}
        for idx, item in enumerate(order):
            if item not in order_map:
                order_map[item] = idx
            item_lower = item.lower()
            if item_lower not in order_map:
                order_map[item_lower] = idx
                
        def get_order_index(name):
            clean_name = re.sub(r'^\d+[\s_]+', '', name)
            title_base = clean_name[:-3] if clean_name.endswith(".md") else clean_name
            clean_title = title_base.replace("_", " ").title()
            
            candidates = [
                name,
                clean_name,
                title_base,
                clean_title,
                name.lower(),
                clean_name.lower(),
                title_base.lower(),
                clean_title.lower()
            ]
            for cand in candidates:
                if cand in order_map:
                    return order_map[cand]
            return None

        # Sort based on matched order index; items not in order.json go to the end sorted alphabetically
        def sort_key(name):
            idx = get_order_index(name)
            if idx is not None:
                return (0, idx, name)
            else:
                return (1, 0, name.lower())
        sorted_names = sorted(files_to_sort, key=sort_key)
    else:
        sorted_names = sorted(files_to_sort)
        
    for name in sorted_names:
        full_path = os.path.join(current_dir, name)
        rel_path = os.path.relpath(full_path, directory)
        
        # Clean prefix (e.g. "doc_bedrock_notes" -> "bedrock_notes", "01_welcome" -> "welcome")
        clean_name = re.sub(r'^(doc_replica_|doc_uday_|doc_)+', '', name, flags=re.IGNORECASE)
        clean_name = re.sub(r'^\d+[\s_]+', '', clean_name)
        
        if os.path.isdir(full_path):
            sub_items = build_nav_from_fs(directory, full_path)
            has_index = False
            href = ""
            for sub in sub_items:
                if sub.get("title", "").lower() in ("index", "readme"):
                    href = sub.get("href", "")
                    has_index = True
                    break
            
            if clean_name.lower() in ("summarised_notes_2nd_bedrock_notes", "backup"):
                clean_title = "Summarised Notes (2nd Bedrock Notes)"
            else:
                clean_title = clean_name.replace("_", " ").title()
            
            if sub_items:
                node = {
                    "title": clean_title,
                    "contents": sub_items
                }
                if has_index:
                    node["href"] = href
                items.append(node)
                
        elif name.endswith(".md"):
            title_base = clean_name[:-3] if clean_name.endswith(".md") else clean_name
            if title_base.startswith("Chapter_"):
                title = title_base
            elif title_base.lower() in ("index", "readme"):
                dir_name = os.path.basename(current_dir)
                dir_clean = re.sub(r'^(doc_replica_|doc_uday_|doc_)+', '', dir_name, flags=re.IGNORECASE)
                dir_clean = re.sub(r'^\d+[\s_]+', '', dir_clean)
                title = dir_clean.replace("_", " ").title()
            else:
                title = title_base.replace("_", " ").title()
            items.append({
                "title": title,
                "href": rel_path
            })
    return items

@app.get("/api/kbs/{kb_id}/navigation")
def get_kb_navigation(kb_id: str):
    """Serve the navigation TOC tree for the selected KB."""
    kb_dir = os.path.join(WORKSPACE_DIR, kb_id)
    if not os.path.exists(kb_dir) or not os.path.isdir(kb_dir):
        raise HTTPException(status_code=404, detail="Knowledge base folder not found")
        
    # Option 1: Try to load toc-contents.json (standard AWS documentation TOC)
    toc_path = os.path.join(kb_dir, "toc-contents.json")
    if os.path.exists(toc_path):
        try:
            with open(toc_path, "r", encoding="utf-8") as f:
                toc_data = json.load(f)
            # Map toc keys to standardized React navigation tree keys if needed
            return toc_data.get("contents", [])
        except Exception as e:
            print(f"Warning: Failed to load toc-contents.json: {e}")
            
    # Option 2: Fallback to scanning filesystem structure
    print(f"Generating navigation tree from filesystem walker for {kb_id}...")
    return build_nav_from_fs(kb_dir, kb_dir)

@app.get("/api/kbs/{kb_id}/document")
def get_kb_document(kb_id: str, path: str = Query(..., description="Relative path to .md file")):
    """Retrieve and serve the content of a markdown document."""
    kb_dir = os.path.join(WORKSPACE_DIR, kb_id)
    if not os.path.exists(kb_dir):
        raise HTTPException(status_code=404, detail="Knowledge base not found")
        
    # Prevent Directory Traversal Vulnerability (LFI)
    target_path = os.path.abspath(os.path.join(kb_dir, path))
    base_dir_resolved = os.path.abspath(kb_dir)
    if not target_path.startswith(base_dir_resolved):
        raise HTTPException(status_code=403, detail="Access denied: outside directory boundary")
        
    # Dynamically resolve .html request extensions to .md files
    if not os.path.exists(target_path) and target_path.endswith(".html"):
        md_path = target_path[:-5] + ".md"
        if os.path.exists(md_path):
            target_path = md_path

    # Fallback: search recursively if not found at exact path (for nested files with flat TOC references)
    if not os.path.exists(target_path):
        filename = os.path.basename(target_path)
        if filename.endswith(".html"):
            filename = filename[:-5] + ".md"
        elif not filename.endswith(".md"):
            filename = filename + ".md"
            
        found_path = None
        for root, dirs, files in os.walk(kb_dir):
            if filename in files:
                found_path = os.path.join(root, filename)
                break
        if found_path:
            target_path = found_path

    if not os.path.exists(target_path) or not os.path.isfile(target_path):
        raise HTTPException(status_code=404, detail=f"Document {path} not found")
        
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/kbs/{kb_id}/index")
def index_kb(kb_id: str):
    """Trigger semantic vector indexing for the chosen KB."""
    # Check if folder exists
    kb_dir = os.path.join(WORKSPACE_DIR, kb_id)
    if not os.path.exists(kb_dir):
        raise HTTPException(status_code=404, detail="Knowledge base not found")
        
    engine = RAGEngine(WORKSPACE_DIR, kb_id)
    if not engine.api_key:
        raise HTTPException(status_code=400, detail="GEMINI_API_KEY environment variable is not set. Cannot index.")
        
    success, msg = engine.build_index(force=True)
    if not success:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}

@app.post("/api/kbs/{kb_id}/chat")
def chat_with_kb(kb_id: str, request: ChatRequest):
    """Perform RAG search and generate answer using Gemini."""
    kb_dir = os.path.join(WORKSPACE_DIR, kb_id)
    if not os.path.exists(kb_dir):
        raise HTTPException(status_code=404, detail="Knowledge base not found")
        
    engine = RAGEngine(WORKSPACE_DIR, kb_id)
    if not engine.api_key:
        return {
            "answer": "⚠️ **RAG System Offline**: The `GEMINI_API_KEY` environment variable is not configured. Please set it in your environment and restart the backend server to use the AI Q&A Agent.",
            "sources": []
        }
        
    answer, sources = engine.answer_question(request.query)
    return {"answer": answer, "sources": sources}

class InvokeRequest(BaseModel):
    model_id: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 500

@app.post("/api/playground/invoke")
def invoke_bedrock_model(request: InvokeRequest):
    """Invoke an AWS Bedrock model using local Boto3 credentials."""
    try:
        import boto3
        import json
        
        client = boto3.client("bedrock-runtime")
        
        # Build provider-specific request payload
        body_dict = {}
        if "anthropic" in request.model_id:
            body_dict = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": request.max_tokens,
                "messages": [{"role": "user", "content": request.prompt}],
                "temperature": request.temperature
            }
        elif "meta" in request.model_id:
            body_dict = {
                "prompt": request.prompt,
                "max_gen_len": request.max_tokens,
                "temperature": request.temperature
            }
        else:
            # Default to Amazon Titan format
            body_dict = {
                "inputText": request.prompt,
                "textGenerationConfig": {
                    "maxTokenCount": request.max_tokens,
                    "stopSequences": [],
                    "temperature": request.temperature,
                    "topP": 0.9
                }
            }
            
        response = client.invoke_model(
            modelId=request.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body_dict)
        )
        
        response_body = json.loads(response.get('body').read().decode('utf-8'))
        
        # Parse output depending on provider
        result_text = ""
        if "anthropic" in request.model_id:
            result_text = response_body.get("content", [{}])[0].get("text", "")
        elif "meta" in request.model_id:
            result_text = response_body.get("generation", "")
        else:
            result_text = response_body.get("results", [{}])[0].get("outputText", "")
            if not result_text and "output" in response_body:
                result_text = response_body.get("output", "")
                
        return {"success": True, "output": result_text}
    except Exception as e:
        return {"success": False, "error": str(e)}

class RunCodeRequest(BaseModel):
    code: str

@app.post("/api/playground/run-code")
def run_code_playground(request: RunCodeRequest):
    """Execute Python code locally and return stdout/stderr."""
    import sys
    import io
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    
    try:
        # Execute the code block locally
        exec(request.code, {"__name__": "__main__"})
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        return {
            "success": True,
            "stdout": redirected_output.getvalue(),
            "stderr": redirected_error.getvalue()
        }
    except Exception as e:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        return {
            "success": False,
            "stdout": redirected_output.getvalue(),
            "stderr": redirected_error.getvalue() + str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
