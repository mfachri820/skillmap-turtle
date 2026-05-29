import streamlit as st


def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "admin_user" not in st.session_state:
        st.session_state.admin_user = ""
