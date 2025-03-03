from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import base64
import os

app = FastAPI()

# Sarvam API details
SARVAM_API_URL = "https://api.sarvam.ai/text-to-speech"
HEADERS = {
    "API-Subscription-Key": os.getenv("SARVAM_API_KEY"),  # Use environment variable
    "Content-Type": "application/json"
}

# Function to convert text to speech
def text_to_speech(text: str, target_language="hi-IN", speaker="meera", sample_rate=8000, model="bulbul:v1"):
    payload = {
        "inputs": [text],
        "target_language_code": target_language,
        "speaker": speaker,
        "speech_sample_rate": sample_rate,
        "enable_preprocessing": True,
        "model": model
    }
    response = requests.post(SARVAM_API_URL, json=payload, headers=HEADERS)

    if response.status_code == 200:
        response_json = response.json()
        audio_base64 = response_json["audios"][0]
        audio_bytes = base64.b64decode(audio_base64)
        output_filename = "output_audio.wav"

        with open(output_filename, "wb") as audio_file:
            audio_file.write(audio_bytes)

        return output_filename
    else:
        return None

# FastAPI endpoint
@app.post("/generate-audio")
async def generate_audio(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text input is required")
    
    output_file = text_to_speech(text)
    if output_file:
        return FileResponse(output_file, media_type="audio/wav", filename="output_audio.wav")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio")

# Run the server (Render uses this)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
