import requests

# Define API URL (Replace with your Render deployment URL)
url = "https://sarvam-tts.onrender.com:10000/generate-audio"

# Define request headers
headers = {
    "Content-Type": "application/json"
}

# Define request payload
payload = {
    "text": "Namaste! Kaise ho aap?"
}

# Send POST request
response = requests.post(url, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    # Save the audio file
    with open("output_audio.wav", "wb") as f:
        f.write(response.content)
    print("✅ Audio file saved as output_audio.wav")
else:
    print("❌ Error:", response.status_code, response.text)
