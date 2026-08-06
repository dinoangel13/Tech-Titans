import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_students, get_student_by_id

st.set_page_config(page_title="Teacher Dashboard - PathAI", page_icon="👨‍🏫", layout="wide")

if not st.session_state.get('authenticated'):
    st.warning("Please log in from the main app page to view Teacher Dashboard.")
    st.stop()

if st.session_state.get('role', 'student') not in ['teacher', 'admin']:
    st.error("⛔ Access Denied: Teacher or Admin credentials required.")
    st.stop()

st.title("👨‍🏫 Teacher Overview & Class Management")

students_df = get_all_students()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Enrolled Students", len(students_df))
with col2:
    at_risk_count = len(students_df[students_df['quiz_score'] < 65])
    st.metric("⚠️ At-Risk Students (<65%)", at_risk_count, delta=f"{(at_risk_count/len(students_df))*100:.1f}%", delta_color="inverse")
with col3: st.metric("Class Avg Quiz Score", f"{students_df['quiz_score'].mean():.1f}%")
with col4: st.metric("Class Avg Progress", f"{students_df['progress'].mean():.1f}%")

st.divider()

col_search, col_filter = st.columns([3, 1])
with col_search: search_q = st.text_input("🔍 Search Student by Name or ID:")
with col_filter: filter_at_risk = st.checkbox("🚨 Show Only At-Risk (<65%)")

filtered_df = get_all_students(search_q)
if filter_at_risk:
    filtered_df = filtered_df[filtered_df['quiz_score'] < 65]

st.dataframe(filtered_df[['student_id', 'name', 'email', 'quiz_score', 'progress', 'attempts', 'current_topic', 'next_topic', 'weak_topics']], use_container_width=True, hide_index=True)