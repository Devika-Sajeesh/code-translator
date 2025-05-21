import streamlit as st
import os
import groq

# AI setup - Use environment variables or Streamlit secrets for API keys
client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])

# Chatbot setup
def ai_chatbot(a, b, user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Convert the entered command inputted in {a} language to {b} language. The input is: {user_input} ",
            }
        ],
        model="llama-3.3-70b-versatile",  
    )
    return chat_completion.choices[0].message.content

def chatbot_ui(a, b):
    """Streamlit UI for the chatbot"""
    st.title("Code Translator")
    
    user_input = st.text_input("Please enter the command that should be converted. I will guide you:")
    
    if user_input:  
        if user_input.lower() == "exit":
            st.write("Goodbye! Feel free to come back anytime.")
        else:
            # Get the chatbot's response
            response = ai_chatbot(a, b, user_input)
            st.write(f"**BumbleBee🤖:** {response}")

# Create columns for alignment
col1, col2 = st.columns(2)

# Language selection in the first column
with col1:
    tochange_choice = st.selectbox("Choose the language to convert from:", [
        "Python", "Java", "C", "C++", "JavaScript", "Ruby", "PHP", "Go", "Swift", 
        "Kotlin", "Rust", "TypeScript", "HTML", "CSS", "SQL", "R", "MATLAB", "Lua", 
        "Shell", "Perl", "Scala", "Dart", "Haskell", "Objective-C", "VHDL", "Verilog", 
        "Julia", "F#", "Groovy", "Assembly Language"
    ])

# Language selection in the second column
with col2:
    ischange_choice = st.selectbox("Choose the language to convert to:", [
        "Python", "Java", "C", "C++", "JavaScript", "Ruby", "PHP", "Go", "Swift", 
        "Kotlin", "Rust", "TypeScript", "HTML", "CSS", "SQL", "R", "MATLAB", "Lua", 
        "Shell", "Perl", "Scala", "Dart", "Haskell", "Objective-C", "VHDL", "Verilog", 
        "Julia", "F#", "Groovy", "Assembly Language"
    ])

# Display the chatbot UI
chatbot_ui(tochange_choice, ischange_choice)