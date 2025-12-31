import streamlit as st

def render_admin_ui(style_func):
    style_func()
    
    # Header centering using HTML
    st.markdown("<h1 class='neon-glow' style='text-align: center;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Creating spacers: The 1s on the ends are the "margins"
    # The 2s in the middle are your actual content areas
    _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
    
    with c1:
        st.metric("Ingested Assets", "3 Files", "Verified")
    with c2:
        st.metric("Neural Tokens", "1,420", "Optimized")
    with c3:
        st.metric("Latency", "12ms", "Elite Tier")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Centering the JSON/Repository section
    col_left, col_mid, col_right = st.columns([1, 3, 1])
    with col_mid:
        st.subheader("Knowledge Repository")
        st.json({"Pre-CAT": "Sync Active", "Contacts": "Linked", "About-Us": "Live"})