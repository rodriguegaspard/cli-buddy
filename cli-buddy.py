import os
import openai
import time
import requests
from datetime import datetime
from termcolor import colored, cprint
from forex_python.converter import CurrencyRates, CurrencyCodes

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
    :wf = Get 3-day weather forecast
    :astro = Get 3-day astronomical forecast
    :forex : Converts an amount in a particular currency into another, using latest currency rates
    :say = Talk to ChatGPT
    :q = Closes the application
          """)

def currentWeather():
    city = input("City of location: ")
    r = requests.get('http://api.weatherapi.com/v1/current.json?key={0}&q={1}'.format(weather_api_key, city))
    result = r.json()
    cprint("\nCurrent weather in {0}, {1}, {2} (Last updated: {3}):".format(result["location"]["name"], result["location"]["region"], result["location"]["country"], getDatetime(result["current"]["last_updated"])), "light_yellow", attrs=["bold", "underline"])
    print("Condition: {0}".format(result["current"]["condition"]["text"]))
    print("Cloud coverage: {0:3}%, Visibility: {1:2} km".format(result["current"]["cloud"], result["current"]["vis_km"]))
    print("Temperature: {0:5}°C (Feels like {1:5}°C)".format(result["current"]["temp_c"], result["current"]["feelslike_c"]))
    print("Windspeed: {0:5} km/h, {1:3}° {2:3}".format(result["current"]["wind_kph"], result["current"]["wind_degree"], result["current"]["wind_dir"]))
    print("Air pressure: {0:6} mb, Humidity: {1:3}%".format(result["current"]["pressure_mb"], result["current"]["humidity"]))
    if result["current"]["precip_mm"]:
        print("Precipitation: {} mm".format(result["current"]["precip_mm"]))

def weatherForecast():
    city = input("City or location: ")
    r = requests.get('http://api.weatherapi.com/v1/forecast.json?key={0}&q={1}&days=3'.format(weather_api_key, city))
    result = r.json()
    cprint("\nWeather forecast in {0}, {1}, {2} (Last updated: {3}):".format(result["location"]["name"], result["location"]["region"], result["location"]["country"], result["current"]["last_updated"]), "light_yellow" , attrs=["bold", "underline"])
    for day in result["forecast"]["forecastday"]:
        cprint("\n{0} (min: {1:5}°C  max: {2:5}°C, avg: {3:5}°C) Wind: {4:5} km/h, Humidity: {5:.0f}%".format(colored(datetime.fromisoformat(day["date"]).date(), "yellow", attrs=["underline"]), day["day"]["mintemp_c"], day["day"]["maxtemp_c"], day["day"]["avgtemp_c"], day["day"]["maxwind_kph"], day["day"]["avghumidity"]), "white", attrs=["bold"], end='')
        if day["day"]["daily_will_it_snow"]:
            cprint(", Snow: {0}% (~{1} cm)".format(day["day"]["daily_chance_of_snow"], day["day"]["totalsnow_cm"]), "white", attrs=["bold"], end='')
        if day["day"]["daily_will_it_rain"]:
            cprint(", Rain: {0}% (~{1} mm)".format(day["day"]["daily_chance_of_rain"], day["day"]["totalprecip_mm"]), "white", attrs=["bold"], end='')
        print("")
        for forecast_hour in (hour for hour in day["hour"] if day["hour"].index(hour)%2 == 0):
            print("{0:2d}h : {1:30} ({2:5}°C, Humidity: {3:3}%, Clouds: {4:3}%, Wind: {5:5} km/h)".format(datetime.fromisoformat(forecast_hour["time"]).time().hour, forecast_hour["condition"]["text"], forecast_hour["temp_c"], forecast_hour["humidity"], forecast_hour["cloud"], forecast_hour["wind_kph"]), end='')
            if forecast_hour["will_it_snow"]:
                print(" - Snow: {0:3}%".format(forecast_hour["chance_of_snow"]), end='')
            if forecast_hour["will_it_rain"]:
                print(" - Rain: {0:3}% ({1:5} mm)".format(forecast_hour["chance_of_rain"], forecast_hour["precip_mm"]), end='')
            print("")

def astroForecast():
    city = input("City or location: ")
    r = requests.get('http://api.weatherapi.com/v1/forecast.json?key={0}&q={1}&days=3'.format(weather_api_key, city))
    result = r.json()
    cprint("Astronomical forecast in {0}, {1}, {2} (Last updated: {3})".format(result["location"]["name"], result["location"]["region"], result["location"]["country"], result["current"]["last_updated"]), "light_cyan", attrs=["bold", "underline"])
    for day in result["forecast"]["forecastday"]:
        print("\n{0} - (Sun: {1:7} -> {2:7}, Moon: {3:7} -> {4:7}) - {5:15} ({6:3}% illumination)".format(colored(day["date"],"light_cyan", attrs=["underline"]), day["astro"]["sunrise"], day["astro"]["sunset"], day["astro"]["moonrise"], day["astro"]["moonset"], day["astro"]["moon_phase"], day["astro"]["moon_illumination"]))
        for astro_hour in (hour for hour in day["hour"] if day["hour"].index(hour)%2==0):
            print("{0:2}h - {1:30} (Visibility: {2:4} km, Cloud coverage: {3:3}%)".format(datetime.fromisoformat(astro_hour["time"]).time().hour, astro_hour["condition"]["text"], astro_hour["vis_km"], astro_hour["cloud"]))

def convertCurrency():
    rates = CurrencyRates()
    codes = CurrencyCodes()
    amount = float(input("Enter the amount: "))
    starting_currency = input("Enter the currency for the amount entered: ")
    desired_currency = input("Enter the desired currency: ")
    print("{0} {1} ({2}) is currently {3} {4} ({5})".format(amount, codes.get_symbol(starting_currency), codes.get_currency_name(starting_currency), rates.convert(starting_currency, desired_currency, amount), codes.get_symbol(desired_currency), codes.get_currency_name(desired_currency)))

def AIQuery():
    print("Enter or paste your query. Ctrl-D or Ctrl-Z (Windows) to send it.\n> ", end='')
    prompt = []
    while True:
        try:
            line = input()
        except EOFError:
            print("\n> ", end='')
            break
        prompt.append(line)
    query = '\n'.join(prompt)
    if not query:
        print("Query is empty!")
    else:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        ai_response = chat_completion['choices'][0]['message']['content']
        printResponse(ai_response)

def quit():
    raise SystemExit

commands = {":h" : help,
            ":w" : currentWeather,
            ":wf" : weatherForecast,
            ":astro" : astroForecast,
            ":forex" : convertCurrency,
            ":say": AIQuery,
            ":q" : quit,
            }

cprint("Welcome to cli-buddy! :h for a list of useful commands.", "white", attrs=["bold"])
while True:
    user_input = input('\n> ')
    print()
    if user_input in commands.keys():
        commands[user_input]()
    else:
        print("Wrong command. Type :h for a list of all commands.")

