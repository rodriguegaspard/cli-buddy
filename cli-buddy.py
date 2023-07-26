import os
import openai
import textwrap
import time
import requests
from datetime import datetime

# Load your API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

def getDatetime(date_string):
    # Left-zero padding for the local time, to render it ISO-8601 compatible
    if len(date_string) < 16:
        return datetime.fromisoformat(date_string[:11] + '0' + date_string[11:])
    else:
        return datetime.fromisoformat(date_string)

def printResponse(text):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()

# Commands

def help():
    print("""CLI-BUDDY COMMANDS
------------------
    :h = Shows commands
    :w = Get current weather
    :q = Closes the application
          """)

def currentWeather():
    city = input("City of location: ")
    r = requests.get('http://api.weatherapi.com/v1/current.json?key={0}&q={1}'.format(weather_api_key, city))
    result = r.json()
    print("Current weather in {0}, {1}, {2} ({3}):".format(result["location"]["name"], result["location"]["region"], result["location"]["country"], getDatetime(result["location"]["localtime"])))
    print("Condition: {0}. (Cloud coverage: {1}%, Visibility: {2} km)".format(result["current"]["condition"]["text"], result["current"]["cloud"], result["current"]["vis_km"]))
    print("Temperature: {0}°C (Feels like {1}°C)".format(result["current"]["temp_c"], result["current"]["feelslike_c"]))
    print("Windspeed: {0} km/h, {1}° {2}".format(result["current"]["wind_kph"], result["current"]["wind_degree"], result["current"]["wind_dir"]))
    print("Air pressure: {0} mb, Humidity: {1}%, Precipitation: {2} mm".format(result["current"]["pressure_mb"], result["current"]["humidity"], result["current"]["precip_mm"]))

def weatherForecast():
    city = input("City or location: ")
    r = requests.get('http://api.weatherapi.com/v1/forecast.json?key={0}&q={1}&days=3'.format(weather_api_key, city))
    result = r.json()
    print("Weather forecast in {0}, {1}, {2} ({3}):".format(result["location"]["name"], result["location"]["region"], result["location"]["country"], result["location"]["localtime"], getDatetime(result["location"]["localtime"])))
    #for day in result["forecast"]["forecastday"]:
    #   for hour in day["hour"]:

def quit():
    raise SystemExit

commands = {":h" : help,
            ":w" : currentWeather,
            ":wf" : weatherForecast,
            ":q" : quit,
            }

print("Welcome to cli-buddy! :h for a list of useful commands.")
while True:
    user_input = input('\n> ')
    print()
    if user_input in commands.keys():
        commands[user_input]()
    else:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_input}])
        ai_response = chat_completion['choices'][0]['message']['content']
        formatted_response = textwrap.fill(ai_response, 100)
        printResponse(formatted_response)
