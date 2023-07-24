import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello World!"}])
ai_response = chat_completion['choices'][0]['message']['content']
print("OpenAI says :\n" + ai_response)
