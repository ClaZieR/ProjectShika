import requests
import pygame
import os
import time
import speech_recognition as sr
import openai

# Initialize OpenAI API key
openai.api_key = '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'

def convert_speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error during speech recognition: {e}")
    except Exception as e:
        print(f"Error: {e}")

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
    user_text = convert_speech_to_text()

    # Call the OpenAI API and get the response
    response = openai.Completion.create(
        engine="text-davinci-002",  # Replace with the engine you want to use
        prompt=user_text,
        max_tokens=100  # Adjust the number of tokens for the response
    )

    if 'choices' in response and len(response['choices']) > 0:
        ai_response = response['choices'][0]['text']
        print("AI Response:", ai_response)

        # Convert AI response to voice
        text_to_voice(ai_response)
    else:
        print("Failed to get AI response.")
