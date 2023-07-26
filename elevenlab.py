
import openai
assistant_role="User"

openai.api_key = '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'
chat_history=[]
while True:
    user_text = input("User:")
    prompt = f"{chat_history} {assistant_role}:{user_text}AI:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with the engine you want to use
        prompt=prompt,
        max_tokens=100 , # Adjust the number of tokens for the response
        stop=[f"{assistant_role}:","AI:"]
    )

    print(response)
    ai_response = response['choices'][0]['text'].replace("\n", "")

    chat_history.append(f"{assistant_role}: {user_text}")
    chat_history.append(f"Assistant:{ai_response}")
    print("Chat History:", chat_history)