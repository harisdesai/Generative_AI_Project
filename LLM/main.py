import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import embedding 

# --- INITIAL LOAD ---
load_dotenv()

# --- 1. RAG RESOURCES ---
@st.cache_resource
def load_rag_system():
    vectorstore = Chroma(
        persist_directory="./knowledgebase",
        embedding_function=embedding.embed_model,
        collection_name="sunbeam_data"
    )
    llm = init_chat_model(
        model="llama-3.3-70b-versatile",
        model_provider="openai",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("groq_api_key"),
        temperature=0
    )
    return vectorstore, llm

vectorstore, llm = load_rag_system()

# --- 2. RAG LOGIC ---
def get_neural_response(user_query):
    prefixed_query = f"search_query: {user_query}"
    docs = vectorstore.similarity_search(prefixed_query, k=6)
    sources = sorted(list(set([doc.metadata.get('source', 'Unknown') for doc in docs])))
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    prompt_template = ChatPromptTemplate.from_template("""
    You are a professional Sunbeam Pune Assistant. Use the context below to answer accurately.
    Context: {context}
    Question: {question}
    """)
    
    formatted_prompt = prompt_template.format(context=context_text, question=user_query)
    response = llm.invoke(formatted_prompt)
    return response.content, sources

# --- 3. UI STYLING (Left-Right + Hover Animations) ---
def style_func():
    st.markdown("""
        <style>
        /* Neon Header */
        .neon-glow {
            color: #00f2ff;
            text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Base Chat Bubble Style */
        [data-testid="stChatMessage"] {
            border-radius: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(0, 242, 255, 0.2);
            width: fit-content;
            max-width: 80%;
            transition: all 0.3s ease-in-out; /* Smooth transition for hover */
            position: relative;
        }

        /* Hover Animation: Scale and Glow */
        [data-testid="stChatMessage"]:hover {
            transform: translateY(-2px) scale(1.01);
            border-color: #00f2ff !important;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
            z-index: 10;
        }

        /* User Message (Right Align) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            margin-left: auto !important;
            background-color: rgba(0, 242, 255, 0.1) !important;
            border-right: 4px solid #00f2ff !important;
        }

        /* Assistant Message (Left Align) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
            margin-right: auto !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-left: 4px solid #00f2ff !important;
        }

        /* Spinner Styling */
        .stSpinner > div {
            border-top-color: #00f2ff !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 4. THE UI RENDERER ---
def render_user_ui(style_func): 
    style_func() 
    
    with st.sidebar:
        st.markdown("<h2 class='neon-glow'>SYSTEM OPS</h2>", unsafe_allow_html=True)
        st.divider()
        st.subheader("🛠️ Interface Controls")
        if st.button("Clear Neural History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
    st.markdown("<h1 class='neon-glow' style='text-align: center;'>Neural Interface v4.0</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Container
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            st.caption(f"{msg.get('time', '')}")

    # --- INPUT SECTION ---
    if prompt := st.chat_input("Input command..."):
        curr_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": prompt, "time": curr_time})
        st.rerun()

    # --- ASSISTANT LOGIC ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Decoding Neural Pathways..."):
                user_input = st.session_state.messages[-1]["content"]
                answer, sources = get_neural_response(user_input)
                
                st.markdown(answer)
                if sources:
                    with st.markdown("📚 Data Sources"):
                        for s in sources:
                            st.write(f"- {s}")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "sources": sources,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

if __name__ == "__main__":
    render_user_ui(style_func)