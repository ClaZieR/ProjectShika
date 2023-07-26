import requests
import pygame
import io
import time
import speech_recognition as sr
import openai

# Initialize OpenAI API key
openai.api_key = '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'

# Initialize Pygame mixer
pygame.mixer.init()

assistant_role = "female assistant"  # Set the role of the assistant

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
        # Convert the response content to audio data
        audio_data = io.BytesIO(response.content)

        print("Text-to-speech conversion successful.")

        sound = pygame.mixer.Sound(audio_data)
        sound.play()

        # Wait for the audio to finish playing
        while pygame.mixer.get_busy():
            time.sleep(0.1)
    else:
        print("Text-to-speech conversion failed. Status Code:", response.status_code)

if __name__ == "__main__":
    print("Listening for commands...")
    while True:
        user_text = convert_speech_to_text()

        # Check if the user wants to stop
        if user_text.lower() == "stop":
            print("Exiting the loop.")
            break

        # Call the OpenAI API and get the response
        response = openai.Completion.create(
            engine="text-davinci-002",  # Replace with the engine you want to use
            prompt=f"{assistant_role}: {user_text}",  # Include the assistant role in the prompt
            max_tokens=100  # Adjust the number of tokens for the response
        )

        if 'choices' in response and len(response['choices']) > 0:
            ai_response = response['choices'][0]['text']
            print("AI Response:", ai_response)

            # Convert AI response to voice and play it
            text_to_voice(ai_response)
        else:
            print("Failed to get AI response.")
