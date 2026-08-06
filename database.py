import os
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime
from preprocess import generate_all_datasets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "personalized_learning.db")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(os.path.join(DATASET_DIR, "students.csv")):
        generate_all_datasets()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        student_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        age INTEGER,
        gender TEXT,
        education_level TEXT,
        learning_style TEXT,
        previous_gpa REAL,
        quiz_score INTEGER,
        attempts INTEGER,
        time_spent REAL,
        progress INTEGER,
        current_topic TEXT,
        completed_topics TEXT,
        weak_topics TEXT,
        strong_topics TEXT,
        previous_recommendation TEXT,
        next_topic TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        topic_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT,
        difficulty TEXT,
        prerequisites TEXT,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quizzes (
        quiz_id TEXT PRIMARY KEY,
        topic_id TEXT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        explanation TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        resource_id TEXT PRIMARY KEY,
        topic_id TEXT,
        title TEXT NOT NULL,
        type TEXT,
        url TEXT,
        difficulty TEXT,
        duration_minutes INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        quiz_id TEXT,
        topic_id TEXT,
        score INTEGER,
        attempts INTEGER,
        time_spent REAL,
        date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        rec_1 TEXT,
        score_1 REAL,
        rec_2 TEXT,
        score_2 REAL,
        rec_3 TEXT,
        score_3 REAL,
        explanation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    cursor.execute('SELECT COUNT(*) FROM students')
    if cursor.fetchone()[0] == 0:
        print("[+] Seeding SQLite database from CSV datasets...")
        
        topics_df = pd.read_csv(os.path.join(DATASET_DIR, "topics.csv"))
        topics_df.columns = [c.lower() for c in topics_df.columns]
        topics_df = topics_df.rename(columns={'topicid': 'topic_id'})
        topics_df.to_sql('topics', conn, if_exists='append', index=False)

        quizzes_df = pd.read_csv(os.path.join(DATASET_DIR, "quizzes.csv"))
        quizzes_df = quizzes_df.rename(columns={
            'QuizID': 'quiz_id', 'TopicID': 'topic_id', 'Question': 'question',
            'OptionA': 'option_a', 'OptionB': 'option_b', 'OptionC': 'option_c',
            'OptionD': 'option_d', 'CorrectOption': 'correct_option', 'Explanation': 'explanation'
        })
        quizzes_df.to_sql('quizzes', conn, if_exists='append', index=False)

        resources_df = pd.read_csv(os.path.join(DATASET_DIR, "resources.csv"))
        resources_df = resources_df.rename(columns={
            'ResourceID': 'resource_id', 'TopicID': 'topic_id', 'Title': 'title',
            'Type': 'type', 'URL': 'url', 'Difficulty': 'difficulty', 'DurationMinutes': 'duration_minutes'
        })
        resources_df.to_sql('resources', conn, if_exists='append', index=False)

        students_df = pd.read_csv(os.path.join(DATASET_DIR, "students.csv"))
        
        def get_weak_topics(row):
            if row['QuizScore'] < 65:
                return "Trees & Binary Search Trees, Dynamic Programming"
            elif row['QuizScore'] < 80:
                return "Graph Algorithms"
            return "None"

        def get_strong_topics(row):
            if row['QuizScore'] >= 80:
                return "Arrays & Hash Maps, Stacks & Queues, Sorting & Searching"
            elif row['QuizScore'] >= 65:
                return "Arrays & Hash Maps, Linked Lists"
            return "Arrays & Hash Maps"

        students_df['email'] = students_df['StudentID'].apply(lambda x: f"{x.lower()}@student.edu")
        students_df['weak_topics'] = students_df.apply(get_weak_topics, axis=1)
        students_df['strong_topics'] = students_df.apply(get_strong_topics, axis=1)

        db_students_df = students_df[[
            'StudentID', 'Name', 'email', 'Age', 'Gender', 'EducationLevel',
            'LearningStyle', 'PreviousGPA', 'QuizScore', 'Attempts', 'TimeSpent',
            'Progress', 'CurrentTopic', 'CompletedTopics', 'weak_topics', 'strong_topics',
            'PreviousRecommendation', 'NextTopic'
        ]].rename(columns={
            'StudentID': 'student_id', 'Name': 'name', 'Age': 'age', 'Gender': 'gender',
            'EducationLevel': 'education_level', 'LearningStyle': 'learning_style',
            'PreviousGPA': 'previous_gpa', 'QuizScore': 'quiz_score', 'Attempts': 'attempts',
            'TimeSpent': 'time_spent', 'Progress': 'progress', 'CurrentTopic': 'current_topic',
            'CompletedTopics': 'completed_topics', 'PreviousRecommendation': 'previous_recommendation',
            'NextTopic': 'next_topic'
        })
        
        db_students_df.to_sql('students', conn, if_exists='append', index=False)

        default_users = [
            ('Admin User', 'admin@edu.com', hash_password('admin123'), 'admin', 'ADM001'),
            ('Teacher Alex', 'teacher@edu.com', hash_password('teacher123'), 'teacher', 'TCH001'),
            ('Student User', 'stu0001@student.edu', hash_password('student123'), 'student', 'STU0001')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO users (name, email, password_hash, role, student_id)
            VALUES (?, ?, ?, ?, ?)
        ''', default_users)

        sample_history = []
        for s in students_df.head(200).itertuples():
            sample_history.append((s.StudentID, "Q101", "T101", s.QuizScore, s.Attempts, s.TimeSpent))
            sample_history.append((s.StudentID, "Q102", "T101", min(100, s.QuizScore + 10), 1, s.TimeSpent * 0.8))

        cursor.executemany('''
            INSERT INTO quiz_history (student_id, quiz_id, topic_id, score, attempts, time_spent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_history)

        conn.commit()

    conn.close()

def register_user(name, email, password, role='student', student_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role, student_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, pwd_hash, role, student_id))
        
        if role == 'student' and student_id:
            cursor.execute('''
                INSERT OR IGNORE INTO students (student_id, name, email, quiz_score, attempts, time_spent, progress, current_topic)
                VALUES (?, ?, ?, 70, 1, 30.0, 10, 'Arrays & Hash Maps')
            ''', (student_id, name, email))
            
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "User with this email already exists."
    finally:
        conn.close()

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password_hash = ?
    ''', (email, pwd_hash))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_students(search_query=None):
    conn = get_db_connection()
    if search_query:
        query = "SELECT * FROM students WHERE name LIKE ? OR student_id LIKE ? ORDER BY student_id ASC"
        df = pd.read_sql_query(query, conn, params=(f"%{search_query}%", f"%{search_query}%"))
    else:
        df = pd.read_sql_query("SELECT * FROM students ORDER BY student_id ASC", conn)
    conn.close()
    return df

def get_student_by_id(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_or_update_student(student_dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (
            student_id, name, email, age, gender, education_level, learning_style,
            previous_gpa, quiz_score, attempts, time_spent, progress, current_topic,
            completed_topics, weak_topics, strong_topics, previous_recommendation, next_topic
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            name=excluded.name, email=excluded.email, quiz_score=excluded.quiz_score,
            attempts=excluded.attempts, time_spent=excluded.time_spent, progress=excluded.progress,
            current_topic=excluded.current_topic, completed_topics=excluded.completed_topics,
            weak_topics=excluded.weak_topics, strong_topics=excluded.strong_topics, next_topic=excluded.next_topic
    ''', (
        student_dict.get('student_id'), student_dict.get('name'), student_dict.get('email'),
        student_dict.get('age', 20), student_dict.get('gender', 'Male'), student_dict.get('education_level', 'UG'),
        student_dict.get('learning_style', 'Visual'), student_dict.get('previous_gpa', 3.0),
        student_dict.get('quiz_score', 70), student_dict.get('attempts', 1), student_dict.get('time_spent', 30.0),
        student_dict.get('progress', 20), student_dict.get('current_topic', 'Arrays & Hash Maps'),
        student_dict.get('completed_topics', 'Arrays & Hash Maps'), student_dict.get('weak_topics', 'Graph Algorithms'),
        student_dict.get('strong_topics', 'Arrays & Hash Maps'), student_dict.get('previous_recommendation', 'M1 -> M2'),
        student_dict.get('next_topic', 'Linked Lists')
    ))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

