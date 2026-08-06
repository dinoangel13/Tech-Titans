import streamlit as st
import pandas as pd
import plotly.express as px
import io
from database import get_student_by_id, get_student_quiz_history, get_all_students
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Student Dashboard - PathAI", page_icon="📈", layout="wide")

def generate_pdf_report(student, quiz_history_df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#6C5CE7'), spaceAfter=12)

    story.append(Paragraph("Personalized Learning Performance Report", title_style))
    story.append(Paragraph(f"Student Name: <b>{student['name']}</b> (ID: {student['student_id']})", styles['Normal']))
    story.append(Paragraph(f"Education Level: {student['education_level']} | Learning Style: {student['learning_style']}", styles['Normal']))
    story.append(Spacer(1, 12))

    metrics_data = [
        ["Metric", "Value"],
        ["Latest Quiz Accuracy", f"{student['quiz_score']}%"],
        ["Overall Progress", f"{student['progress']}%"],
        ["Total Time Spent", f"{student['time_spent']} mins"],
        ["Prerequisite Attempts", f"{student['attempts']}"],
        ["Current Focus Topic", f"{student['current_topic']}"],
        ["Next Recommended Topic", f"{student['next_topic']}"]
    ]
    t = Table(metrics_data, colWidths=[200, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6C5CE7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Topic Mastery Breakdown:</b>", styles['Heading2']))
    story.append(Paragraph(f"• <b>Strong Topics:</b> {student['strong_topics']}", styles['Normal']))
    story.append(Paragraph(f"• <b>Weak Topics Needing Focus:</b> {student['weak_topics']}", styles['Normal']))
    story.append(Spacer(1, 16))

    if not quiz_history_df.empty:
        story.append(Paragraph("<b>Recent Quiz History:</b>", styles['Heading2']))
        qh_data = [["Topic", "Score", "Attempts", "Time Spent (m)"]]
        for _, row in quiz_history_df.head(5).iterrows():
            qh_data.append([str(row.get('topic_title', 'Quiz Module')), f"{row.get('score', 0)}%", str(row.get('attempts', 1)), f"{row.get('time_spent', 0)} mins"])
        ht = Table(qh_data, colWidths=[180, 80, 80, 110])
        ht.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4A5568')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ]))
        story.append(ht)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

if not st.session_state.get('authenticated'):
    st.warning("Please log in from the main app page to view your Student Dashboard.")
    st.stop()

st.title("🎯 Student Learning Dashboard")

student_id = st.session_state.get('student_id', 'STU0001')
all_students_df = get_all_students()
student_ids = all_students_df['student_id'].tolist() if not all_students_df.empty else ['STU0001']

col_sel1, col_sel2 = st.columns([3, 1])
with col_sel1:
    selected_id = st.selectbox("Select Student Profile:", student_ids, index=student_ids.index(student_id) if student_id in student_ids else 0)

student = get_student_by_id(selected_id)

st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h2 style="margin:0; color:#6C5CE7;">👤 {student['name']}</h2>
                <p style="margin:0; color:#A0AEC0;">ID: {student['student_id']} | Email: {student['email']}</p>
            </div>
            <div>
                <span style="background:rgba(108,92,231,0.2); color:#6C5CE7; padding:6px 14px; border-radius:20px; font-weight:700;">
                    {student['learning_style']} Learner
                </span>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align:center;">
            <div><b>Age:</b> {student['age']}</div>
            <div><b>Education:</b> {student['education_level']}</div>
            <div><b>Previous GPA:</b> {student['previous_gpa']} / 4.0</div>
            <div><b>Current Topic:</b> {student['current_topic']}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Quiz Score Accuracy", f"{student['quiz_score']}%")
with m2: st.metric("Course Progress", f"{student['progress']}%")
with m3: st.metric("Time Spent per Module", f"{student['time_spent']} mins")
with m4: st.metric("Quiz Attempts", f"{student['attempts']}")

st.divider()

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📊 Quiz Score History & Trend")
    quiz_history_df = get_student_quiz_history(student['student_id'])
    
    if not quiz_history_df.empty:
        fig_trend = px.line(quiz_history_df, x="date_taken", y="score", markers=True, title="Quiz Score Trend Over Time", color_discrete_sequence=["#6C5CE7"])
        fig_trend.update_layout(template="plotly_dark", yaxis_range=[0, 100])
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        sim_data = pd.DataFrame({'Attempt': [f'Quiz {i}' for i in range(1, 6)], 'Score': [max(40, student['quiz_score'] - 20 + i*5) for i in range(5)]})
        fig_trend = px.bar(sim_data, x='Attempt', y='Score', color='Score', color_continuous_scale='Purples')
        fig_trend.update_layout(template="plotly_dark", yaxis_range=[0, 100])
        st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("⚡ Topic Mastery Matrix")
    st.markdown(f"""<div class="glass-card" style="border-left: 4px solid #10B981;"><h4 style="color:#10B981; margin:0 0 8px 0;">💪 Strong Topics</h4><p style="margin:0;">{student['strong_topics']}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glass-card" style="border-left: 4px solid #EF4444;"><h4 style="color:#EF4444; margin:0 0 8px 0;">⚠️ Weak Topics Needing Revision</h4><p style="margin:0;">{student['weak_topics']}</p></div>""", unsafe_allow_html=True)

    st.subheader("🗓️ Weekly AI Study Plan")
    st.info(f"Targeting: **{student['next_topic']}**")
    st.markdown(f"""
        - **Mon & Tue:** Review concept fundamentals of *{student['next_topic']}* (30 mins/day)
        - **Wed:** Complete interactive video resources tailored for **{student['learning_style']}** style.
        - **Thu & Fri:** Take diagnostic quiz; target >75% accuracy threshold.
        - **Weekend:** Hands-on practice problem set on weak areas (*{student['weak_topics']}*).
    """)

    st.divider()
    pdf_bytes = generate_pdf_report(student, quiz_history_df)
    st.download_button(
        label="📥 Download Student Performance Report (PDF)",
        data=pdf_bytes,
        file_name=f"Learning_Report_{student['student_id']}.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary"
    )