import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

# --- 1. CONFIGURATION ---
# Using absolute paths to prevent "directory not found" errors
script_dir = os.path.dirname(os.path.abspath(__file__)) # Utility folder
project_root = os.path.abspath(os.path.join(script_dir, ".."))

SCRAPED_DATA_PATH = os.path.join(project_root, "Scraped_data")
SUMMARIES_OUTPUT_PATH = os.path.join(project_root, "Summarized_data")

os.makedirs(SUMMARIES_OUTPUT_PATH, exist_ok=True)

# Get API Key from environment
groq_key = os.getenv("groq_api_key")

# Initialize the LLM
llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_key,
    temperature=0
)

# --- 2. SUMMARIZATION UTILITIES ---

def generate_summary(content: str, prompt: str):
    """Generic utility to call the LLM for high-density summarization."""
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=content)
    ]
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error summarizing: {str(e)}"

# --- 3. TASK 1: MASTER MODULAR SUMMARY ---

def summarize_modular_courses():
    """Consolidates all individual modular course JSONs into one Master file."""
    modular_dir = os.path.join(SCRAPED_DATA_PATH, "Modular_courses")
    
    if not os.path.exists(modular_dir):
        print(f"⚠️ Modular courses directory not found at: {modular_dir}")
        return

    all_summaries = []
    print(f"📂 Consolidating Modular Course files from {modular_dir}...")
    
    files = [f for f in os.listdir(modular_dir) if f.endswith(".json")]
    if not files:
        print("⚠️ No JSON files found in Modular_courses!")
        return

    for file_name in files:
        file_path = os.path.join(modular_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        
        prompt = (
            f"Summarize the technical details for course: {file_name}. "
            "Capture: Course Name, exact Fees (from summary string), Duration, "
            "and a bulleted list of high-level Syllabus modules. "
            "Keep it precise so an AI Agent can use it as a reference."
        )
        
        course_summary = generate_summary(data, prompt)
        all_summaries.append(f"--- MODULAR COURSE: {file_name} ---\n{course_summary}\n")
        print(f"   ✔ Summarized: {file_name}")

    output_file = os.path.join(SUMMARIES_OUTPUT_PATH, "Modular_Master_Summary.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_summaries))
    print(f"✅ Saved MASTER MODULAR SUMMARY to: {output_file}")

# --- 4. TASK 2: GENERAL KNOWLEDGE SUMMARY (About, Contact, Pre-CAT, MCQs) ---
def summarize_modular_courses():
    """Consolidates all individual modular course JSONs into one Master file."""
    modular_dir = os.path.join(SCRAPED_DATA_PATH, "Modular_courses")
    
    if not os.path.exists(modular_dir):
        print(f"⚠️ Modular courses directory not found at: {modular_dir}")
        return

    all_summaries = []
    print(f"📂 Consolidating Modular Course files from {modular_dir}...")
    
    files = [f for f in os.listdir(modular_dir) if f.endswith(".json")]
    if not files:
        print("⚠️ No JSON files found in Modular_courses!")
        return

    for file_name in files:
        file_path = os.path.join(modular_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        
        prompt = (
            f"Summarize the technical details for course: {file_name}. "
            "Capture: Course Name, exact Fees (from summary string), Duration, "
            "and a bulleted list of high-level Syllabus modules. "
            "Keep it precise so an AI Agent can use it as a reference."
        )
        
        course_summary = generate_summary(data, prompt)
        all_summaries.append(f"--- MODULAR COURSE: {file_name} ---\n{course_summary}\n")
        print(f"   ✔ Summarized: {file_name}")

    output_file = os.path.join(SUMMARIES_OUTPUT_PATH, "Modular_Master_Summary.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_summaries))
    print(f"✅ Saved MASTER MODULAR SUMMARY to: {output_file}")

# --- 4. TASK 2: INDIVIDUAL FILE SUMMARIZATION (One Summary Per File) ---

def summarize_file_to_file():
    """Generates an individual .txt summary for every .json file in the target categories."""
    target_categories = ["aboutUS", "contactUS", "Pre-CAT", "Mastering_mcqs", "Internship_Scrap"]
    
    print("📂 Starting Individual File Summarization (One-to-One)...")
    
    for category in target_categories:
        cat_path = os.path.join(SCRAPED_DATA_PATH, category)
        output_cat_path = os.path.join(SUMMARIES_OUTPUT_PATH, category)
        
        if not os.path.exists(cat_path):
            print(f"   ⏩ Skipping {category} (folder not found)")
            continue
        
        os.makedirs(output_cat_path, exist_ok=True)
            
        for file_name in os.listdir(cat_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(cat_path, file_name)
                # Create a matching .txt filename for the summary
                output_file_name = file_name.replace(".json", "_summary.txt")
                output_file_path = os.path.join(output_cat_path,output_file_name)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # REASONING-FIRST PROMPT:
                # Forces the LLM to scan the entire document before committing to a summary.
                prompt = (
            "You are a specialized technical content analyzer for Sunbeam Infotech. "
            f"Analyze the following Modular Course JSON for: {file_name}.\n\n"
            "YOUR TASK:\n"
            "1. COURSE OVERVIEW: Start with a brief 1-2 sentence description of what this course is about and its primary goal.\n"
            "2. KEY DATA EXTRACTION: Extract the following into clear bullet points:\n"
            "   - Official Course Name\n"
            "   - Exact Fees (Search for 'summary' or 'fee' fields)\n"
            "   - Course Duration and Timings\n"
            "   - Technical Syllabus (Grouped into logical modules)\n"
            "   - Target Audience and Prerequisites\n\n"
            "CRITICAL: Be precise. If a specific fee or duration is found, include it exactly as written. "
            "Use bullet points for all extracted data to ensure an AI Agent can easily parse it."
        )
                
                summary_content = generate_summary(json.dumps(data), prompt)
                
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(summary_content)
                
                print(f"   ✔ Generated individual summary for: {file_name} -> {output_file_name}")

    print(f"✅ One-to-one summarization complete. Check folders in: {SUMMARIES_OUTPUT_PATH}")


# --- 5. EXECUTION ---
if __name__ == "__main__":
   # summarize_modular_courses()
    summarize_file_to_file()