import os
import re
from langchain_chroma import Chroma
from langchain_core.documents import Document
import embedding

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))

base_data_path = os.path.join(project_root, "Summarized_data")
DB_DIR = os.path.join(project_root, "Embedding", "knowledgebase")

MASTER_FILE_NAME = "Modular_Master_Summary.txt"

print(f"Project Root Detected: {project_root}")
print(f"Scanning data from: {base_data_path}")
print(f"Database Target: {DB_DIR}")

if not os.path.exists(base_data_path):
    print(f"ERROR: The path {base_data_path} does not exist.")
    exit()

all_documents = []

def process_text_file(file_path, file_name, relative_id):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if file_name == MASTER_FILE_NAME:
        parts = re.split(r'(--- MODULAR COURSE: .*? ---)', content)
        current_course_header = "General Modular Info"
        for part in parts:
            if not part.strip(): continue
            if part.startswith("--- MODULAR COURSE:"):
                raw_header = part.replace("--- MODULAR COURSE:", "").replace("---", "").strip()
                current_course_header = raw_header.replace(".json", "").replace(".txt", "").replace("_", " ")
                continue
            
            course_text = part.strip()
            category = current_course_header
            descriptive_header = f"Sunbeam Infotech {category} Details: "
            final_text = embedding.embed_for_storage(descriptive_header + course_text)

            all_documents.append(Document(
                page_content=final_text,
                metadata={"source": relative_id, "category": category, "type": "modular_split"}
            ))
            print(f"Processed Category: {category}")

    else:
        category = file_name.replace(".txt", "").replace("_", " ").replace("Summary", "").strip()
        descriptive_header = f"Sunbeam Infotech {category} Summary: "
        final_text = embedding.embed_for_storage(descriptive_header + content)
        all_documents.append(Document(
            page_content=final_text,
            metadata={"source": relative_id, "category": category, "type": "summary_file"}
        ))
        print(f"Processed File: {file_name}")

for root, dirs, files in os.walk(base_data_path):
    for file in files:
        if file.endswith(".txt"):
            full_path = os.path.join(root, file)
            rel_id = os.path.relpath(full_path, base_data_path)
            process_text_file(full_path, file, rel_id)

if all_documents:
    if os.path.exists(DB_DIR):
        print("Clearing existing collection...")
        try:
            vectorstore = Chroma(
                persist_directory=DB_DIR,
                embedding_function=embedding.embed_model,
                collection_name="sunbeam_data"
            )
            vectorstore.delete_collection()
            print("Collection cleared successfully.")
        except Exception as e:
            print(f"Note during reset: {e} (Will attempt to overwrite)")

    print(f"Storing {len(all_documents)} items in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embedding.embed_model,
        persist_directory=DB_DIR,
        collection_name="sunbeam_data"
    )
    
    final_count = vectorstore._collection.count()
    print(f"Ingestion complete! {final_count} items successfully verified in database.")
else:
    print("No valid .txt files found in Summarized_data.")