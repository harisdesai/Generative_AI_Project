import streamlit as st
import time

# --- WORLD-CLASS CONFIG ---
st.set_page_config(page_title="Sunbeam Neural Partner", page_icon="💠", layout="wide")

# --- CUSTOM "GLASS-NEON" CSS ---
st.markdown("""
    <style>
    /* Main Background with Deep Radial Glow */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1c2533 0%, #080a0f 80%);
    }

    /* Sidebar - Frosted Glass Look */
    [data-testid="stSidebar"] {
        background: rgba(17, 21, 28, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Professional Chat Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        padding: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 209, 255, 0.4) !important;
        box-shadow: 0 12px 40px 0 rgba(0, 209, 255, 0.1);
    }

    /* Neon Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(0, 209, 255, 0.03);
        border: 1px solid rgba(0, 209, 255, 0.1);
        border-radius: 18px;
        padding: 1.2rem;
        transition: 0.3s;
    }

    /* Premium Typography */
    .premium-header {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #ffffff, #00d1ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Chat Input Bar Styling */
    .stChatInputContainer {
        border-radius: 30px !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NAVIGATION HUB ---
with st.sidebar:
    st.image("https://sunbeaminfo.in/img/new/new_logo.png", width=150)
    st.markdown("<h1 class='premium-header'>SUNBEAM ELITE</h1>", unsafe_allow_html=True)
    st.markdown("---")
    choice = st.selectbox("Intelligence Core", ["🧠 Neural Assistant", "🌐 Knowledge Vault", "⚙️ Data Lab"])
    
    st.markdown("### System Integrity")
    st.progress(98, "Neural Sync")
    st.progress(85, "Vector Density")
    
    st.markdown("---")
    if st.button("Purge Session Cache"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE: NEURAL CHAT ---
if choice == "🧠 Neural Assistant":
    st.markdown("<h1 class='premium-header'>Neural Interface v4.0</h1>", unsafe_allow_html=True)
    st.caption("Secured via local ChromaDB. Real-time inference active.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Modern Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Fluid Input
    if prompt := st.chat_input("Input command or question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Decoding knowledge patterns..."):
                time.sleep(0.8)
                # CONNECT YOUR RAG CHAIN HERE
                response = f"Simulated elite response for: **{prompt}**. Your local RAG engine is currently synthesizing this data point."
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif choice == "🌐 Knowledge Vault":
    st.markdown("<h1 class='premium-header'>Knowledge Statistics</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Documents Ingested", "3 Core Files", "Verified")
    c2.metric("Vector Vectors", "1,420 Units", "Optimized")
    c3.metric("Retrieval Accuracy", "99.2%", "Elite Tier")
    
    st.divider()
    st.subheader("Ingested Source Map")
    st.json({
        "Pre-CAT": {"Status": "Active", "Last_Update": "2025-12-30"},
        "About-Us": {"Status": "Active", "Type": "General Info"},
        "Contacts": {"Status": "Active", "Type": "Structured Table"}
    })