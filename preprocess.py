import os
import pandas as pd
import numpy as np
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Rahul", "Neha", "Vikram", "Sneha", "Aditya", "Ishita",
               "Karan", "Kavya", "Arjun", "Riya", "Dev", "Meera", "Siddharth", "Tanvi", "Yash", "Pooja",
               "Alex", "Emma", "Liam", "Sophia", "Noah", "Olivia", "Ethan", "Ava", "Mason", "Isabella"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Joshi", "Mehta", "Nair", "Rao",
              "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

TOPICS_DATA = [
    {"TopicID": "T101", "Title": "Arrays & Hash Maps", "Category": "Data Structures", "Difficulty": "Easy", "Prerequisites": "None", "Description": "Fundamental linear data structures, contiguous memory allocation, constant time lookups."},
    {"TopicID": "T102", "Title": "Linked Lists & Doubly Linked Lists", "Category": "Data Structures", "Difficulty": "Easy", "Prerequisites": "Arrays & Hash Maps", "Description": "Node-based dynamic data structures, pointer manipulation, structural traversal."},
    {"TopicID": "T103", "Title": "Stacks & Queues", "Category": "Data Structures", "Difficulty": "Medium", "Prerequisites": "Linked Lists", "Description": "LIFO and FIFO operations, call stack simulation, queue scheduling."},
    {"TopicID": "T104", "Title": "Trees & Binary Search Trees", "Category": "Data Structures", "Difficulty": "Medium", "Prerequisites": "Stacks & Queues", "Description": "Hierarchical tree structures, balanced BSTs, depth-first and breadth-first search."},
    {"TopicID": "T105", "Title": "Graph Algorithms", "Category": "Algorithms", "Difficulty": "Hard", "Prerequisites": "Trees & Binary Search Trees", "Description": "Dijkstra's algorithm, BFS/DFS traversals, topological sort, shortest paths."},
    {"TopicID": "T106", "Title": "Sorting & Searching Algorithms", "Category": "Algorithms", "Difficulty": "Medium", "Prerequisites": "Arrays & Hash Maps", "Description": "QuickSort, MergeSort, Binary Search, and time complexity analysis."},
    {"TopicID": "T107", "Title": "Dynamic Programming", "Category": "Algorithms", "Difficulty": "Hard", "Prerequisites": "Trees & Binary Search Trees", "Description": "Memoization, tabulation, subproblem optimization, memoization tables."},
    {"TopicID": "T108", "Title": "Greedy Algorithms & Backtracking", "Category": "Algorithms", "Difficulty": "Hard", "Prerequisites": "Sorting & Searching Algorithms", "Description": "Optimal substructure, activity selection, N-Queens problem, state-space exploration."},
    {"TopicID": "T109", "Title": "System Design Basics & Caching", "Category": "System Design", "Difficulty": "Hard", "Prerequisites": "Arrays & Hash Maps", "Description": "LRU Cache design, load balancing, database indexing, horizontal scaling."},
    {"TopicID": "T110", "Title": "Machine Learning Foundations", "Category": "AI / ML", "Difficulty": "Medium", "Prerequisites": "Arrays & Hash Maps", "Description": "Linear regression, Random Forests, feature scaling, model evaluation."}
]

