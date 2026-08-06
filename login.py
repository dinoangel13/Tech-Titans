import streamlit as st
from database import login_user, register_user

def render_login_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #6C5CE7; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.2rem;">
                🧠 PathAI Learning System
            </h1>
            <p style="color: #A0AEC0; font-size: 1.1rem;">
                AI-Powered Personalized Recommendation & Adaptive Learning Path Engine
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Register Student"])

        with tab_login:
            st.markdown("### Welcome Back")
            login_email = st.text_input("Email Address", key="login_email", placeholder="student@student.edu")
            login_pwd = st.text_input("Password", type="password", key="login_pwd", placeholder="••••••••")
            
            if st.button("🚀 Log In", use_container_width=True, type="primary"):
                if not login_email or not login_pwd:
                    st.error("Please enter both email and password.")
                else:
                    user = login_user(login_email, login_pwd)
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user
                        st.session_state['role'] = user['role']
                        st.session_state['student_id'] = user.get('student_id', 'STU0001')
                        st.success(f"Welcome back, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")

            st.markdown("""
                <div style="background: rgba(108, 92, 231, 0.08); border-left: 4px solid #6C5CE7; padding: 12px; border-radius: 6px; margin-top: 20px;">
                    <p style="font-size: 0.85rem; margin: 0; color: #CBD5E0;">
                        <b>Demo Credentials:</b><br>
                        • <b>Student:</b> stu0001@student.edu | password: <code>student123</code><br>
                        • <b>Teacher:</b> teacher@edu.com | password: <code>teacher123</code><br>
                        • <b>Admin:</b> admin@edu.com | password: <code>admin123</code>
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with tab_register:
            st.markdown("### Create New Account")
            reg_name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
            reg_email = st.text_input("Email Address", key="reg_email", placeholder="john@student.edu")
            reg_pwd = st.text_input("Password", type="password", key="reg_pwd", placeholder="Create password")
            reg_stu_id = st.text_input("Student ID", key="reg_stu_id", value="STU" + str(st.session_state.get('rand_id', '9999')))
            
            if st.button("✨ Create Account", use_container_width=True):
                if not reg_name or not reg_email or not reg_pwd:
                    st.error("Please fill in all required fields.")
                else:
                    success, msg = register_user(reg_name, reg_email, reg_pwd, role='student', student_id=reg_stu_id)
                    if success:
                        st.success(msg + " You can now log in.")
                    else:
                        st.error(msg)