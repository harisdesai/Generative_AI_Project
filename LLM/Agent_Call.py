import os
import time
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import embedding 

load_dotenv()

# --- 1. KNOWLEDGE BASE ---
vectorstore = Chroma(
    persist_directory="./knowledgebase",
    embedding_function=embedding.embed_model,
    collection_name="sunbeam_data"
)

# --- 2. THE 4 PILLAR TOOLS ---

def search_internship(query: str):
    """Accesses Internship data (₹4,000/-). Covers: Generative AI, MERN, Java, .NET, Python, Web Dev, etc."""
    results = vectorstore.similarity_search(query, k=5, filter={"category": "Internship_Scrap"})
    return "\n\n".join([d.page_content for d in results])

def search_modular(query: str):
    """
    Accesses Modular Course data. 
    12 Courses: Java Mastery, .NET Mastery, MERN Stack, Mean Stack, Python, PHP/Laravel, 
    DevOps, Apache Spark, Android, Software Testing, C++ Programming, and SQL.
    """
    results = vectorstore.similarity_search(query, k=15, filter={"category": "Modular_courses"})
    return "\n\n".join([d.page_content for d in results])

def search_precat(query: str):
    """Accesses Pre-CAT data for C-DAC entrance exam preparation."""
    results = vectorstore.similarity_search(query, k=3, filter={"category": "Pre-CAT"})
    return "\n\n".join([d.page_content for d in results])

def search_mcq(query: str):
    """Accesses Mastering MCQ and Campus Placement Preparation data."""
    results = vectorstore.similarity_search(query, k=3, filter={"category": "Mastering_mcqs"})
    return "\n\n".join([d.page_content for d in results])

# --- 3. THE GURU LOGIC ---

llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api_key"),
    temperature=0
)

# System Message as a formal object
SYSTEM_MSG = SystemMessage(content="""
You are the Sunbeam Guru. Strictly follow these rules:
1. GREETINGS: Respond normally to 'hi' or 'hello'.
2. AMBIGUITY (CRITICAL): If a user asks for 'Java', '.NET', 'MERN', or 'Python' without 
   specifying, ASK: "Are you interested in the 1-month Internship (₹4,000) or the Modular Course?"
3. FEES: If fees are asked, check both general info and batch schedules within the specific data.
4. SCOPE: Only answer about Sunbeam Infotech.
""")

def get_guru_response(user_input, history):
    # history is now a list of Message objects
    
    # 1. Decide if we need a tool or just chat
    # Note: We check user_input for intent
    context = ""
    if any(word in user_input.lower() for word in ["internship", "project"]):
        context = search_internship(user_input)
    elif any(word in user_input.lower() for word in ["java", "mern", "spark", "modular", "dotnet", "cpp"]):
        # Check for ambiguity first
        if "internship" not in user_input.lower() and "modular" not in user_input.lower():
            return "I see you're interested in that tech! Are you looking for the 1-month Internship (₹4,000) or the deep-dive Modular course?"
        context = search_modular(user_input)
    elif "cat" in user_input.lower() or "entrance" in user_input.lower():
        context = search_precat(user_input)
    elif "mcq" in user_input.lower() or "placement" in user_input.lower():
        context = search_mcq(user_input)
    else:
        # General chat/About/Contact
        res = vectorstore.similarity_search(user_input, k=3, filter={"category": {"$in": ["aboutUS", "contactUS"]}})
        context = "\n\n".join([d.page_content for d in res])

    # 2. Build the full message list for LangChain
    # We combine: [System Message] + [History] + [Current User Prompt + Context]
    context_aware_prompt = f"Context from Sunbeam Data:\n{context}\n\nUser Question: {user_input}"
    
    messages = [SYSTEM_MSG] + history + [HumanMessage(content=context_aware_prompt)]
    
    # 3. Generate response
    response = llm.invoke(messages)
    return response.content

# --- 4. EXECUTION ---
print("🚀 Sunbeam Guru is Online! (Fixed History Management)")
chat_history = []  # Changed from string to list

while True:
    u_in = input("\nStudent: ")
    if u_in.lower() in ["exit", "quit"]: break
    
    ans = get_guru_response(u_in, chat_history)
    print(f"\nSunbeam Guru: {ans}")
    
    # Append the turn to history for the next iteration
    chat_history.append(HumanMessage(content=u_in))
    chat_history.append(AIMessage(content=ans))
    
    # Optional: Keep history manageable by trimming if it gets too long
    if len(chat_history) > 10:  # Keeps last 5 turns
        chat_history = chat_history[-10:]