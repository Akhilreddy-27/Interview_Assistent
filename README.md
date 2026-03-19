<div align="center">
  
  # 🔥 Interview Assassin
  
  **An AI-powered interviewer to help prep for technical and behavioral rounds.**
  
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)
  [![Google Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](#)
  [![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)](#)

  [**🔴 Try the Live App Here**](https://interviewassistent-9it3tptyvyyfezk8uz7y6e.streamlit.app/)
  
</div>

---

## What is this?

I built this app to help practice for software engineering internships and technical rounds. Instead of just grinding generic Leetcode problems, I wanted an AI that could look at my actual resume, ask targeted questions, and then ruthlessly grade my code and explanations.

It uses Google's Gemini 2.5 Flash API under the hood and is wrapped in a heavily customized Streamlit interface.

---

## Features

* **Resume Parsing (RAG):** You can upload your resume (PDF/TXT). The app parses it using `PyPDF2` and feeds it to the LLM so the interviewer actually asks about your specific projects and tech stack.
* **Built-in C++ Editor:** Standard text boxes are terrible for writing code. I integrated `streamlit-ace` so you can write actual algorithms with syntax highlighting, right in the browser.
* **Strict Grading Engine:** The AI acts as a tough hiring manager. It grades technical answers on Big O complexity, edge cases, and optimization. For behavioral questions, it grades based on the STAR method.
* **Async JavaScript Timer:** To simulate real interview pressure, I injected custom JS/HTML into Streamlit to create a live countdown timer that doesn't block or freeze the Python backend.
* **Custom UI:** Wrote custom CSS to overwrite Streamlit's default layout, adding dark mode, glassmorphism cards, and a cleaner sidebar setup.

---

## How it works under the hood

1. **Setup:** User sets the target role, difficulty, and uploads their resume.
2. **Prompt Generation:** Gemini generates a specific question based on the provided context.
3. **Execution:** User types their code/answer while the injected JS timer ticks down.
4. **Evaluation Pipeline:** The response is sent back to Gemini with a strict grading rubric prompt. The app extracts the JSON-style scores using Regex to display badges and a historical performance chart.

---

## Run it locally

Want to try running it on your own machine?

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Akhilreddy-27/Interview_Assistent.git](https://github.com/Akhilreddy-27/Interview_Assistent.git)
   cd Interview_Assistent
