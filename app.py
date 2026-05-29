import streamlit as st
import streamlit.components.v1 as components

from config import SKILL_KEYWORD_MAP, SKILL_OPTIONS, THEME
from services.session_state import init_session_state
from ui.admin_view import render_admin_view
from ui.styles import apply_global_style
from ui.user_view import render_ai_assistant_view, render_jobs_view, render_user_view

st.set_page_config(
    page_title="SkillMap AI",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
apply_global_style(THEME)

components.html(
    """
    <script>
        if (window.location.hash) {
            const cleanUrl = window.location.pathname + window.location.search;
            window.history.replaceState(null, "", cleanUrl);
        }
    </script>
    """,
    height=0,
)

if "active_view" not in st.session_state:
    st.session_state.active_view = "Search"

st.sidebar.markdown("### Navigation")
if st.sidebar.button("Search", use_container_width=True):
    st.session_state.active_view = "Search"
if st.sidebar.button("View Jobs", use_container_width=True):
    st.session_state.active_view = "View Jobs"
if st.sidebar.button("AI Assistant", use_container_width=True):
    st.session_state.active_view = "AI Assistant"

st.sidebar.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-footer'>", unsafe_allow_html=True)
if st.sidebar.button("Admin", use_container_width=True):
    st.session_state.active_view = "Admin"
st.sidebar.markdown("</div>", unsafe_allow_html=True)

if st.session_state.active_view == "Admin":
    render_admin_view(THEME)
elif st.session_state.active_view == "View Jobs":
    render_jobs_view(THEME, SKILL_OPTIONS)
elif st.session_state.active_view == "AI Assistant":
    render_ai_assistant_view(THEME, SKILL_KEYWORD_MAP)
else:
    render_user_view(THEME, SKILL_KEYWORD_MAP, SKILL_OPTIONS)
