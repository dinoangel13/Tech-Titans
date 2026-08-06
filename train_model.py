import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
from preprocess import generate_all_datasets
from sklearn.metrics import f1_score
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "model")

def train_and_save_model():
    students_csv = os.path.join(DATASET_DIR, "students.csv")
    if not os.path.exists(students_csv):
        generate_all_datasets()

    df = pd.read_csv(students_csv)
    le_style = LabelEncoder()
    le_edu = LabelEncoder()
    le_diff = LabelEncoder()
    

    df['LearningStyle_Enc'] = le_style.fit_transform(df['LearningStyle'].astype(str))
    df['EducationLevel_Enc'] = le_edu.fit_transform(df['EducationLevel'].astype(str))
    df['ContextualDifficulty_Enc'] = le_diff.fit_transform(df['ContextualDifficulty'].astype(str))
   

    feature_cols = [
    'QuizScore',
    'Attempts',
    'TimeSpent',
    'Progress',
    'PreviousGPA',
    'EngagementScore',
    'LearningStyle_Enc',
    'EducationLevel_Enc',
    'ContextualDifficulty_Enc'
]
    
    X = df[feature_cols]
    y = df['NextTopic']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    rf_model = RandomForestClassifier(n_estimators=120, max_depth=12, min_samples_split=4, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)
    print(f"[*] Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    f1=f1_score(y_test,y_pred,average='weighted')
    print(f"[*]Model F1 Score: {f1:.4f}")
    os.makedirs(MODEL_DIR, exist_ok=True)
    artifacts = {
        'model': rf_model,
        'feature_cols': feature_cols,
        'le_style': le_style,
        'le_edu': le_edu,
        'le_diff': le_diff,
        'classes': rf_model.classes_
    }
    joblib.dump(artifacts, os.path.join(MODEL_DIR, "model.pkl"))
    print("[+] Model artifacts saved to model/model.pkl")

if __name__ == "__main__":
    train_and_save_model()
