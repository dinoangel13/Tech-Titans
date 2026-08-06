import streamlit as st
import os
from database import init_db
from login import render_login_page

st.set_page_config(
    page_title="PathAI - Learning Recommendation System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

def inject_custom_css():
    theme = st.session_state['theme']
    bg_color = "#0F172A" if theme == 'dark' else "#F8FAFC"
    card_bg = "rgba(30, 41, 59, 0.7)" if theme == 'dark' else "#FFFFFF"
    text_color = "#F8FAFC" if theme == 'dark' else "#0F172A"
    border_color = "rgba(255, 255, 255, 0.1)" if theme == 'dark' else "#E2E8F0"
    subtext_color = "#94A3B8" if theme == 'dark' else "#64748B"

    css = f"""
    <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}
        .glass-card {{ background: {card_bg}; backdrop-filter: blur(12px); border: 1px solid {border_color}; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15); }}
        .stat-box {{ text-align: center; padding: 16px; border-radius: 10px; background: rgba(108, 92, 231, 0.12); border: 1px solid rgba(108, 92, 231, 0.25); }}
        .stat-value {{ font-size: 1.8rem; font-weight: 800; color: #6C5CE7; }}
        .stat-label {{ font-size: 0.85rem; color: {subtext_color}; text-transform: uppercase; letter-spacing: 0.05em; }}
        .stButton>button {{ border-radius: 8px; font-weight: 600; }}
        header[data-testid="stHeader"] {{ background: transparent; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

if not st.session_state['authenticated']:
    render_login_page()
else:
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 10px 0;">
                <h2 style="color: #6C5CE7; margin:0;">🧠 PathAI</h2>
                <p style="font-size:0.8rem; color:#A0AEC0;">Adaptive Learning System</p>
            </div>
        """, unsafe_allow_html=True)
        
        user = st.session_state['user']
        st.divider()
        
        st.markdown(f"""
            <div class="glass-card" style="padding: 12px; margin-bottom: 15px;">
                <p style="margin:0; font-weight:700;">👤 {user['name']}</p>
                <p style="margin:0; font-size:0.8rem; color:#6C5CE7; text-transform:uppercase;">Role: {user['role']}</p>
                <p style="margin:0; font-size:0.75rem; color:#A0AEC0;">{user['email']}</p>
            </div>
        """, unsafe_allow_html=True)

        theme_choice = st.radio(
            "🎨 UI Theme",
            ["Dark Mode 🌙", "Light Mode ☀️"],
            index=0 if st.session_state['theme'] == 'dark' else 1
        )
        new_theme = 'dark' if "Dark" in theme_choice else 'light'
        if new_theme != st.session_state['theme']:
            st.session_state['theme'] = new_theme
            st.rerun()

        st.divider()
        st.markdown("### 📌 Navigation")
        st.info("Use the sidebar menu above to switch between Dashboard, Recommendations, Analytics, Teacher, and Admin views.")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['authenticated'] = False
            st.session_state['user'] = None
            st.rerun()

    st.title(f"Welcome to PathAI, {st.session_state['user']['name']}! 👋")
    st.markdown("""
        ### AI-Powered Personalized Learning Path Recommendation System
        
        This platform uses **Random Forest Machine Learning** and **Explainable AI (XAI)** to dynamically analyze your 
        quiz performance, time spent per module, learning style, and topic attempts to construct a tailor-made 
        learning roadmap.
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-value">🎯 1_Dashboard</div>
                <div class="stat-label">Student Metrics & Plan</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-value">🤖 2_Recommendation</div>
                <div class="stat-label">AI Paths & XAI</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-value">📊 3_Analytics</div>
                <div class="stat-label">Plotly Insights</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-value">👨‍🏫 4_Teacher / Admin</div>
                <div class="stat-label">Class Management</div>
            </div>
        """, unsafe_allow_html=True)