QUIZZES_DATA = [
    # Keeping this minimal to save space, but it's your exact original quiz data
    {"QuizID": "Q101", "TopicID": "T101", "Question": "What is the average time complexity of looking up a key in a Hash Map?", "OptionA": "O(1)", "OptionB": "O(n)", "OptionC": "O(log n)", "OptionD": "O(n^2)", "CorrectOption": "OptionA", "Explanation": "Hash Maps achieve O(1) average time complexity for lookups using direct index hashing."},
    {"QuizID": "Q102", "TopicID": "T101", "Question": "Which data structure uses contiguous memory blocks?", "OptionA": "Linked List", "OptionB": "Array", "OptionC": "Tree", "OptionD": "Graph", "CorrectOption": "OptionB", "Explanation": "Arrays allocate memory in contiguous sequential blocks."},
    {"QuizID": "Q103", "TopicID": "T102", "Question": "What advantage does a Doubly Linked List have over a Singly Linked List?", "OptionA": "Uses less memory", "OptionB": "Can traverse in both directions", "OptionC": "Faster random access", "OptionD": "Constant time sorting", "CorrectOption": "OptionB", "Explanation": "Doubly linked lists contain both previous and next pointers enabling bidirectional traversal."},
    {"QuizID": "Q104", "TopicID": "T103", "Question": "Which principle does a Stack data structure follow?", "OptionA": "FIFO (First In First Out)", "OptionB": "LIFO (Last In First Out)", "OptionC": "LILO (Last In Last Out)", "OptionD": "Random Order", "CorrectOption": "OptionB", "Explanation": "Stacks adhere to LIFO principles where the last inserted element is removed first."},
    {"QuizID": "Q105", "TopicID": "T104", "Question": "What is the maximum number of children a node can have in a Binary Tree?", "OptionA": "1", "OptionB": "2", "OptionC": "3", "OptionD": "Unlimited", "CorrectOption": "OptionB", "Explanation": "In a binary tree, every node has at most 2 child nodes (left and right)."},
    {"QuizID": "Q106", "TopicID": "T105", "Question": "Which algorithm is commonly used to find the shortest path in a weighted graph without negative weights?", "OptionA": "Kruskal's Algorithm", "OptionB": "Dijkstra's Algorithm", "OptionC": "Breadth First Search", "OptionD": "Floyd-Warshall Algorithm", "CorrectOption": "OptionB", "Explanation": "Dijkstra's algorithm finds single-source shortest paths in graphs with non-negative edge weights."},
    {"QuizID": "Q107", "TopicID": "T106", "Question": "What is the worst-case time complexity of QuickSort?", "OptionA": "O(n log n)", "OptionB": "O(n)", "OptionC": "O(n^2)", "OptionD": "O(log n)", "CorrectOption": "OptionC", "Explanation": "QuickSort degrades to O(n^2) when poor pivots (like already sorted elements) are chosen."},
    {"QuizID": "Q108", "TopicID": "T107", "Question": "What key technique does Dynamic Programming rely on to avoid redundant computations?", "OptionA": "Recursion only", "OptionB": "Memoization and Tabulation", "OptionC": "Randomization", "OptionD": "Greedy selection", "CorrectOption": "OptionB", "Explanation": "Dynamic Programming stores solved subproblem solutions via memoization or tabulation."},
    {"QuizID": "Q109", "TopicID": "T108", "Question": "What is the primary characteristic of a Greedy Algorithm?", "OptionA": "Makes locally optimal choices at each step", "OptionB": "Explores all possible state paths", "OptionC": "Revisits past decisions", "OptionD": "Uses matrix exponentiation", "CorrectOption": "OptionA", "Explanation": "Greedy algorithms pick the locally optimal choice hoping to find a global optimum."},
    {"QuizID": "Q110", "TopicID": "T109", "Question": "Which cache eviction policy removes the least recently used item first?", "OptionA": "FIFO", "OptionB": "LRU", "OptionC": "LFU", "OptionD": "Random", "CorrectOption": "OptionB", "Explanation": "LRU (Least Recently Used) discards items that haven't been accessed for the longest time."}
]

RESOURCES_DATA = [
    # Exact original resource data
    {"ResourceID": "R101", "TopicID": "T101", "Title": "Mastering Hash Tables in Python", "Type": "Video", "URL": "https://youtube.com/watch?v=hashtable_tutorial", "Difficulty": "Easy", "DurationMinutes": 25},
    {"ResourceID": "R102", "TopicID": "T101", "Title": "Array Memory Layouts Deep Dive", "Type": "Article", "URL": "https://geeksforgeeks.org/array-memory-allocation", "Difficulty": "Easy", "DurationMinutes": 15},
    {"ResourceID": "R103", "TopicID": "T102", "Title": "Linked List Visualizer & Code Exercises", "Type": "Interactive", "URL": "https://leetcode.com/explore/learn/card/linked-list", "Difficulty": "Easy", "DurationMinutes": 40},
    {"ResourceID": "R104", "TopicID": "T103", "Title": "Stacks & Queues Crash Course", "Type": "Video", "URL": "https://youtube.com/watch?v=stacks_queues", "Difficulty": "Medium", "DurationMinutes": 30},
    {"ResourceID": "R105", "TopicID": "T104", "Title": "Binary Trees & BFS/DFS Traversals", "Type": "Article", "URL": "https://geeksforgeeks.org/binary-tree-data-structure", "Difficulty": "Medium", "DurationMinutes": 35},
    {"ResourceID": "R106", "TopicID": "T105", "Title": "Dijkstra & Graph Shortest Path Visualized", "Type": "Interactive", "URL": "https://visualgo.net/en/sssp", "Difficulty": "Hard", "DurationMinutes": 50},
    {"ResourceID": "R107", "TopicID": "T106", "Title": "Sorting Algorithms Benchmark & Guide", "Type": "Article", "URL": "https://realpython.com/sorting-algorithms-python", "Difficulty": "Medium", "DurationMinutes": 20},
    {"ResourceID": "R108", "TopicID": "T107", "Title": "Dynamic Programming for Beginners to Advanced", "Type": "Video", "URL": "https://youtube.com/watch?v=dp_masterclass", "Difficulty": "Hard", "DurationMinutes": 60},
    {"ResourceID": "R109", "TopicID": "T108", "Title": "Backtracking & N-Queens Guide", "Type": "Article", "URL": "https://leetcode.com/articles/n-queens", "Difficulty": "Hard", "DurationMinutes": 45},
    {"ResourceID": "R110", "TopicID": "T109", "Title": "Building an LRU Cache from Scratch", "Type": "Interactive", "URL": "https://leetcode.com/problems/lru-cache", "Difficulty": "Hard", "DurationMinutes": 40}
]

