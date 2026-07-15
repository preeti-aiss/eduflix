import streamlit as st
import pandas as pd
from openai import OpenAI  # Changed from google import genai
import os

# Set page configuration
st.set_page_config(page_title="PDP Session: AI EduFlix Engine", layout="wide")
st.title("🤖 EduFlix AI Smart Content Generation Engine")
st.markdown("**Professional Development Program (PDP) Demonstration** | *Class XII CS Domain*")

# API Configuration
st.sidebar.header("🔑 API Configurations")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

def generate_ai_content(topic, difficulty, concept, marks):
    if not api_key:
        return "⚠️ Please enter a valid OpenAI API Key in the sidebar."
    try:
        # Initialize OpenAI Client
        client = OpenAI(api_key=api_key)
        
        prompt_content = f"""
        You are an expert Computer Science teacher for CBSE/ISC Class XII (Subject Code 083).
        Generate a highly targeted revision resource for a student evaluated at the '{difficulty}' level.
        
        Topic: {topic}
        Specific Syllabus Concept: {concept}
        Exam Weighting: Approximately {marks} Marks
        
        Please provide your response strictly divided into these three sections using clear Markdown headers:
        ###  Dynamic Concept Notes
        
        ###  Executable Model Code Template
        
        ###  Handcrafted Practical Challenge
        """
        
        # Calling OpenAI's stable gpt-4o-mini model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_content}]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"ERROR_OCCURRED: {str(e)}"

def fetch_syllabus_row(topic_selected, student_tier):
    csv_file = "cs_syllabus.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        match = df[(df['topic'] == topic_selected) & (df['difficulty'] == student_tier)]
        if not match.empty:
            return match.iloc[0].to_dict()
    return {"core_concept": "General Concepts", "expected_marks": "Variable"}

# Initialize session state
if 'score' not in st.session_state: st.session_state.score = 0
if 'level' not in st.session_state: st.session_state.level = "Beginner"
if 'quiz_done' not in st.session_state: st.session_state.quiz_done = False

selected_topic = st.sidebar.selectbox("Choose Syllabus Domain:", ["Python Functions", "File Handling", "SQL Databases"])

if st.sidebar.button("Reset Student Assessment"):
    st.session_state.score = 0
    st.session_state.level = "Beginner"
    st.session_state.quiz_done = False
    st.rerun()

col1, col2 = st.columns(2)

with col1:
    st.header("🧪 Level Evaluator")
    if not st.session_state.quiz_done:
        st.info(f"Targeting: **{st.session_state.level}** tier.")
        if st.session_state.level == "Beginner":
            q, opts, ans = "Extension of Python source file?", [".txt", ".py", ".csv", ".dat"], ".py"
        elif st.session_state.level == "Intermediate":
            q, opts, ans = "Function to find total items in list?", ["count()", "size()", "length()", "len()"], "len()"
        else:
            q, opts, ans = "SQL keyword to eliminate duplicates?", ["UNIQUE", "DISTINCT", "CHECK", "GROUP BY"], "DISTINCT"

        user_input = st.radio(q, opts, key=f"q_{st.session_state.level}")
        if st.button("Submit Answer"):
            if user_input == ans:
                st.session_state.score += 1
                if st.session_state.level == "Beginner": st.session_state.level = "Intermediate"
                elif st.session_state.level == "Intermediate": st.session_state.level = "Advanced"
                else: st.session_state.quiz_done = True
            else:
                st.session_state.quiz_done = True
            st.rerun()
    else:
        st.success("✅ Assessment Complete!")
        st.metric("Assessed Mastery Tier", st.session_state.level)

with col2:
    st.header("📚 Generated AI Learning Materials")
    metadata = fetch_syllabus_row(selected_topic, st.session_state.level)
    st.warning(f"📖 **Topic:** {selected_topic} | **Tier:** {st.session_state.level}")
    
    if st.button("✨ Generate AI Curriculum Material", type="primary"):
        with st.spinner("AI Teacher is generating custom notes..."):
            ai_output = generate_ai_content(selected_topic, st.session_state.level, metadata['core_concept'], metadata['expected_marks'])
            
            if "ERROR_OCCURRED" in ai_output:
                st.error("The AI service is currently experiencing high demand. Please try again.")
                with st.expander("Technical Details"):
                    st.code(ai_output)
            else:
                st.markdown(ai_output)
