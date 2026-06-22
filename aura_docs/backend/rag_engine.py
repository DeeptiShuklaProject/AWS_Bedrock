import os
import json
import re
import math
from google import genai
from google.genai import types

class RAGEngine:
    def __init__(self, workspace_dir, kb_id):
        self.workspace_dir = workspace_dir
        self.kb_id = kb_id
        self.kb_dir = os.path.join(workspace_dir, kb_id)
        self.cache_path = os.path.join(workspace_dir, "aura_docs", "backend", f"embeddings_{kb_id}_cache.json")
        self.client = None
        self.index = []
        
        # Initialize Gemini Client if API Key is available
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize GenAI client: {e}")
        else:
            print("Warning: GEMINI_API_KEY environment variable not found. RAG functionality will be offline.")

        self.load_index()

    def get_md_files(self):
        """Recursively retrieve all .md file paths in the KB directory."""
        md_files = []
        if not os.path.exists(self.kb_dir):
            return md_files
        for root, _, files in os.walk(self.kb_dir):
            for file in files:
                if file.endswith(".md") and not file.startswith("."):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.kb_dir)
                    md_files.append((full_path, rel_path))
        return md_files

    def chunk_document(self, text, max_chars=1200, overlap=200):
        """Split markdown text into logical chunks by heading or paragraph size."""
        # Clean double spaces or metadata headers if any
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Split by headings first to keep sections coherent
        sections = re.split(r'(\n#+\s+)', text)
        
        chunks = []
        current_chunk = ""
        
        for part in sections:
            if not part:
                continue
            if len(current_chunk) + len(part) <= max_chars:
                current_chunk += part
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                # If a single section is too long, split it by paragraphs
                if len(part) > max_chars:
                    paragraphs = part.split("\n\n")
                    for para in paragraphs:
                        if len(current_chunk) + len(para) <= max_chars:
                            current_chunk += "\n\n" + para
                        else:
                            if current_chunk.strip():
                                chunks.append(current_chunk.strip())
                            current_chunk = para
                else:
                    current_chunk = part
                    
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks

    def load_index(self):
        """Load the cached embeddings if they exist."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    self.index = json.load(f)
                print(f"Loaded cached index for {self.kb_id} with {len(self.index)} files.")
            except Exception as e:
                print(f"Error loading index cache: {e}")
                self.index = []

    def save_index(self):
        """Save the current embeddings index to local cache file."""
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self.index, f, indent=2)
            print(f"Saved index cache for {self.kb_id}.")
        except Exception as e:
            print(f"Error saving index cache: {e}")

    def build_index(self, force=False):
        """Build the embedding index for all markdown files in this KB."""
        if not self.client:
            return False, "GEMINI_API_KEY not configured"

        md_files = self.get_md_files()
        existing_paths = {item["rel_path"]: item for item in self.index}
        new_index = []
        updated = False

        print(f"Indexing KB '{self.kb_id}' ({len(md_files)} files total)...")

        for full_path, rel_path in md_files:
            # Check modification time to see if we can reuse the cached index
            mtime = os.path.getmtime(full_path)
            
            if not force and rel_path in existing_paths and existing_paths[rel_path].get("mtime") == mtime:
                # Reuse cached embeddings
                new_index.append(existing_paths[rel_path])
                continue

            # Process new or modified file
            print(f"Embedding file: {rel_path}")
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                chunks = self.chunk_document(content)
                if not chunks:
                    continue

                # Generate embeddings for all chunks in batch
                embeddings = []
                # Google GenAI SDK allows embedding batches
                response = self.client.models.embed_content(
                    model="text-embedding-004",
                    contents=chunks
                )
                
                # Check response structure. In google-genai, embeddings is a list of ContentEmbedding
                for i, chunk_emb in enumerate(response.embeddings):
                    embeddings.append({
                        "text": chunks[i],
                        "values": chunk_emb.values
                    })

                new_index.append({
                    "rel_path": rel_path,
                    "mtime": mtime,
                    "chunks": embeddings
                })
                updated = True
            except Exception as e:
                print(f"Error indexing {rel_path}: {e}")
                # Keep existing if error, so we don't wipe it out
                if rel_path in existing_paths:
                    new_index.append(existing_paths[rel_path])

        self.index = new_index
        if updated or force:
            self.save_index()
        return True, "Index build completed"

    def cosine_similarity(self, v1, v2):
        """Compute the cosine similarity between two vector lists."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a * a for a in v1))
        magnitude_v2 = math.sqrt(sum(a * a for a in v2))
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)

    def search(self, query, top_n=5):
        """Perform semantic search for matching chunks."""
        if not self.client:
            return []
            
        if not self.index:
            self.build_index()

        try:
            # Embed the query
            query_response = self.client.models.embed_content(
                model="text-embedding-004",
                contents=query
            )
            query_vector = query_response.embeddings[0].values
        except Exception as e:
            print(f"Error embedding query: {e}")
            return []

        results = []
        for file_item in self.index:
            for chunk in file_item["chunks"]:
                similarity = self.cosine_similarity(query_vector, chunk["values"])
                results.append({
                    "rel_path": file_item["rel_path"],
                    "text": chunk["text"],
                    "similarity": similarity
                })

        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_n]

    def answer_question(self, query):
        """Retrieve context and answer the user question using Gemini."""
        if not self.client:
            return "Error: GEMINI_API_KEY environment variable not configured. Cannot perform Q&A.", []

        # 1. Search for matching documents
        matches = self.search(query, top_n=5)
        if not matches:
            return "I could not find any relevant information in the documentation to answer your question.", []

        # 2. Build prompt context
        context_blocks = []
        sources = []
        for i, match in enumerate(matches):
            context_blocks.append(f"--- Document Chunk {i+1} (Source: {match['rel_path']}) ---\n{match['text']}")
            if match['rel_path'] not in sources:
                sources.append(match['rel_path'])

        context = "\n\n".join(context_blocks)

        system_instruction = (
            "You are an expert technical documentation assistant.\n"
            "Answer the user's question accurately using ONLY the provided documentation context below.\n"
            "If the answer cannot be found in the context, state that you cannot find the answer in the provided documents.\n"
            "Do not make up facts or use external knowledge not in the context.\n"
            "Keep your answer clear, structured, and developer-friendly."
        )

        user_content = f"CONTEXT:\n{context}\n\nQUESTION:\n{query}"

        try:
            # Query Gemini
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )
            return response.text, sources
        except Exception as e:
            return f"Error invoking Gemini model: {e}", []