def generate_students_csv(num_records=2200):
    np.random.seed(42)
    random.seed(42)

    topics_list = [t["Title"] for t in TOPICS_DATA]
    learning_styles = ["Visual", "Auditory", "Kinesthetic"]
    education_levels = ["High School", "UG", "PG"]
    gender_list = ["Male", "Female"]
    outcomes_list = ["Fail", "Fair", "Good", "Excellent"]

    records = []
    
    # -----------------------------------------------
    # FIXED INDENTATION & LOGIC
    # -----------------------------------------------
    for i in range(1, num_records + 1):
        student_id = f"STU{i:04d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        age = random.randint(18, 26)
        gender = random.choice(gender_list)
        edu = random.choice(education_levels)
        style = random.choice(learning_styles)
        gpa = round(random.uniform(2.0, 4.0), 2)
        
        topics_completed_count = random.randint(1, 10)
        curr_topic = random.choice(topics_list)
        comp_topics_sample = random.sample(topics_list, k=min(topics_completed_count, len(topics_list)))
        completed_topics_str = ", ".join(comp_topics_sample)
        
        # DEFINE QUIZ SCORE BEFORE THE IF STATEMENT
        quiz_score = int(np.random.normal(loc=72, scale=15))
        quiz_score = max(30, min(100, quiz_score))

        attempts = random.randint(1, 5)
        time_spent_min = round(random.uniform(15.0, 60.0), 1)
        progress_pct = min(100, int((topics_completed_count / len(topics_list)) * 100))
        engagement = random.randint(60, 100)
        distraction = random.randint(0, 5)

        # 15% random noise for realism
        noise = random.random() < 0.15 

        # NEW LOGIC CONNECTING FEATURES TO PREDICTION
        if quiz_score < 60:
            if noise: 
                next_topic = random.choice(["Arrays & Hash Maps", "Linked Lists & Doubly Linked Lists"])
            else: 
                next_topic = "Arrays & Hash Maps" if attempts > 2 else "Linked Lists & Doubly Linked Lists"
            outcome = random.choice(["Fail", "Fair"])
            
        elif quiz_score < 75:
            if noise: 
                next_topic = random.choice(["Stacks & Queues", "Sorting & Searching Algorithms", "Machine Learning Foundations"])
            else:
                if style == "Visual": next_topic = "Stacks & Queues"
                elif style == "Auditory": next_topic = "Sorting & Searching Algorithms"
                else: next_topic = "Machine Learning Foundations"
            outcome = random.choice(["Fair", "Good"])
            
        elif quiz_score < 88:
            if noise: 
                next_topic = random.choice(["Trees & Binary Search Trees", "Greedy Algorithms & Backtracking"])
            else:
                if edu == "High School": next_topic = "Trees & Binary Search Trees"
                else: next_topic = "Greedy Algorithms & Backtracking"
            outcome = random.choice(["Good", "Excellent"])
            
        else:
            if noise: 
                next_topic = random.choice(["Graph Algorithms", "Dynamic Programming", "System Design Basics & Caching"])
            else:
                if gpa > 3.5: next_topic = "Graph Algorithms"
                elif gpa > 3.0: next_topic = "Dynamic Programming"
                else: next_topic = "System Design Basics & Caching"
            outcome = "Excellent"

        prev_rec = f"M1 -> M{random.randint(2,4)} -> M{random.randint(4,6)}"
        diff_level = random.choice(["Easy", "Medium", "Hard"])
        path_eff = random.randint(70, 100)
        final_score = min(100, max(40, quiz_score + random.randint(-10, 10)))

        records.append({
            "StudentID": student_id, "Name": name, "Age": age, "Gender": gender,
            "EducationLevel": edu, "LearningStyle": style, "PreviousGPA": gpa,
            "QuizScore": quiz_score, "Attempts": attempts, "TimeSpent": time_spent_min,
            "Progress": progress_pct, "CurrentTopic": curr_topic, "CompletedTopics": completed_topics_str,
            "EngagementScore": engagement, "DistractionEvents": distraction,
            "ContextualDifficulty": diff_level, "PreviousRecommendation": prev_rec,
            "PathEfficiency": path_eff, "FinalAssessmentScore": final_score,
            "LearningOutcome": outcome, "NextTopic": next_topic
        })

    # PROPERLY INDENTED OUTSIDE THE LOOP
    return pd.DataFrame(records)

def generate_all_datasets():
    os.makedirs(DATASET_DIR, exist_ok=True)
    students_df = generate_students_csv(num_records=2200)
    students_df.to_csv(os.path.join(DATASET_DIR, "students.csv"), index=False)
    pd.DataFrame(TOPICS_DATA).to_csv(os.path.join(DATASET_DIR, "topics.csv"), index=False)
    pd.DataFrame(QUIZZES_DATA).to_csv(os.path.join(DATASET_DIR, "quizzes.csv"), index=False)
    pd.DataFrame(RESOURCES_DATA).to_csv(os.path.join(DATASET_DIR, "resources.csv"), index=False)
    print("[+] Saved all 4 CSV datasets.")

if __name__ == "__main__":
    generate_all_datasets()