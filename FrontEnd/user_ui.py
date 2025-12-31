import streamlit as st
import time
from datetime import datetime

def render_user_ui(style_func): 
    style_func() 
    
    # --- SIDEBAR CONTROL PANEL ---
    with st.sidebar:
        st.divider()
        st.subheader("🛠️ Interface Controls")
        if st.button("Clear Neural History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
    # --- MAIN INTERFACE ---
    st.markdown("<h1 class='neon-glow' style='text-align: center;'>Neural Interface v4.0</h1>", unsafe_allow_html=True)
    
    # Centered conversation area
    _, chat_col, _ = st.columns([1, 5, 1])
    
    with chat_col:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Render message history with timestamps
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                # Subtle timestamp feature
                st.caption(f"{msg.get('time', '')}")

    # --- INPUT SECTION ---
    if prompt := st.chat_input("Input command..."):
        curr_time = datetime.now().strftime("%H:%M")
        
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt, 
            "time": curr_time
        })
        st.rerun()

    # --- ASSISTANT LOGIC ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with chat_col:
            with st.chat_message("assistant"):
                with st.spinner("Decoding Neural Pathways..."):
                    time.sleep(1.2) # Simulated thinking time
                    response = f"Neural analysis complete for: **{st.session_state.messages[-1]['content']}**."
                    st.markdown(response)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response, 
                        "time": datetime.now().strftime("%H:%M")
                    })
                    st.rerun()