import streamlit as st
import time
from user_ui import render_user_ui
from admin_ui import render_admin_ui
from Css import style_func, local_css

st.set_page_config(page_title="Sunbeam Elite Portal", page_icon="💠", layout="wide")

# --- AUTHENTICATION LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login():
    style_func()
    logo_left, logo_mid, logo_right = st.columns([1.43, 1, 1])
    
    with logo_mid:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image("https://sunbeaminfo.in/img/new/new_logo.png", width=200)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 1. Centered Header
    st.markdown("<h1 class='neon-glow' style='text-align: center;'>SYSTEM ACCESS</h1>", unsafe_allow_html=True)
    left_spacer, center_col, right_spacer = st.columns([1, 1.2, 1])
    
    with center_col:
        with st.container():
            with st.form("login_form"):
                user = st.text_input("Username")
                pw = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["User", "Admin"])
                
                submit = st.form_submit_button("UNLEASH AI", use_container_width=True)
                
                if submit:
                    if user == "admin" and pw == "admin123" and role == "Admin":
                        st.session_state.logged_in, st.session_state.role = True, "Admin"
                        st.rerun()
                    elif user == "user" and pw == "user123" and role == "User":
                        st.session_state.logged_in, st.session_state.role = True, "User"
                        st.rerun()
                    else:
                        st.error("Invalid Credentials")

if not st.session_state.logged_in:
    login() 
else:
    if st.session_state.role == "Admin":
        render_admin_ui(style_func) 
    else:
        render_user_ui(local_css)
