import streamlit as st
import os
import sys
import json
import uuid
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from Css import local_css

# --- 1. SYSTEM PATH CONFIGURATION ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from LLM.Agent_Call import chat_with_guru
except ImportError:
    def chat_with_guru(query, history):
        return "Backend not connected. Please ensure LLM/Agent_Call.py exists."

load_dotenv()

# --- 2. STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Sunbeam ChatBot | Academic Assistant",
    page_icon="🎓",
    layout="wide"
)


# --- 4. DATA PERSISTENCE & STATE ---
HISTORY_FILE = "chat_history.json"

def load_all_chats():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_all_chats(chats):
    with open(HISTORY_FILE, "w") as f:
        json.dump(chats, f)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_all_chats()

if "active_chat_id" not in st.session_state:
    if not st.session_state.all_chats:
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {"title": "New Session", "messages": [], "created_at": str(datetime.now())}
        st.session_state.active_chat_id = new_id
    else:
        sorted_chats = sorted(st.session_state.all_chats.items(), key=lambda x: x[1].get('created_at', ''), reverse=True)
        st.session_state.active_chat_id = sorted_chats[0][0]

# --- 5. AGENT ADAPTER ---
def get_neural_response_wrapper(user_query, active_messages):
    langchain_history = []
    for msg in active_messages[-6:]:
        if msg["role"] == "user":
            langchain_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_history.append(AIMessage(content=msg["content"]))
    
    return chat_with_guru(user_query, langchain_history)

# --- 6. UI COMPONENTS ---
def render_user_ui(local_css): 
    local_css()
    
    user_icon = "https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
    guru_icon = "https://i.pinimg.com/736x/02/06/d4/0206d47d83e1030d7ea44b8f511c3c3a.jpg"
    
    with st.sidebar:
        st.image("https://sunbeaminfo.in/img/new/new_logo.png", width=140)
        st.markdown("<h3 style='color: #f8fafc; margin-bottom: 10px;'>Neural History</h3>", unsafe_allow_html=True)
        
        if st.button("➕ New Chat", use_container_width=True):
            new_id = str(uuid.uuid4())
            st.session_state.all_chats[new_id] = {"title": "New Session", "messages": [], "created_at": str(datetime.now())}
            st.session_state.active_chat_id = new_id
            save_all_chats(st.session_state.all_chats)
            st.rerun()
        
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.all_chats = {}
            if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
            st.rerun()

        st.divider()
        
        # Chat History List
        sorted_chats = sorted(st.session_state.all_chats.items(), key=lambda x: x[1].get('created_at', ''), reverse=True)
        for chat_id, chat_data in sorted_chats:
            is_active = chat_id == st.session_state.active_chat_id
            btn_label = f"💬 {chat_data['title']}"
            
            if st.button(btn_label, key=chat_id, use_container_width=True, help=chat_data['created_at']):
                st.session_state.active_chat_id = chat_id
                st.rerun()

        st.divider()

    # --- MAIN CHAT AREA ---
    active_chat = st.session_state.all_chats.get(st.session_state.active_chat_id)
    if not active_chat:
        st.info("Please select or create a chat session.")
        return

    st.markdown(f"<h1 class='main-header' style='text-align: center;'>Sunbeam ChatBot</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Active Session: {active_chat['title']}</p>", unsafe_allow_html=True)
    st.divider()

    # Display Chat History
    for msg in active_chat["messages"]:
        css_class = "user" if msg["role"] == "user" else "assistant"
        icon_url = user_icon if msg["role"] == "user" else guru_icon
        display_content = msg["content"].replace('\n', '<br>')
        display_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', display_content)
        
        st.markdown(f"""
            <div class="message-row {css_class}">
                <div class="message-avatar"><img src="{icon_url}"></div>
                <div class="message-bubble">
                    <div class="message-content">{display_content}</div>
                    <span class="message-time">{msg.get('time', '')}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- CHAT INPUT ---
    if prompt := st.chat_input("Enter your academic inquiry..."):
        curr_time = datetime.now().strftime("%I:%M %p")
        
        # Add User Message
        active_chat["messages"].append({"role": "user", "content": prompt, "time": curr_time})
        
        # Update Title if it's the first message
        if active_chat["title"] == "New Session":
            active_chat["title"] = prompt[:25] + ("..." if len(prompt) > 25 else "")
        
        save_all_chats(st.session_state.all_chats)
        st.rerun()

    # --- ASSISTANT LOGIC ---
    if active_chat["messages"] and active_chat["messages"][-1]["role"] == "user":
        with st.spinner("Analyzing request..."):
            answer = get_neural_response_wrapper(active_chat["messages"][-1]["content"], active_chat["messages"])
            
            active_chat["messages"].append({
                "role": "assistant", 
                "content": answer, 
                "time": datetime.now().strftime("%I:%M %p")
            })
            save_all_chats(st.session_state.all_chats)
            st.rerun()

if __name__ == "__main__":
    render_user_ui(local_css)