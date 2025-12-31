import os
import json
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_core.documents import Document
import embedding # Uses your updated file with prefixes

# 1. SETUP PATHS
script_dir = os.path.dirname(os.path.abspath(__file__))
# Points to your Scraped_data folder one level up
base_data_path = os.path.abspath(os.path.join(script_dir, "..", "Scraped_data"))
DB_DIR = "./knowledgebase"

# 2. INITIALIZE THE SPLITTER
# max_chunk_size=500 keeps batch info, fees, and syllabus items together
json_splitter = RecursiveJsonSplitter(max_chunk_size=500)

print(f"Scanning for data in: {base_data_path}")

all_documents = []

# 3. RECURSIVELY FIND AND CHUNK JSON FILES
for root, dirs, files in os.walk(base_data_path):
    for file in files:
        if file.endswith(".json"):
            full_file_path = os.path.join(root, file)
            # relative_id is used for metadata (e.g., 'Internship/mern.json')
            relative_id = os.path.relpath(full_file_path, base_data_path)

            try:
                with open(full_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Split the JSON into meaningful smaller chunks
                chunks = json_splitter.split_json(json_data=data)
                
                # Convert chunks into LangChain Documents
                for i, chunk in enumerate(chunks):
                    # CONVERT JSON CHUNK TO STRING
                    chunk_text = json.dumps(chunk)
                    
                    # APPLY NOMIC PREFIX FROM YOUR EMBEDDING FILE
                    # This tells the model: "This is a document to be searched later"
                    prefixed_text = embedding.embed_for_storage(chunk_text)
                    
                    doc = Document(
                        page_content=prefixed_text,
                        metadata={
                            "source": relative_id,
                            "chunk_index": i
                        }
                    )
                    all_documents.append(doc)
                
                print(f"✅ Chunked: {relative_id} ({len(chunks)} chunks)")

            except Exception as e:
                print(f"❌ Error processing {relative_id}: {e}")

# 4. STORE IN CHROMADB
if all_documents:
    print(f"\nStoring {len(all_documents)} chunks in ChromaDB...")
    
    # We pass your embed_model object. 
    # Chroma will automatically call its embed_documents method on our prefixed text.
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embedding.embed_model,
        persist_directory=DB_DIR,
        collection_name="sunbeam_data"
    )
    print("🚀 Ingestion complete! The database is optimized with Nomic prefixes.")
else:
    print("⚠️ No valid JSON files found. Check your 'Scraped_data' folder.")