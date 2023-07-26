import speech_recognition as sr
import openai

# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
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
    else:
        print("Failed to get AI response.")
