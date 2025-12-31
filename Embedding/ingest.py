import os
import json
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_core.documents import Document
import embedding # Assuming this contains your embed_model

# --- 1. SETUP PATHS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
base_data_path = os.path.abspath(os.path.join(script_dir, "..", "Scraped_data"))
DB_DIR = "./knowledgebase"

# --- 2. OPTIMIZED SPLITTER ---
# INCREASED max_chunk_size to 1200 to keep JSON objects (like addresses) together.
json_splitter = RecursiveJsonSplitter(max_chunk_size=1200)

print(f"🚀 Scanning for Sunbeam data in: {base_data_path}")

all_documents = []

# --- 3. PROCESSING WITH CONTEXTUAL HEADERS ---
for root, dirs, files in os.walk(base_data_path):
    for file in files:
        if file.endswith(".json"):
            full_file_path = os.path.join(root, file)
            relative_id = os.path.relpath(full_file_path, base_data_path)
            category = relative_id.split(os.sep)[0] 

            try:
                with open(full_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Split JSON into larger, meaningful chunks
                chunks = json_splitter.split_json(json_data=data)
                
                for i, chunk in enumerate(chunks):
                    chunk_text = json.dumps(chunk)
                    
                    # IMPROVEMENT: Add a descriptive header to the chunk text.
                    # This helps the Vector Search 'understand' what this JSON is about.
                    descriptive_header = f"Sunbeam Infotech {category.replace('_', ' ')} Details: "
                    final_text_for_embedding = descriptive_header + chunk_text
                    
                    # Apply your Nomic storage prefix (from your previous embedding logic)
                    prefixed_text = embedding.embed_for_storage(final_text_for_embedding)
                    
                    doc = Document(
                        page_content=prefixed_text,
                        metadata={
                            "source": relative_id,
                            "category": category,
                            "chunk_index": i
                        }
                    )
                    all_documents.append(doc)
                
                print(f"✅ Processed: {relative_id} ({len(chunks)} chunks)")

            except Exception as e:
                print(f"❌ Error processing {relative_id}: {e}")

# --- 4. CLEAR AND STORE IN CHROMADB ---
if all_documents:
    # Logic to clear old data if it exists
    if os.path.exists(DB_DIR):
        print("🧹 Clearing existing database for a fresh start...")
        import shutil
        shutil.rmtree(DB_DIR)

    print(f"\n📦 Storing {len(all_documents)} chunks in ChromaDB...")
    
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embedding.embed_model,
        persist_directory=DB_DIR,
        collection_name="sunbeam_data"
    )
    print("✨ Ingestion complete! The Agent now has better context for your queries.")
else:
    print("⚠️ No valid JSON files found.")