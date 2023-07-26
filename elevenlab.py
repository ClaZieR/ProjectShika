import requests
import pygame
import os
import time

def text_to_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        'xi-api-key': '40cf6900c4850ddc885253c6daf970bb',
        'Content-Type': 'application/json',
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Remove existing output.mp3 file
        if os.path.exists("output.mp3"):
            os.remove("output.mp3")

        with open("output.mp3", "wb") as f:
            f.write(response.content)

        print("Text-to-speech conversion successful. Audio saved as 'output.mp3'")

        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        print("Text-to-speech conversion failed. Status Code:", response.status_code)

if __name__ == "__main__":
    text_to_voice("Hello How can I help you?.")

