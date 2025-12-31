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