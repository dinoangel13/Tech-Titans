import streamlit as st
import pandas as pd
from database import (
    get_all_students, add_or_update_student, delete_student,
    get_all_topics, add_topic, delete_topic,
    get_all_quizzes, add_quiz, get_all_resources, init_db
)

st.set_page_config(page_title="Admin Control Panel - PathAI", page_icon="⚙️", layout="wide")

if not st.session_state.get('authenticated'):
    st.warning("Please log in from the main app page.")
    st.stop()

if st.session_state.get('role', 'student') != 'admin':
    st.error("⛔ Access Denied: Administrator credentials required.")
    st.stop()

st.title("⚙️ Administrator Control Panel & System Management")

students_df = get_all_students()
topics_df = get_all_topics()
quizzes_df = get_all_quizzes()
resources_df = get_all_resources()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Students", len(students_df))
with col2: st.metric("Course Topics", len(topics_df))
with col3: st.metric("Quiz Questions", len(quizzes_df))
with col4: st.metric("Learning Resources", len(resources_df))

st.divider()

tab_students, tab_topics, tab_quizzes, tab_sys = st.tabs(["👥 Manage Students", "📚 Manage Topics", "❓ Quiz Question Uploader", "⚙️ Maintenance"])

with tab_students:
    st.dataframe(students_df[['student_id', 'name', 'email', 'quiz_score', 'progress', 'next_topic']], use_container_width=True, hide_index=True)

with tab_topics:
    st.dataframe(topics_df, use_container_width=True, hide_index=True)

with tab_quizzes:
    st.dataframe(quizzes_df, use_container_width=True, hide_index=True)

with tab_sys:
    if st.button("🔄 Re-seed SQLite Database from CSV Datasets"):
        init_db()
        st.success("Database re-seeded!")