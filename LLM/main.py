import streamlit as st
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import embedding 

load_dotenv()

# --- 1. SETUP DATABASE ---
vectorstore = Chroma(
    persist_directory="./knowledgebase",
    embedding_function=embedding.embed_model,
    collection_name="sunbeam_data"
)

# --- 2. SETUP LLM ---
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api_key"),
    temperature=0
)

# --- 3. RAG LOGIC ---
def get_answer(user_query):
    # Apply Nomic prefix for the search
    prefixed_query = f"search_query: {user_query}"
    
    # Increase k to 6 because chunks are now smaller
    docs = vectorstore.similarity_search(prefixed_query, k=6)
    
    # Extract source files for citations
    sources = sorted(list(set([doc.metadata.get('source', 'Unknown') for doc in docs])))
    
    # Combine content
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    prompt_template = ChatPromptTemplate.from_template("""
    You are a professional Sunbeam Pune Assistant. Use the context below to answer accurately.
    Explain things in your own words. If the info is missing, say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """)
    
    formatted_prompt = prompt_template.format(context=context_text, question=user_query)
    response = llm.invoke(formatted_prompt)
    
    return response.content, sources

# --- 4. STREAMLIT UI ---
st.set_page_config(page_title="Sunbeam AI", page_icon="🎓")
st.title("Sunbeam Course Advisor 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about fees, batches, or courses..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching Sunbeam records..."):
            answer, sources = get_answer(prompt)
            
            st.markdown(answer)
            
            # Display source citations at the bottom
            if sources:
                with st.expander("📚 Sources Used"):
                    for s in sources:
                        st.write(f"- {s}")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})