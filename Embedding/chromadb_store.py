import os
import json
import chromadb
import embedding # Uses your local embedding model
# Use the new v1.0 import path
from langchain_chroma import Chroma

# 1. DYNAMIC PATH SETUP: Works on any PC
script_dir = os.path.dirname(os.path.abspath(__file__))
base_data_path = os.path.abspath(os.path.join(script_dir, "..", "Scraped_data"))

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./knowledgebase")
collection = client.get_or_create_collection(name="sunbeam_data")

def store_db(full_path, relative_id):
    """Processes a single JSON file and adds it to the collection."""
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Build content text dynamically
        full_text_content = f"Program: {data.get('program_name', 'N/A')}\n\n"
        for section in data.get("general_sections", []):
            full_text_content += f"### {section['title']}\n{section['content']}\n\n"
        
        if "technology_matrix" in data:
            full_text_content += "### Technology Matrix\n"
            full_text_content += json.dumps(data.get("technology_matrix"), indent=2)

        # Fallback for simpler files (About Us / Contact)
        if not full_text_content.strip() or full_text_content == "Program: N/A\n\n":
            full_text_content = json.dumps(data, indent=2)

        # Generate Embedding
        vectors = embedding.embed_model.embed_documents([full_text_content])
        vector = vectors[0]

        # Use the relative path as ID so it's consistent across PCs
        collection.upsert(
            ids=[relative_id],
            documents=[full_text_content],
            embeddings=[vector],
            metadatas=[{"source": relative_id}]
        )
        print(f"Added: {relative_id}")
        
    except Exception as e:
        print(f"Error processing {relative_id}: {e}")

# --- MAIN EXECUTION: Recursively find all JSON files ---
print(f"Scanning for data in: {base_data_path}")

# os.walk traverses every subfolder shown in your screenshot
for root, dirs, files in os.walk(base_data_path):
    for file in files:
        if file.endswith(".json"):
            # Full path for opening the file
            full_file_path = os.path.join(root, file)
            # Relative path for the ID (e.g., 'Internship_Scrap/sunbeam_internship_full.json')
            relative_id = os.path.relpath(full_file_path, base_data_path)
            
            store_db(full_file_path, relative_id)

print("\nIngestion complete. The database is now shared-ready.")

def search_resume(job_description, top_k):
    # Use the same model object here as well
    query_vector = embedding.embed_model.embed_query(job_description)
    search_results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return search_results