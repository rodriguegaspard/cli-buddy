import os
import openai
import textwrap
import time

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def print_response(text):
    for line in text:
        for char in line:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()
    print()

def help():
    print("""CLI-BUDDY COMMANDS
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
    print()
    if user_input in commands.keys():
        commands[user_input]()
    else:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_input}])
        ai_response = chat_completion['choices'][0]['message']['content']
        formatted_response = textwrap.wrap(ai_response, 100)
        print_response(formatted_response)
