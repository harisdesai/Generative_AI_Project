import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import embedding 

load_dotenv()

# --- 1. VECTOR STORE CONNECTION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.abspath(os.path.join(script_dir, "..", "Embedding", "knowledgebase"))

print(f"Attempting to connect to database at: {DB_DIR}")

vectorstore = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embedding.embed_model,
    collection_name="sunbeam_data"
)

# Debugging: Quick check of document count
try:
    count = vectorstore._collection.count()
    print(f" Database Status: SUCCESS! {count} documents found.")
except Exception as e:
    print(f" Database Status: Error connecting to collection - {e}")

# --- 2. DEFINE SPECIALIZED TOOLS ---

@tool
def list_all_offerings(category_type: Optional[str] = None) -> str:
    """
    Use this tool ONLY when the user wants a list of ALL courses or ALL categories.
    Args:
        category_type: Optional filter. Use 'modular_split' for Modular courses or 'summary_file' for individual summaries.
    """
    print(f" [Tool] Listing all offerings for type: {category_type}")
    
    # We fetch more documents here (k=20) because listing requires high recall
    # We use metadata filtering if the agent provides a type
    search_filter = {"type": category_type} if category_type else None
    results = vectorstore.get(where=search_filter)
    
    if not results or not results['metadatas']:
        return "No offerings found in the database."

    # Extract unique categories from metadata to create a clean list
    categories = sorted(list(set([m.get('category') for m in results['metadatas']])))
    return "Available Sunbeam Offerings:\n- " + "\n- ".join(categories)

@tool
def search_course_details(query: str, specific_category: Optional[str] = None) -> str:
    """
    Search for technical course details including syllabus, fees, and duration.
    Args:
        query: The search term.
        specific_category: Optional category name if the user mentioned a specific course (e.g., 'Core Java').
    """
    print(f" [Tool] Searching Course: '{query}' in Category: {specific_category}")
    
    # If a specific category is known, we filter by it to be 100% accurate
    search_filter = {"category": specific_category} if specific_category else None
    
    # MMR search for diversity
    results = vectorstore.max_marginal_relevance_search(
        query, 
        k=5, 
        fetch_k=20, 
        filter=search_filter
    )
    
    if not results:
        return f"No specific details found for '{query}'."

    formatted_results = []
    for i, d in enumerate(results):
        cat = d.metadata.get('category', 'General')
        formatted_results.append(f"--- SOURCE: {cat} ---\n{d.page_content}")
    
    return "\n\n".join(formatted_results[0:4])

@tool
def search_sunbeam_info(query: str) -> str:
    """Search for general info: Address, Contacts, About Us, and Internships."""
    print(f"[Tool] Searching General Info: '{query}'")
    results = vectorstore.similarity_search(query, k=6)
    
    if not results:
        return "No general information found."

    formatted_results = []
    for i, d in enumerate(results):
        cat = d.metadata.get('category', 'General')
        formatted_results.append(f"--- SOURCE: {cat} ---\n{d.page_content}")
    
    return "\n\n".join(formatted_results[0:5])  # Limit to top 5 results

tools = [list_all_offerings, search_course_details, search_sunbeam_info]

# --- 3. INITIALIZE LLM ---
# llm = init_chat_model(
#     model="llama-3.3-70b-versatile",
#     model_provider="openai",
#     base_url="https://api.groq.com/openai/v1",
#     api_key=os.getenv("groq_api_key"),
#     temperature=0
# )

# llm = init_chat_model(
#     model="llama-3.1-8b-instant",
#     model_provider="openai",
#     base_url="https://api.groq.com/openai/v1",
#     api_key=os.getenv("groq_api_key"),
#     temperature=0
# )

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key= "no-needed",
    temperature=0
)


# llm = init_chat_model(
#     model="llama-3.3-70b-versatile",
#     model_provider= "openai",
#     base_url = "https://api.groq.com/openai/v1",
#     api_key = os.getenv("groq_api_key"),
#     temperature=0
# )

# --- 4. THE GURU SYSTEM PROMPT ---
SYSTEM_PROMPT = (
    "You are the 'Sunbeam Guru', a strictly data-driven counselor for Sunbeam Infotech.\n\n"
    "### TOOL USAGE STRATEGY:\n"
    "1. LISTING: If the user asks 'list all courses' or 'what modular courses do you have?', use 'list_all_offerings'.\n"
    "2. SPECIFIC SEARCH: If they ask about a specific course (e.g., 'Spark fee'), use 'search_course_details'.\n"
    "3. DISCOVERY: If you've listed the courses and the user picks one, use 'search_course_details' with the 'specific_category' filter.\n\n"
    "### MANDATORY INSTRUCTIONS:\n"
    "- Rely ONLY on retrieved data. If a tool returns ₹14,900, say ₹14,900.\n"
    "- If a user asks a conceptual question (e.g., 'What is a Lambda in Java?'), answer directly using your own knowledge.\n"
    "- For all Sunbeam-specific facts (fees, syllabus, address), you MUST use tools.\n"
    "- Refuse non-academic/non-Sunbeam queries politely."
    " - never use any tool that is not listed in your toolset.\n"
    " - never give imaginary answers. those which are not supported by the data in the knowledge base.\n"
    " - always give answers in proper format and readable manner.\n"
)

# --- 5. CREATE THE AGENT ---
agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)

# --- 6. CHAT ROUTING LOGIC ---
def chat_with_guru(user_input: str, history: List):
    user_query = user_input.lower().strip()
    
    # Trigger keywords for data retrieval
    needs_data = ["fee", "cost", "price", "syllabus", "list", "batch", "address", 
                  "contact", "phone", "internship", "cat", "pre-cat", "course"]
    
    if any(word in user_query for word in needs_data):
        print(f"[Agent] Routing to Tool Path: '{user_input}'")
        clean_history = []
        for msg in history:
            if isinstance(msg, (HumanMessage, AIMessage)):
                if isinstance(msg, AIMessage):
                    msg.tool_calls = []
                clean_history.append(msg)

        input_data = {"messages": clean_history + [HumanMessage(content=user_input)]}
        
        try:
            response = agent.invoke(input_data)
            return response["messages"][-1].content
        except Exception as e:
            print(f"[Agent] Error: {e}")
            fallback_res = vectorstore.similarity_search(user_input, k=5)
            context = "\n\n".join([f"[{d.metadata.get('category')}]: {d.page_content}" for d in fallback_res])
            messages = [
                SystemMessage(content=SYSTEM_PROMPT + "\n\nCONTEXT:\n" + context),
                HumanMessage(content=user_input)
            ]
            return llm.invoke(messages).content

    # Greetings / Small Talk / Conceptual Q&A
    print(f"[Agent] Routing to Direct Chat Path.")
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + history + [HumanMessage(content=user_input)]
    return llm.invoke(messages).content

# --- 7. RUNTIME ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Sunbeam ChatBot (Production Mode) is Online!")
    print("="*50 + "\n")
    
    chat_history = [] 

    while True:
        u_in = input("Student: ")
        if u_in.lower() in ["exit", "quit"]: break
        
        ans = chat_with_guru(u_in, chat_history)
        print(f"\nSunbeam ChatBot: {ans}\n" + "-"*30)
        
        chat_history.append(HumanMessage(content=u_in))
        chat_history.append(AIMessage(content=ans))
        if len(chat_history) > 6: chat_history = chat_history[-6:]

        