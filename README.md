
# 🎓 Dynamic Video Generation for Personalized Learning

This project dynamically generates educational video transcripts tailored to a student's learning level and subject. It uses **Generative AI** to produce a personalized explanation and **gTTS** to convert the response into speech—ideal for creating educational videos or audio lessons.

---

## 📌 Features

- 🔍 Takes user input: query, context (subject), and student standard (grade level)
- 🧠 Uses **Gemini Pro (Google Generative AI)** to generate an educational transcript
- 🔊 Converts text to speech using **Google Text-to-Speech (gTTS)**
- 🌐 Simple Flask web interface for interaction
- 📁 Saves audio files for video generation or playback

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI Model**: Google Gemini Pro (via `google.generativeai`)
- **Text-to-Speech**: gTTS
- **Frontend**: HTML (Jinja2 templating)
- **Hosting Ready**: Can be deployed using Render, Replit, or Railway

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/soiboie/Dynamic-Video-Generation-for-Personalized-Learning.git
cd Dynamic-Video-Generation-for-Personalized-Learning

pip install -r requirements.txt
```
# Run the app
```bash
python app.py
```
# Project Structure 
.
├── app.py                  # Main Flask app
├── templates/
│   └── index.html          # HTML form
├── static/
│   └── response_audio.mp3  # Generated audio output
├── requirements.txt
└── README.md




