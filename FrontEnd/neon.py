import streamlit as st

def apply_neon_style():
    st.markdown("""
        <style>
        /* --- GLOBAL LAYOUT --- */
        .stApp { background: radial-gradient(circle at 50% -20%, #1c2533 0%, #080a0f 80%); }

        /* --- DYNAMIC CHAT BUBBLES --- */
        [data-testid="stChatMessage"] {
            display: flex;
            width: 100%;
            margin-bottom: 1.2rem;
            background: transparent !important;
        }

        /* Right-align User Messages */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
        [data-testid="stChatMessage"]:has(img[alt="user"]) {
            flex-direction: row-reverse;
            text-align: right;
        }

        /* Message Bubble Styling (The "Dynamic Size" Magic) */
        [data-testid="stChatMessageContent"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 209, 255, 0.2) !important;
            border-radius: 20px !important;
            padding: 12px 20px !important;
            transition: all 0.3s ease;
            
            /* DYNAMIC WIDTH SETTINGS */
            width: fit-content !important; 
            max-width: 85% !important;     /* Prevents stretching too far on long text */
            display: inline-block !important;
        }

        /* Align User bubble itself to the right within the flex container */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
            margin-left: auto;
            text-align: left; /* Keep text inside bubble readable */
        }

        /* --- NEON ANIMATIONS & HOVERS --- */
        @keyframes pulsate {
            100% { text-shadow: 0 0 15px #00d1ff, 0 0 30px #00d1ff; }
            0% { text-shadow: 0 0 5px #00d1ff; }
        }

        @keyframes status-flicker {
            0%, 18%, 22%, 25%, 53%, 57%, 100% {
                box-shadow: 0 0 15px rgba(0, 209, 255, 0.4), 0 0 5px rgba(0, 209, 255, 0.2);
            }
            20%, 24%, 55% { box-shadow: none; }
        }

        .neon-glow {
            background: linear-gradient(to right, #ffffff, #00d1ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            animation: pulsate 2.5s infinite alternate;
        }

        [data-testid="stChatMessageContent"]:hover {
            transform: translateY(-3px);
            border-color: #00d1ff !important;
            animation: status-flicker 2s infinite;
        }

        /* STICKY BOTTOM INPUT */
        .stChatInputContainer {
            padding-bottom: 20px !important;
            background-color: transparent !important;
        }

        .stChatInputContainer > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 209, 255, 0.3) !important;
            border-radius: 25px !important;
        }
            /* Add these to your existing style block in neon.py */

        /* Styling for the timestamps */
        .stCaption {
            font-size: 0.7rem !important;
            opacity: 0.5;
            margin-top: -10px;
            color: #00d1ff !important;
        }

        /* Scrollbar styling to match the neon theme */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-thumb {
            background: #00d1ff;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }

        /* Tooltip/Info box styling */
        .stInfo {
            background-color: rgba(0, 209, 255, 0.1) !important;
            border: 1px solid #00d1ff !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)