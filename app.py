from flask import Flask, request, jsonify
import requests
from gtts import gTTS
import os
import re
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EDEN_API_KEY = os.getenv("EDEN_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
EDEN_API_URL = os.getenv("EDEN_API_URL")

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()
    student_prompt = data.get('prompt')
    num_images = data.get('numImages', 3)  # Default to 3 if not provided

    # Step 1: Get transcript from Gemini API
    transcript = get_transcript(student_prompt)
    if not transcript:
        return jsonify({'error': 'Failed to generate transcript'}), 500

    # Step 2: Convert transcript to speech with GTTS
    audio_file = 'output.mp3'
    tts = gTTS(text=transcript, lang='en')
    tts.save(audio_file)

    # Step 3: Split transcript into segments based on num_images
    segments = split_transcript(transcript, num_images)

    # Step 4: Generate images for each segment
    image_urls = []
    for segment in segments:
        image_url = generate_image(segment)
        if image_url:
            image_urls.append(image_url)

    if not image_urls:
        return jsonify({'error': 'Failed to generate images'}), 500

    # Clean up audio file (optional, remove if not needed)
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return jsonify({'imageUrls': image_urls})

def get_transcript(prompt):
    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={
                'Authorization': f'Bearer {GEMINI_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={'prompt': prompt}
        )
        response.raise_for_status()
        return response.json().get('transcript')  # Adjust based on actual API response
    except Exception as e:
        print(f'Error with Gemini API: {e}')
        return None

def split_transcript(transcript, num_segments):
    # Split transcript into sentences and group into num_segments
    sentences = re.split(r'(?<=[.!?]) +', transcript)
    segment_size = max(1, len(sentences) // num_segments)
    segments = [' '.join(sentences[i:i + segment_size]) for i in range(0, len(sentences), segment_size)]
    return segments[:num_segments]  # Limit to num_segments

def generate_image(segment):
    try:
        response = requests.post(
            EDEN_API_URL,
            headers={
                'Authorization': f'Bearer {EDEN_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={'prompt': segment}
        )
        response.raise_for_status()
        return response.json().get('imageUrl')  # Adjust based on actual API response
    except Exception as e:
        print(f'Error with Eden API: {e}')
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5500)