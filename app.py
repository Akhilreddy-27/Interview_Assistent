import streamlit as st
import os
import re
import time
from dotenv import load_dotenv
from google import genai
import PyPDF2  
from gtts import gTTS
import io
from streamlit_ace import st_ace
import streamlit.components.v1 as components

# -------------------------
# Page Config MUST be the very first Streamlit command
# -------------------------
st.set_page_config(page_title="Interview Assassin", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# -------------------------
# Advanced Premium UI Styling
# -------------------------
st.markdown("""
<style>
/* Import modern font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

/* Global Font & Background */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background-color: #0f172a;
    background-image: 
        radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
        radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
        radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
    color: #f8fafc;
}

/* ===== Sidebar Styling ===== */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* ===== Animated Neon Title ===== */
.hero-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 0px;
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc, #38bdf8);
    background-size: 200% auto;
    color: #000;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.hero-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.2rem;
    margin-bottom: 40px;
    letter-spacing: 1px;
}

/* ===== Glassmorphism Cards ===== */
.glass-card {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.3);
}

/* ===== Input Fields ===== */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: white !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
    background-color: rgba(15, 23, 42, 0.9) !important;
}

/* ===== Epic Buttons ===== */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    color: white !important;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.8rem;
    border: none !important;
    border-radius: 12px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5);
    background: linear-gradient(135deg, #7dd3fc 0%, #a5b4fc 100%);
}

.stButton > button:active {
    transform: translateY(1px);
}

/* ===== Chat Bubbles for Q&A ===== */
.ai-bubble {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(129, 140, 248, 0.05));
    border-left: 4px solid #38bdf8;
    padding: 1.5rem;
    border-radius: 0 15px 15px 15px;
    margin-bottom: 20px;
}

/* ===== Evaluation Badges ===== */
.score-badge {
    padding: 10px 20px;
    border-radius: 50px;
    font-weight: 800;
    font-size: 1.2rem;
    text-align: center;
    margin: 20px 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.score-elite { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid #10b981; box-shadow: 0 0 20px rgba(16,185,129,0.2); }
.score-strong { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid #3b82f6; }
.score-developing { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid #f59e0b; }
.score-improve { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid #ef4444; }

/* ===== Custom Slider Coloring ===== */
div[data-baseweb="slider"] div[data-testid="stTickBar"] {
    background-color: #38bdf8 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Load API Key
# -------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found. Please ensure it is in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# -------------------------
# Session State Setup
# -------------------------
if "question" not in st.session_state:
    st.session_state.question = None
if "history" not in st.session_state:
    st.session_state.history = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration_seconds" not in st.session_state:
    st.session_state.duration_seconds = 120 # Default 2 mins

# -------------------------
# SIDEBAR: Setup & Configuration
# -------------------------
with st.sidebar:
    st.markdown("## ⚙️ Interview Setup")
    
    role = st.text_input("💼 Target Job Role", value="Software Engineering Intern")
    skills = st.text_area("🛠 Key Skills", value="C++, Data Structures, Algorithms")
    
    experience = st.selectbox("📈 Experience Level", ["Fresher","1-3 Years","3-5 Years","5+ Years"])
    interview_type = st.radio("🎤 Interview Type", ["Technical","Behavioral","HR"])
    difficulty = st.select_slider("🔥 Difficulty", options=["Normal", "Hard", "FAANG Level"])
    personality = st.selectbox("🧠 Interviewer Persona", ["Friendly", "Strict", "Aggressive", "Mentor"])
    
    # Dynamic Timer Selection
    st.markdown("---")
    st.markdown("### ⏱️ Timer Settings")
    timer_minutes = st.slider("Interview Duration (Minutes)", min_value=1, max_value=45, value=2)
    
    st.markdown("---")
    st.markdown("### 📄 Context Engine")
    resume = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
    resume_text = ""

    if resume:
        if resume.name.endswith(".pdf"):
            try:
                pdf_reader = PyPDF2.PdfReader(resume)
                for page in pdf_reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        resume_text += extracted_text + "\n"
                st.success("PDF synced!")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        elif resume.name.endswith(".txt"):
            resume_text = resume.read().decode("utf-8")
            st.success("Text synced!")

# -------------------------
# MAIN STAGE
# -------------------------
st.markdown("<div class='hero-title'>Interview Assassin</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>AI-Powered Technical & Behavioral Simulator</div>", unsafe_allow_html=True)

# Top Action Bar
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Generate Question", use_container_width=True):
        if role and skills:
            with st.spinner("Analyzing profile & generating question..."):
                prompt = f"""
                You are a {personality} senior interviewer.
                Generate ONE realistic {interview_type} interview question for the {role} position.
                Experience Level: {experience} | Skills: {skills} | Difficulty: {difficulty}.
                Resume Context: {resume_text if resume_text else "None. Rely on skills."}
                Instructions: Tailor the question to the provided skills/resume. Only provide the question text.
                """
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.session_state.question = response.text
                
                # Lock in the selected timer duration when question generates
                st.session_state.duration_seconds = timer_minutes * 60
                st.session_state.start_time = time.time() 
with col2:
    if st.button("⏱ Reset Timer", use_container_width=True):
        st.session_state.duration_seconds = timer_minutes * 60
        st.session_state.start_time = time.time()

# -------------------------
# Dynamic Timer Display
# -------------------------
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    total_time = st.session_state.duration_seconds
    remaining = total_time - elapsed
    
    if remaining > 0:
        timer_html = f"""
        <div id="timer" style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 600; color: #e2e8f0; padding: 15px; border-radius: 12px; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            ⏳ Time Remaining: <span id="time" style="color: #38bdf8; font-weight: 800; font-size: 1.3rem;">{remaining}</span> seconds
            <div style="width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 5px; margin-top: 10px; height: 8px;">
              <div id="progress-bar" style="height: 100%; width: {(remaining/total_time)*100}%; background: linear-gradient(90deg, #38bdf8, #818cf8); border-radius: 5px; transition: width 1s linear;"></div>
            </div>
        </div>
        <script>
            var timeLeft = {remaining};
            var totalTime = {total_time};
            var elem = document.getElementById('time');
            var bar = document.getElementById('progress-bar');
            var timer = document.getElementById('timer');
            var timerId = setInterval(countdown, 1000);
            
            function countdown() {{
                if (timeLeft <= 0) {{
                    clearTimeout(timerId);
                    timer.innerHTML = "⏰ <b>Time's up!</b> Please wrap up your answer.";
                    timer.style.border = "1px solid #ef4444";
                    timer.style.color = "#f87171";
                }} else {{
                    timeLeft--;
                    elem.innerHTML = timeLeft;
                    bar.style.width = (timeLeft / totalTime * 100) + '%';
                }}
            }}
        </script>
        """
        components.html(timer_html, height=100)
    else:
        st.error("⏰ Time's up! Wrap up your answer.")

st.markdown("---")

# -------------------------
# Question & Answer Arena
# -------------------------
if st.session_state.question:
    # THE QUESTION (AI Bubble)
    st.markdown(f"""
    <div class='glass-card'>
        <h4 style='color: #38bdf8; margin-bottom: 10px;'>Interviewer</h4>
        <div class='ai-bubble'>{st.session_state.question}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio Player hidden in a clean expander to save space
    with st.expander("🔊 Listen to Question"):
        try:
            tts = gTTS(text=st.session_state.question, lang='en', slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            st.audio(audio_fp, format='audio/mp3')
        except Exception as e:
            st.error(f"Failed to generate audio: {e}")

    # THE ANSWER WIDGET
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #a5b4fc; margin-bottom: 15px;'>Your Answer</h4>", unsafe_allow_html=True)
    
    final_answer = ""
    
    if interview_type == "Technical":
        st.caption("💻 C++ Environment Active. Watch your Big O!")
        code_answer = st_ace(
            language="c_cpp",
            theme="tomorrow_night",
            keybinding="vscode",
            font_size=15,
            tab_size=4,
            min_lines=15,
            key="ace_editor"
        )
        verbal_explanation = st.text_area("✍️ Approach & Big O Explanation:", height=80, placeholder="Explain your logic...")
        if code_answer:
            final_answer = f"Code:\n{code_answer}\n\nExplanation:\n{verbal_explanation}"
    else:
        st.caption("✍️ Type your response below.")
        final_answer = st.text_area("Your Response", height=150, placeholder="Use the STAR method (Situation, Task, Action, Result) for behavioral questions...", label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # Evaluation Engine
    # -------------------------
    if st.button("✨ Submit & Evaluate Response", use_container_width=True):
        if not final_answer.strip():
            st.warning("Please provide an answer before evaluating.")
        else:
            with st.spinner("Running deep analysis..."):
                if interview_type == "Technical":
                    evaluation_prompt = f"""
                    Evaluate this DSA/Systems answer strictly.
                    Question: {st.session_state.question}
                    Answer: {final_answer}
                    Score using:
                    Accuracy (0–25)
                    Optimization (0–20)
                    Edge Cases (0–20)
                    Cleanliness (0–15)
                    Explanation (0–20)
                    Return exactly:
                    Accuracy: X/25
                    Optimization: X/20
                    Edge Cases: X/20
                    Cleanliness: X/15
                    Explanation: X/20
                    Total: X/100
                    Then provide: Strengths:, Missed Edge Cases:, Big O Analysis:, Better Approach:
                    """
                else:
                    evaluation_prompt = f"""
                    Evaluate this behavioral answer strictly.
                    Question: {st.session_state.question}
                    Answer: {final_answer}
                    Score using:
                    Relevance (0–25)
                    STAR Method (0–20)
                    Impact (0–20)
                    Structure (0–15)
                    Clarity (0–20)
                    Return exactly:
                    Relevance: X/25
                    STAR Method: X/20
                    Impact: X/20
                    Structure: X/15
                    Clarity: X/20
                    Total: X/100
                    Then provide: Strengths:, Weaknesses:, Missed Opportunities:, How to Improve:
                    """

                eval_response = client.models.generate_content(model="gemini-2.5-flash", contents=evaluation_prompt)
                result_text = eval_response.text
                
                def extract_score(label, max_score):
                    match = re.search(rf"{label}:\s*(\d+)/{max_score}", result_text)
                    return int(match.group(1)) if match else 0

                total = extract_score("Total", 100)
                st.session_state.history.append(total)

                # Display Results in a stunning container
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📊 Performance Report")
                
                if total >= 90:
                    st.markdown(f"<div class='score-badge score-elite'>🏆 Elite ({total}/100)</div>", unsafe_allow_html=True)
                elif total >= 75:
                    st.markdown(f"<div class='score-badge score-strong'>💪 Strong ({total}/100)</div>", unsafe_allow_html=True)
                elif total >= 60:
                    st.markdown(f"<div class='score-badge score-developing'>📈 Developing ({total}/100)</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='score-badge score-improve'>⚠ Needs Work ({total}/100)</div>", unsafe_allow_html=True)

                st.write(result_text)
                
                if len(st.session_state.history) > 1:
                    st.markdown("#### 📉 Trend")
                    st.line_chart(st.session_state.history)
                    
                st.markdown("</div>", unsafe_allow_html=True)

else:
    # Placeholder when no question is generated yet
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; color: #64748b;'>
        <h2>Ready to begin?</h2>
        <p>Configure your profile in the sidebar and hit Generate Question.</p>
    </div>
    """, unsafe_allow_html=True)