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
# Ensure selected_topic is initialized
if 'selected_topic' not in st.session_state: st.session_state.selected_topic = "Data Structures" 

def generate_ai_content(topic, difficulty, concept, marks):
    if not api_key:
        return "⚠️ Please enter a valid Gemini API Key in the sidebar."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
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
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        match = df[(df['topic'] == topic_selected) & (df['difficulty'] == student_tier)]
        if not match.empty:
            # Corrected: Using .iloc[0] to get the first matching row, then .to_dict()
            return match.iloc[0].to_dict()
    return {"core_concept": "General Concepts", "expected_marks": "Variable"}

# --- UI Logic ---
if st.sidebar.button("Reset Student Assessment"):
    st.session_state.score = 0
    st.session_state.level = "Beginner"
    st.session_state.quiz_done = False
    st.rerun()

# --- Columns Defined HERE before being referenced ---
col1, col2 = st.columns(2)

with col1:
    st.header("Student Assessment")
    st.write(f"Current Level: {st.session_state.level}")
    # Add your assessment logic here

with col2:
    st.header("📚 Generated AI Learning Materials")
    metadata = fetch_syllabus_row(st.session_state.selected_topic, st.session_state.level)
    st.warning(f"📖 **Topic:** {st.session_state.selected_topic} | **Tier:** {st.session_state.level}")
    
    if st.button("✨ Generate AI Curriculum Material", type="primary"):
        with st.spinner("AI Teacher is generating custom notes..."):
            ai_output = generate_ai_content(
                st.session_state.selected_topic, 
                st.session_state.level, 
                metadata['core_concept'], 
                metadata['expected_marks']
            )
            if "❌" in ai_output or "⚠️" in ai_output:
                st.error(ai_output)
            else:
                st.markdown(ai_output)
