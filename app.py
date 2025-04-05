from flask import Flask, render_template, request
import google.generativeai as genai
from gtts import gTTS
import os

app = Flask(__name__)

# Configure the Generative AI API
genai.configure(api_key="AIzaSyC4NQ7jjvgTXHXjq4wTyMwkpZR9PrYSzLk")
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    audio_file = ""
    if request.method == "POST":
        user_input = request.form.get("query")
        if user_input:
            # Start a chat and send a message
            chat = model.start_chat(history=[])
            response = chat.send_message(user_input)
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