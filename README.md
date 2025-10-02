# Code Translator Web App

A web-based code translator built with **Streamlit** and **Groq LLaMA**, which allows users to convert code from one programming language to another (over 30 languages supported).

Live Demo: [Your App URL](https://devika-sajeesh-code-translator-duo-pilvnz.streamlit.app/)

---

## 🚀 Features

- Translate code snippets between many languages (e.g. Python, JavaScript, C++, Java, Rust, etc.)
- Clean and interactive UI using Streamlit
- Loading spinner & error handling
- History / past translations view (optional)
- API key management via **Streamlit secrets** or environment variables
- Caching to avoid redundant API calls

---

## 🧩 Project Structure

```

.
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── README.md # This documentation
└── ...

```

---

## 🛠️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

````

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   venv\Scripts\activate.bat      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**

   You need a Groq API key to use the translation backend. You can set it either:

   - In `~/.streamlit/secrets.toml`:

     ```toml
     GROQ_API_KEY = "your_groq_api_key_here"
     ```

   - Or as an environment variable:

     ```bash
     export GROQ_API_KEY="your_groq_api_key_here"
     ```

5. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

6. **Open your browser**

   By default, it should open at `http://localhost:8501`.

---

## 📐 Usage

1. Choose the **source language** (language you have code in).
2. Choose the **target language** (language you want to translate to).
3. Paste your code snippet (or command) in the input box.
4. Click **Translate**.
5. The translated code appears below.
6. You can optionally view your translation history in an expandable panel.

To exit or reset, simply clear the input or refresh the page.

---

## 🪄 Architecture Notes & Best Practices

- The **translation logic** is isolated in a function (`ai_translate`) with caching, so you can evolve it (e.g. add streaming or alternative models) independently of the UI.
- Error handling ensures graceful failure if the API is unreachable or the key is invalid.
- The UI is modular and uses **Streamlit columns**, spinners, and session-state for user experience polish.
- API keys are never hard-coded — it reads from secrets or environment variables to follow security best practices.
- You can extend this by adding:

  - Token-level streaming responses
  - Rate limiting
  - User authentication
  - Saving user preferences or history to a database
  - Logging & monitoring (e.g. via Sentry)

---

## 📦 Dependencies

Key libraries used:

- `streamlit`
- `groq`
- `functools` (for caching)
- Standard Python libs (`os`, etc.)

You can freeze them using:

```bash
pip freeze > requirements.txt
```

---

## ✅ Contributing & License

Feel free to open issues, suggest features, or pull requests!

This project is licensed under the **MIT License** — see `LICENSE` for details.

---

## 🙋 Acknowledgements

- Built with **Streamlit**
- Powered by **Groq LLaMA 3.3** for generative code translation
- Inspired by many AI-based code conversion tools

``

```

```
````
