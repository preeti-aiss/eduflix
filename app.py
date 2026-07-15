import streamlit as st
import pandas as pd
import google.generativeai as genai # Updated import for standard SDK
import os

# Set page configuration
st.set_page_config(page_title="PDP Session: AI EduFlix Engine", layout="wide")
st.title("🤖 EduFlix AI Smart Content Generation Engine")
st.markdown("**Professional Development Program (PDP) Demonstration** | *Class XII CS Domain*")

# API Configuration
st.sidebar.header("🔑 API Configurations")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

def generate_ai_content(topic, difficulty, concept, marks):
    if not api_key:
        return "⚠️ Please enter a valid Gemini API Key in the sidebar."
    
    try:
        # Configure the SDK
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash, which is the current stable, fast model
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
        
        # Call the model
        response = model.generate_content(prompt_template)
        
        # Safety check: if the response is blocked or empty
        if response.text:
            return response.text
        else:
            return "❌ The AI generated an empty response. Please try a different topic."
            
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

def fetch_syllabus_row(topic_selected, student_tier):
    csv_file = "cs_syllabus.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        match = df[(df['topic'] == topic_selected) & (df['difficulty'] == student_tier)]
        if not match.empty:
            # FIXED: Corrected .iloc(0) to .iloc[0]
            return match.iloc[0].to_dict() 
    return {"core_concept": "General Concepts", "expected_marks": "Variable"}

# ... [Keep your existing session state and quiz logic here] ...

with col2:
    st.header("📚 Generated AI Learning Materials")
    metadata = fetch_syllabus_row(selected_topic, st.session_state.level)
    st.warning(f"📖 **Topic:** {selected_topic} | **Tier:** {st.session_state.level}")
    
    if st.button("✨ Generate AI Curriculum Material", type="primary"):
        with st.spinner("AI Teacher is generating custom notes..."):
            ai_output = generate_ai_content(selected_topic, st.session_state.level, metadata['core_concept'], metadata['expected_marks'])
            
            # Display error in UI if present
            if "❌" in ai_output or "⚠️" in ai_output:
                st.error(ai_output)
            else:
                st.markdown(ai_output)
