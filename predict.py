import os
import pandas as pd
import numpy as np
import joblib
from train_model import train_and_save_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

def get_model_bundle():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)

def predict_recommendations(student_features):
    bundle = get_model_bundle()
    rf_model = bundle['model']
    feature_cols = bundle['feature_cols']
    le_style = bundle['le_style']
    le_edu = bundle['le_edu']
    le_diff = bundle['le_diff']
    classes = bundle['classes']

    def safe_transform(le, val, default="Visual"):
        val_str = str(val)
        return le.transform([val_str])[0] if val_str in le.classes_ else le.transform([default])[0]

    style_enc = safe_transform(le_style, student_features.get('LearningStyle', 'Visual'))
    edu_enc = safe_transform(le_edu, student_features.get('EducationLevel', 'UG'), default="UG")
    diff_enc = safe_transform(le_diff, student_features.get('ContextualDifficulty', 'Medium'), default="Medium")

    input_row = pd.DataFrame(...)[feature_cols]
    input_row = pd.DataFrame([{
        'QuizScore': float(student_features.get('QuizScore', 70)),
        'Attempts': int(student_features.get('Attempts', 2)),
        'TimeSpent': float(student_features.get('TimeSpent', 35)),
        'Progress': float(student_features.get('Progress', 50)),
        'PreviousGPA': float(student_features.get('PreviousGPA', 3.2)),
        'EngagementScore': int(student_features.get('EngagementScore', 80)),
        'LearningStyle_Enc': style_enc,
        'EducationLevel_Enc': edu_enc,
        'ContextualDifficulty_Enc': diff_enc
    }])[feature_cols]

    probs = rf_model.predict_proba(input_row)[0]
    top_indices = np.argsort(probs)[::-1][:3]

    top_3 = []
    explanations = []

    quiz_score = student_features.get('QuizScore', 70)
    time_spent = student_features.get('TimeSpent', 35)
    attempts = student_features.get('Attempts', 2)
    learning_style = student_features.get('LearningStyle', 'Visual')

    for rank, idx in enumerate(top_indices):
        topic_name = classes[idx]
        confidence = max(float(probs[idx] * 100), 15.5)

        if rank == 0:
            if quiz_score < 60:
                explanation = f"**{topic_name}** is highly recommended as primary focus because your recent quiz score ({quiz_score}%) indicates foundational gaps. Re-attempting core concepts will boost your retention."
            elif quiz_score > 85:
                explanation = f"**{topic_name}** is recommended for advanced progression because you mastered prerequisite topics with high quiz accuracy ({quiz_score}%)."
            else:
                explanation = f"**{topic_name}** aligns best with your learning speed ({time_spent} mins/module) and steady progress profile."
        elif rank == 1:
            explanation = f"**{topic_name}** is selected because you took {attempts} attempts on previous modules; this module provides interactive practice tuned for {learning_style} learners." if attempts > 3 else f"**{topic_name}** provides a balanced follow-up module to broaden your problem-solving toolkit."
        else:
            explanation = f"**{topic_name}** is suggested as an elective module to complement your learning path with a {confidence:.1f}% AI suitability score."

        top_3.append({"topic": topic_name, "confidence_score": round(confidence, 1)})
        explanations.append(explanation)

    importances = dict(zip(feature_cols, rf_model.feature_importances_ * 100))
    importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

    return top_3, explanations, importances
