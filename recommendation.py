import streamlit as st
import pandas as pd
import plotly.express as px
from predict import predict_recommendations
from database import get_student_by_id, save_recommendation, get_all_resources

students_df = get_all_students()

if st.session_state["role"] == "student":

    active_student = students_df[
        students_df["student_id"] ==
        st.session_state["student_id"]
    ].iloc[0].to_dict()

else:

    selected_name = st.selectbox(
        "Select Student",
        students_df["name"]
    )

    active_student = students_df[
        students_df["name"] == selected_name
    ].iloc[0].to_dict()

st.set_page_config(page_title="AI Recommendations & XAI - PathAI", page_icon="🤖", layout="wide")

if not st.session_state.get('authenticated'):
    st.warning("Please log in from the main app page to view Recommendations.")
    st.stop()

st.title("🤖 AI-Powered Recommendation Engine & Explainable AI (XAI)")
st.markdown("Dynamic Random Forest inference engine that computes optimal learning paths based on performance telemetry.")

student_id = st.session_state.get('student_id', 'STU0001')
active_student = get_student_by_id(student_id) or {}

with st.sidebar:
    st.header("🎛️ Simulation Parameters")
    quiz_score_input = st.slider("Quiz Score Accuracy (%)", 0, 100, int(active_student.get('quiz_score', 65)))
    attempts_input = st.slider("Quiz Attempts Count", 1, 10, int(active_student.get('attempts', 2)))
    time_spent_input = st.slider("Time Spent per Module (Mins)", 5.0, 120.0, float(active_student.get('time_spent', 40.0)))
    progress_input = st.slider("Course Progress (%)", 0, 100, int(active_student.get('progress', 45)))
    gpa_input = st.slider("Previous GPA", 1.0, 4.0, float(active_student.get('previous_gpa', 3.2)))
    engagement_input = st.slider("Engagement Score", 30, 100, int(active_student.get('engagement_score', 80)))
    learning_style_input = st.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic"], index=["Visual", "Auditory", "Kinesthetic"].index(active_student.get('learning_style', 'Visual')))
    edu_level_input = st.selectbox("Education Level", ["High School", "UG", "PG"], index=["High School", "UG", "PG"].index(active_student.get('education_level', 'UG')))
    diff_input = st.selectbox("Contextual Difficulty Level", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(active_student.get('contextual_difficulty', 'Medium')))

student_feature_dict = {
    'QuizScore': quiz_score_input, 'Attempts': attempts_input, 'TimeSpent': time_spent_input,
    'Progress': progress_input, 'PreviousGPA': gpa_input, 'EngagementScore': engagement_input,
    'LearningStyle': learning_style_input, 'EducationLevel': edu_level_input, 'ContextualDifficulty': diff_input
}

recs, explanations, feature_importances = predict_recommendations(student_feature_dict)

if st.button("🔄 Generate & Persist Recommendation", type="primary"):
    save_recommendation(student_id, recs, explanations[0])
    st.success("New recommendation persisted to student history log!")

st.subheader("🏆 Top 3 Recommended Learning Topics")

col_r1, col_r2, col_r3 = st.columns(3)
cols = [col_r1, col_r2, col_r3]

for idx, item in enumerate(recs):
    with cols[idx]:
        conf = item['confidence_score']
        topic_name = item['topic']
        rank_badge = ["🥇 Rank #1 Primary", "🥈 Rank #2 Follow-Up", "🥉 Rank #3 Elective"][idx]
        
        st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid #6C5CE7; height: 260px;">
                <span style="font-size:0.8rem; color:#6C5CE7; font-weight:800;">{rank_badge}</span>
                <h3 style="margin:10px 0; color:#F8FAFC;">{topic_name}</h3>
                <p style="font-size:1.8rem; font-weight:800; color:#10B981; margin: 5px 0;">{conf}% <span style="font-size:0.9rem; color:#A0AEC0;">Confidence</span></p>
                <hr style="border-color:rgba(255,255,255,0.1); margin:10px 0;">
                <p style="font-size:0.85rem; color:#CBD5E0; line-height:1.4;">{explanations[idx]}</p>
            </div>
        """, unsafe_allow_html=True)

st.divider()

col_xai_left, col_xai_right = st.columns([1, 1])

with col_xai_left:
    st.subheader("💡 Explainable AI (XAI) Decision Rationale")
    st.markdown(f"""
        > **Primary Recommendation:** `{recs[0]['topic']}`
        
        ### 🔍 Why was this recommended?
        1. **Quiz Accuracy Impact:** Your Quiz Score of **{quiz_score_input}%** triggered the decision branch for targeted topic reinforcement.
        2. **Time Spent Anomaly:** You spent **{time_spent_input} minutes** per module, indicating high effort requiring curated learning resources.
        3. **Style Alignment:** Recommendations prioritize **{learning_style_input}** media types to maximize retention.
    """)
    st.info(f"💡 **XAI Summary Statement:** '{recs[0]['topic']} is recommended because your quiz score ({quiz_score_input}%) indicated topic gaps and your average time spent ({time_spent_input} mins) required an optimized learning path.'")

with col_xai_right:
    st.subheader("⚖️ Random Forest Feature Importance Breakdown")
    imp_df = pd.DataFrame({'Feature': list(feature_importances.keys()), 'Importance': list(feature_importances.values())}).sort_values(by='Importance', ascending=True)
    fig_imp = px.bar(imp_df, x='Importance', y='Feature', orientation='h', title='Global Feature Importance (%)', color='Importance', color_continuous_scale='Purples')
    fig_imp.update_layout(template="plotly_dark", height=320)
    st.plotly_chart(fig_imp, use_container_width=True)

st.divider()

st.subheader("📖 Curated Resources for Primary Recommendation")
resources_df = get_all_resources()

resources_df = resources_df.rename(columns={
    "title": "Title",
    "type": "Type",
    "difficulty": "Difficulty",
    "duration_minutes": "Duration (min)",
    "url": "URL"
})
st.dataframe(
    resources_df[['Title', 'Type', 'Difficulty', 'Duration (min)', 'URL']],
    use_container_width=True,
    hide_index=True
)
if resources_df is not None:
    st.write(resources_df.columns.tolist())
    st.dataframe(resources_df.head())
if not resources_df.empty:
    st.dataframe(
        resources_df,
        use_container_width=True,
        hide_index=True
    )
