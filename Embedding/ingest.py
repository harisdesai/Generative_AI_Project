import os
import json
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_core.documents import Document
import embedding # Ensure this is your updated embedding.py with Nomic prefixes

# --- 1. SETUP PATHS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Adjust this path to point to your 'Scraped_data' folder
base_data_path = os.path.abspath(os.path.join(script_dir, "..", "Scraped_data"))
DB_DIR = "./knowledgebase"

# --- 2. INITIALIZE THE SPLITTER ---
# max_chunk_size=500 is ideal for keeping JSON key-value pairs together
json_splitter = RecursiveJsonSplitter(max_chunk_size=500)

print(f"🚀 Scanning for Sunbeam data in: {base_data_path}")

all_documents = []

# --- 3. RECURSIVELY PROCESS FILES WITH METADATA ---
for root, dirs, files in os.walk(base_data_path):
    for file in files:
        if file.endswith(".json"):
            full_file_path = os.path.join(root, file)
            
            # relative_id: e.g., 'Internship_Scrap/sunbeam_internship_full.json'
            relative_id = os.path.relpath(full_file_path, base_data_path)
            
            # CATEGORY EXTRACTION: Extracts the folder name (e.g., 'Modular_courses')
            # This is critical for Agentic RAG filtering
            category = relative_id.split(os.sep)[0] 

            try:
                with open(full_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Split the JSON into smaller, manageable chunks
                chunks = json_splitter.split_json(json_data=data)
                
                for i, chunk in enumerate(chunks):
                    # Convert JSON chunk to string and apply Nomic storage prefix
                    chunk_text = json.dumps(chunk)
                    prefixed_text = embedding.embed_for_storage(chunk_text)
                    
                    # Create Document with enriched metadata
                    doc = Document(
                        page_content=prefixed_text,
                        metadata={
                            "source": relative_id,
                            "category": category, # The 'Map' for your Agent
                            "chunk_index": i
                        }
                    )
                    all_documents.append(doc)
                
                print(f"✅ Chunked: {relative_id} | Category: {category} ({len(chunks)} chunks)")

            except Exception as e:
                print(f"❌ Error processing {relative_id}: {e}")

# --- 4. STORE IN CHROMADB ---
if all_documents:
    print(f"\n📦 Storing {len(all_documents)} chunks in ChromaDB...")
    
    # This automatically embeds and saves the documents to disk
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embedding.embed_model,
        persist_directory=DB_DIR,
        collection_name="sunbeam_data"
    )
    print("✨ Ingestion complete! Your Agent can now use 'category' filters.")
else:
    print("⚠️ No valid JSON files found. Check your 'Scraped_data' folder structure.")