import streamlit as st
import os
import groq
from functools import lru_cache

# -------------------------
#  Setup & Configuration
# -------------------------

# Safe API key retrieval (support both secrets and environment variables)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ API key not found. Please set it in Streamlit secrets or environment variables.")
    st.stop()

client = groq.Client(api_key=GROQ_API_KEY)

# Supported languages (constant so it's easily maintainable)
LANGUAGES = [
    "Python", "Java", "C", "C++", "JavaScript", "Ruby", "PHP", "Go", "Swift",
    "Kotlin", "Rust", "TypeScript", "HTML", "CSS", "SQL", "R", "MATLAB", "Lua",
    "Shell", "Perl", "Scala", "Dart", "Haskell", "Objective-C", "VHDL", "Verilog",
    "Julia", "F#", "Groovy", "Assembly Language"
]

# -------------------------
#  Core AI Function
# -------------------------

@lru_cache(maxsize=100)  # cache repeated queries
def ai_translate(src_lang: str, tgt_lang: str, user_input: str) -> str:
    """Translate code from src_lang to tgt_lang using Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": (
                    f"Convert the following code from {src_lang} to {tgt_lang}:\n\n{user_input}\n\n"
                    "Only provide the translated code. No explanations unless required by syntax."
                ),
            }],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# -------------------------
#  UI Layer
# -------------------------

def chatbot_ui():
    """Streamlit UI for the translator app."""
    st.title("🌍 Code Translator")
    st.caption("Powered by Groq LLaMA 3.3 – Translate between 30+ languages seamlessly")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        src_lang = st.selectbox("Convert from:", LANGUAGES, index=0)

    with col2:
        tgt_lang = st.selectbox("Convert to:", LANGUAGES, index=1)

    user_input = st.text_area(
        "Enter your code here:",
        placeholder=f"Paste {src_lang} code to translate into {tgt_lang}..."
    )

    if st.button("🚀 Translate", use_container_width=True):
        if not user_input.strip():
            st.warning("⚠️ Please enter some code to translate.")
        else:
            with st.spinner("Translating..."):
                translation = ai_translate(src_lang, tgt_lang, user_input)
                st.subheader("✅ Translated Code:")
                st.code(translation, language=tgt_lang.lower() if tgt_lang != "Assembly Language" else "")

    # Maintain chat history (optional FAANG touch)
    if "history" not in st.session_state:
        st.session_state.history = []

    if user_input.strip():
        st.session_state.history.append((src_lang, tgt_lang, user_input))

    if st.session_state.history:
        with st.expander("📜 Translation History"):
            for i, (s, t, code) in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**{i}. {s} ➝ {t}**")
                st.code(code, language=s.lower())

# -------------------------
#  Run App
# -------------------------
if __name__ == "__main__":
    chatbot_ui()
