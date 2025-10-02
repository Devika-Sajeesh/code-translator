import streamlit as st
import os
import groq
import time
import sqlalchemy as db

# -------------------------
#  Setup & Config
# -------------------------

# Safe API key retrieval
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ API key not found. Set it in Streamlit secrets or environment variables.")
    st.stop()

client = groq.Client(api_key=GROQ_API_KEY)

# Setup DB (SQLite for history persistence)
engine = db.create_engine("sqlite:///translations.db")
connection = engine.connect()
metadata = db.MetaData()

translations = db.Table(
    "translations", metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("src_lang", db.String(50)),
    db.Column("tgt_lang", db.String(50)),
    db.Column("input_code", db.Text),
    db.Column("output_code", db.Text),
    db.Column("latency", db.Float),
)

metadata.create_all(engine)


# -------------------------
#  Core AI Function (Sync)
# -------------------------

def ai_translate(src_lang: str, tgt_lang: str, user_input: str):
    """Translate code using Groq API (synchronous)."""
    start_time = time.time()
    try:
        completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Convert this {src_lang} code into {tgt_lang}:\n{user_input}\n\nOnly return valid code."
            }],
            model="llama-3.3-70b-versatile",
        )
        output = completion.choices[0].message.content.strip()
        latency = round(time.time() - start_time, 2)

        # Save to DB
        ins = translations.insert().values(
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            input_code=user_input,
            output_code=output,
            latency=latency,
        )
        connection.execute(ins)

        return output, latency
    except Exception as e:
        return f"⚠️ Error: {str(e)}", 0.0


# -------------------------
#  UI Layer
# -------------------------

LANGUAGES = [
    "Python", "Java", "C", "C++", "JavaScript", "Ruby", "PHP", "Go", "Swift",
    "Kotlin", "Rust", "TypeScript", "HTML", "CSS", "SQL", "R", "MATLAB", "Lua",
    "Shell", "Perl", "Scala", "Dart", "Haskell", "Objective-C", "VHDL", "Verilog",
    "Julia", "F#", "Groovy", "Assembly Language"
]

def chatbot_ui():
    st.title("🌍 Code Translator ")
    st.caption("Translate code between 30+ languages. Translations are saved with latency tracking.")

    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("Convert from:", LANGUAGES, index=0)
    with col2:
        tgt_lang = st.selectbox("Convert to:", LANGUAGES, index=1)

    # User code input
    user_input = st.text_area(
        "Paste your code here:",
        placeholder=f"Enter {src_lang} code..."
    )

    # Translate button
    if st.button("🚀 Translate"):
        if not user_input.strip():
            st.warning("⚠️ Please enter code before translating.")
        else:
            st.write("Translating…")
            translated, latency = ai_translate(src_lang, tgt_lang, user_input)
            st.code(translated, language=tgt_lang.lower() if tgt_lang != "Assembly Language" else "")
            if latency > 0:
                st.success(f"✅ Translation completed in {latency} seconds")

    # Show last 5 translations
    st.subheader("📜 Translation History (Last 5)")
    result = connection.execute(
        db.select(translations).order_by(translations.c.id.desc()).limit(5)
    )
    for row in result:
        with st.expander(f"{row.src_lang} ➝ {row.tgt_lang} (took {row.latency}s)"):
            st.code(row.input_code, language=row.src_lang.lower())
            st.code(row.output_code, language=row.tgt_lang.lower())


if __name__ == "__main__":
    chatbot_ui()
