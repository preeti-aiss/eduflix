import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Set page configuration
st.set_page_config(page_title="PDP Session: AI EduFlix Engine", layout="wide")
st.title("🤖 EduFlix AI Smart Content Generation Engine")
st.markdown("**Professional Development Program (PDP) Demonstration** | *Class XII CS Domain*")

# API Configuration
st.sidebar.header("🔑 API Configurations")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# --- Initialize Session State ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'level' not in st.session_state: st.session_state.level = "Beginner"
if 'quiz_done' not in st.session_state: st.session_state.quiz_done = False
if 'selected_topic' not in st.session_state: st.session_state.selected_topic = "Data Structures"

# --- Helper Functions ---

def generate_ai_content(topic, difficulty, concept, marks):
    if not api_key:
        return "⚠️ Please enter a valid Gemini API Key in the sidebar."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.5-flash')
        prompt_template = f"""
        You are an expert Computer Science teacher for Class XII.
        Generate a targeted revision resource for the '{difficulty}' level.
        Topic: {topic} | Concept: {concept} | Marks: {marks}
        
        Format as:
        ### 💡 Dynamic Concept Notes
        ### 💻 Executable Model Code Template
        ### 🎯 Handcrafted Practical Challenge
        """
        response = model.generate_content(prompt_template)
        return response.text if response.text else "❌ The AI generated an empty response."
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

def fetch_syllabus_row(topic_selected, student_tier):
    csv_file = "cs_syllabus.csv"
    if not os.path.exists(csv_file):
        return {"core_concept": "File not found", "expected_marks": "N/A"}
        
    df = pd.read_csv(csv_file)
    if 'topic' not in df.columns or 'difficulty' not in df.columns:
        return {"core_concept": "Invalid CSV structure", "expected_marks": "N/A"}

    match = df[(df['topic'] == topic_selected) & (df['difficulty'] == student_tier)]
    if not match.empty:
        return match.iloc[0].to_dict()
    
    return {"core_concept": "General Concepts", "expected_marks": "Variable"}

# --- UI Logic ---
if st.sidebar.button("Reset Student Assessment"):
    st.session_state.score = 0
    st.session_state.level = "Beginner"
    st.session_state.quiz_done = False
    st.rerun()

# Select topic
selected_topic = st.sidebar.selectbox("Select Topic", ["Data Structures", "Networking"])
st.session_state.selected_topic = selected_topic

# Columns Defined BEFORE being referenced
col1, col2 = st.columns(2)

with col1:
    st.header("📝 Student Assessment")
    st.write(f"**Current Level:** {st.session_state.level}")
    st.write(f"**Current Score:** {st.session_state.score}")
    
    # Simple Quiz Implementation
    with st.form("assessment_form"):
        answer = st.radio(f"Quick check: Is '{st.session_state.selected_topic}' an important topic?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit Answer")
        
        if submitted:
            if answer == "Yes":
                st.session_state.score += 10
                st.success("Correct! Score updated.")
            else:
                st.error("Incorrect. Try again!")
    
    # Logic to upgrade level based on score
    if st.session_state.score >= 20 and st.session_state.level == "Beginner":
        st.session_state.level = "Advanced"
        st.info("🎉 You've been promoted to the Advanced level!")

with col2:
    st.header("📚 Generated AI Learning Materials")
    
    # Fetch data
    metadata = fetch_syllabus_row(st.session_state.selected_topic, st.session_state.level)
    
    st.warning(f"📖 **Topic:** {st.session_state.selected_topic} | **Tier:** {st.session_state.level}")
    
    if st.button("✨ Generate AI Curriculum Material", type="primary"):
        with st.spinner("AI Teacher is generating custom notes..."):
            ai_output = generate_ai_content(
                st.session_state.selected_topic, 
                st.session_state.level, 
                metadata.get('core_concept', 'N/A'), 
                metadata.get('expected_marks', 'N/A')
            )
            if "❌" in ai_output or "⚠️" in ai_output:
                st.error(ai_output)
            else:
                st.markdown(ai_output)
