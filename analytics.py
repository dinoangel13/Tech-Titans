import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_students

st.set_page_config(page_title="Visual Analytics - PathAI", page_icon="📊", layout="wide")

if not st.session_state.get('authenticated'):
    st.warning("Please log in from the main app page to view Visual Analytics.")
    st.stop()

st.title("📊 Interactive Learning Analytics & Visual Insights")

students_df = get_all_students()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Active Students", len(students_df))
with col2: st.metric("Average Quiz Score", f"{students_df['quiz_score'].mean():.1f}%")
with col3: st.metric("Average Progress", f"{students_df['progress'].mean():.1f}%")
with col4: st.metric("Avg Module Time", f"{students_df['time_spent'].mean():.1f} mins")

st.divider()

c1, c2 = st.columns(2)
with c1:
    fig_hist = px.histogram(students_df, x="quiz_score", nbins=20, title="Quiz Accuracy Score Distribution", color_discrete_sequence=["#6C5CE7"], marginal="box")
    fig_hist.update_layout(template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    rec_counts = students_df['next_topic'].value_counts().reset_index()
    rec_counts.columns = ['Topic', 'Count']
    fig_pie = px.pie(rec_counts, names='Topic', values='Count', title='AI Recommended Next Topics Distribution', color_discrete_sequence=px.colors.sequential.Purples_r)
    fig_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

c3, c4 = st.columns(2)
with c3:
    fig_scatter = px.scatter(students_df, x="time_spent", y="quiz_score", color="learning_style", size="attempts", hover_data=["student_id", "name"], title="Time Spent (mins) vs Quiz Score Accuracy")
    fig_scatter.update_layout(template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

with c4:
    fig_box = px.box(students_df, x="education_level", y="progress", color="education_level", title="Learning Progress (%) by Education Level")
    fig_box.update_layout(template="plotly_dark")
    st.plotly_chart(fig_box, use_container_width=True)