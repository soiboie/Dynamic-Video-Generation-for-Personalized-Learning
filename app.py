from flask import Flask, render_template, request

app = Flask(__name__) 
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    audio_file = ""
    if request.method == "POST":
        user_input = request.form.get("query")
        educational_context = request.form.get("context")
        student_standard = request.form.get("standard")  # New field for student standard
        if user_input:
            # Start a chat with an educational context and student standard
            full_prompt = (
                f"You are an educational tutor. The topic is: {educational_context}. "
                f"Provide a detailed transcript for a 2-3 minute video."
                f"The explanation should be tailored for a student of {student_standard} standard. "
                f"Now, answer this question: {user_input}"
            )
            chat = model.start_chat(history=[])
            response = chat.send_message(full_prompt)
            transcript = response.text

            # Convert the response text to speech using gTTS
            tts = gTTS(text=transcript, lang='en')
            audio_file = "static/response_audio.mp3"
            tts.save(audio_file)

    return render_template("index.html", transcript=transcript, audio_file=audio_file)

if __name__ == "__main__":
    # Ensure the static folder exists for audio files
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
