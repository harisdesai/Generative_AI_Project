import streamlit as st

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
               
        .stChatInputContainer > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 209, 255, 0.3) !important;
            border-radius: 25px !important;
        }
               
        /* Fix Chat Input Width and Centering */
        .stChatInputContainer {
            padding-bottom: 20px !important;
            background: transparent !important;
        }

        /* Ensure the inner input box stays consistent */
        .stChatInputContainer > div {
            max-width: 800px !important; /* Forces a consistent max width */
            margin: 0 auto !important;   /* Centers it */
        }

        /* Spinner Styling */
        .stSpinner > div {
            border-top-color: #00f2ff !important;
        }
        </style>
    """, unsafe_allow_html=True)

def local_css():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp { 
            background-color: #0b0f19;
            color: #e2e8f0;
        }
        
        .main-header {
            color: #ffffff;
            font-weight: 700;
            font-family: 'Inter', -apple-system, sans-serif;
            letter-spacing: -0.5px;
        }
        
        /* Sidebar Styling */
        .stSidebar { 
            background-color: #050810; 
            border-right: 1px solid #1e293b;
        }
        
        /* Sidebar Chat History Buttons */
        .chat-history-btn {
            width: 100%;
            padding: 10px;
            margin-bottom: 5px;
            background-color: transparent;
            border: 1px solid #1e293b;
            color: #94a3b8;
            text-align: left;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .chat-history-btn:hover {
            background-color: #1e293b;
            color: #10b981;
            border-color: #10b981;
        }

        .chat-active {
            background-color: #064e3b !important;
            color: #ecfdf5 !important;
            border-color: #10b981 !important;
        }

        /* Message Layout */
        .message-row {
            display: flex;
            width: 100%;
            margin-bottom: 20px;
            animation: fadeIn 0.5s ease;
            align-items: flex-start;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message-row.user { justify-content: flex-end; }
        .message-row.user .message-bubble {
            background-color: #064e3b;
            color: #ecfdf5;
            border-bottom-right-radius: 4px;
            margin-left: 60px;
            border: 1px solid #065f46;
        }
        
        .message-row.assistant { justify-content: flex-start; }
        .message-row.assistant .message-bubble {
            background-color: #1e293b;
            color: #f1f5f9;
            border-bottom-left-radius: 4px;
            border: 1px solid #334155;
            margin-right: 60px;
        }
        
        .message-bubble {
            max-width: 75%;
            padding: 14px 20px;
            border-radius: 18px;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }
        
        .message-content { margin: 0; word-wrap: break-word; font-size: 0.98rem; }
        
        /* Formatting bold text specifically within bubbles */
        .message-content strong {
            color: #00f2ff;
            font-weight: bold;
        }

        .message-time { font-size: 0.72rem; opacity: 0.4; margin-top: 8px; display: block; }
        
        .message-avatar {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            flex-shrink: 0;
            background-color: #1e293b;
            border: 1px solid #334155;
        }
        
        .message-avatar img { width: 100%; height: 100%; object-fit: cover; }
        
        .message-row.user .message-avatar { order: 2; margin-left: 12px; border-color: #059669; }
        .message-row.assistant .message-avatar { order: 0; margin-right: 12px; border-color: #475569; }
        
        .stButton button {
            border-radius: 8px;
            border: 1px solid #334155;
            background-color: #0f172a;
            color: #94a3b8;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        
        .stButton button:hover {
            border-color: #10b981;
            color: #10b981;
        }

        .stChatInputContainer textarea {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)