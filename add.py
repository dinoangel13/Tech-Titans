import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("AI_Personalized_Learning.csv")

# -----------------------------
# Encode categorical columns
# -----------------------------
encoders = {}

categorical_columns = [
    "gender",
    "education_level",
    "learning_style",
    "contextual_difficulty_level",
    "recommended_path"
]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# -----------------------------
# Features and Target
# -----------------------------
X = df[
    [
        "age",
        "gender",
        "education_level",
        "learning_style",
        "previous_gpa",
        "completed_modules",
        "avg_time_per_module",
        "engagement_score",
        "distraction_events",
        "quiz_accuracy",
        "feedback_score",
        "contextual_difficulty_level"
    ]
]

y = df["recommended_path"]

# -----------------------------
# Train Model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = accuracy_score(
    y_test,
    model.predict(X_test)
)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Personalized Learning",
    page_icon="🎓"
)

st.title("🎓 AI Personalized Learning Recommendation")

st.success(f"Model Accuracy : {accuracy*100:.2f}%")

age = st.slider("Age",16,35,20)

gender = st.selectbox(
    "Gender",
    encoders["gender"].classes_
)

education = st.selectbox(
    "Education Level",
    encoders["education_level"].classes_
)

learning = st.selectbox(
    "Learning Style",
    encoders["learning_style"].classes_
)

gpa = st.slider(
    "Previous GPA",
    0.0,
    10.0,
    7.0
)

completed = st.slider(
    "Completed Modules",
    0,
    50,
    10
)

time = st.slider(
    "Average Time Per Module",
    5,
    200,
    60
)

engagement = st.slider(
    "Engagement Score",
    0,
    100,
    70
)

distraction = st.slider(
    "Distraction Events",
    0,
    20,
    2
)

quiz = st.slider(
    "Quiz Accuracy",
    0,
    100,
    75
)

feedback = st.slider(
    "Feedback Score",
    1,
    5,
    4
)

difficulty = st.selectbox(
    "Difficulty Level",
    encoders["contextual_difficulty_level"].classes_
)

if st.button("Recommend Learning Path"):

    input_data = [[
        age,
        encoders["gender"].transform([gender])[0],
        encoders["education_level"].transform([education])[0],
        encoders["learning_style"].transform([learning])[0],
        gpa,
        completed,
        time,
        engagement,
        distraction,
        quiz,
        feedback,
        encoders["contextual_difficulty_level"].transform([difficulty])[0]
    ]]

    prediction = model.predict(input_data)[0]

    recommendation = encoders["recommended_path"].inverse_transform([prediction])[0]

    st.success(f"🎯 Recommended Learning Path : {recommendation}")

    probabilities = model.predict_proba(input_data)[0]

    top3 = probabilities.argsort()[-3:][::-1]

    st.subheader("Top 3 Recommendations")

    for i, idx in enumerate(top3, start=1):
        name = encoders["recommended_path"].inverse_transform([idx])[0]
        st.write(f"{i}. {name} — {probabilities[idx]*100:.2f}%")