def get_all_topics():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM topics", conn)
    conn.close()
    return df

def add_topic(topic_id, title, category, difficulty, prerequisites, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO topics (topic_id, title, category, difficulty, prerequisites, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (topic_id, title, category, difficulty, prerequisites, description))
    conn.commit()
    conn.close()

def delete_topic(topic_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE topic_id = ?", (topic_id,))
    conn.commit()
    conn.close()

def get_all_quizzes():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM quizzes", conn)
    conn.close()
    return df

def add_quiz(quiz_id, topic_id, question, opt_a, opt_b, opt_c, opt_d, correct_opt, explanation):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO quizzes (quiz_id, topic_id, question, option_a, option_b, option_c, option_d, correct_option, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (quiz_id, topic_id, question, opt_a, opt_b, opt_c, opt_d, correct_opt, explanation))
    conn.commit()
    conn.close()

def get_all_resources():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM resources", conn)
    conn.close()
    return df

def save_recommendation(student_id, recs, explanation):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recommendations (student_id, rec_1, score_1, rec_2, score_2, rec_3, score_3, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id,
        recs[0]['topic'], recs[0]['confidence_score'],
        recs[1]['topic'], recs[1]['confidence_score'],
        recs[2]['topic'], recs[2]['confidence_score'],
        explanation
    ))
    conn.commit()
    conn.close()

def get_student_quiz_history(student_id):
    conn = get_db_connection()
    df = pd.read_sql_query('''
        SELECT qh.*, t.title as topic_title 
        FROM quiz_history qh
        LEFT JOIN topics t ON qh.topic_id = t.topic_id
        WHERE qh.student_id = ?
        ORDER BY qh.date_taken ASC
    ''', conn, params=(student_id,))
    conn.close()
    return df

if __name__ == "__main__":
    init_db()