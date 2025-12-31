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

        /* Chat Bubble Alignment */
        [data-testid="stChatMessage"] {
            border-radius: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(0, 242, 255, 0.2);
            width: fit-content;
            max-width: 80%;
        }

        /* THE FIX: Force Shrinked Input Box */
        
        /* 1. Target the bottom fixed container */
        [data-testid="stBottom"] > div {
            background: transparent !important;
            border: none !important;
        }

        /* 2. Constrain the width of the actual input area */
        [data-testid="stChatInput"] {
            max-width: 700px !important;
            margin: 0 auto !important;
            left: 0 !important;
            right: 0 !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 209, 255, 0.3) !important;
            border-radius: 25px !important;
        }

        /* 3. Hide the default horizontal line above input */
        [data-testid="stBottomBlockContainer"] {
            border-top: none !important;
        }

        /* Spinner Styling */
        .stSpinner > div {
            border-top-color: #00f2ff !important;
        }
        </style>
    """, unsafe_allow_html=True)