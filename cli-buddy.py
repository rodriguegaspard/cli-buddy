import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def help():
    print("""
CLI-BUDDY COMMANDS
------------------
    :h = Shows commands
    :q = Closes the application
          """)

def quit():
    raise SystemExit

commands = {":h" : help,
            ":q" : quit
            }

print("Welcome to cli-buddy! :h for a list of useful commands.")
while True:
    user_input = input('> ')
    if user_input in commands.keys():
        commands[user_input]()
    else:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_input}])
        ai_response = chat_completion['choices'][0]['message']['content']
        print(ai_response)
