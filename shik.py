import requests
import pygame
import io
import time
import speech_recognition as sr
import openai
import apikeys2py

# Initialize OpenAI API key
openai.api_key = apikeys2py.openAI_API_KEY
# Initialize Pygame mixer
pygame.mixer.init()

# Set the role of the assistant
assistant_role = "User"

# List to store the chat history
chat_history = []

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
        'xi-api-key': apikeys2py.xi_api_key,
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

        # Combine the chat history and current input
        prompt = f"{chat_history} {assistant_role}:{user_text}AI:"
        response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with the engine you want to use
        prompt=prompt,
        max_tokens=100 , # Adjust the number of tokens for the response
        stop=[f"{assistant_role}:","AI:"]  # Adjust the number of tokens for the response
        )

        if 'choices' in response and len(response['choices']) > 0:
            ai_response = response['choices'][0]['text']
            print("AI Response:", ai_response)

            # Convert AI response to voice and play it
            text_to_voice(ai_response)

            # Add the user input and AI response to the chat history
            chat_history.append(f"{assistant_role}: {user_text}")
            chat_history.append(f"Assistant:{ai_response}")
            print("Chat History:", chat_history)

        else:
            print("Failed to get AI response.")
