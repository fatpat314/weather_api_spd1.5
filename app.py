from flask import Flask, render_template, request, redirect, url_for
import requests
import pprint
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def space():
    print("---------------------------------------------------------")

@app.route('/')
def index():
    return render_template('index.html')


global city_name
@app.route('/result')
def result():

    pp = pprint.PrettyPrinter(indent=4)
    global city_name
    city_name = request.args.get('city_name')
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=1d09975e1c6267c23a4e02549672280c"
    response = requests.get(weather_url)
    response_json = response.json()
    main_data = response_json["main"]
    weather_data = response_json["weather"]
    wind_data = response_json["wind"]
    temp_in_kelvin = main_data["temp"]
    temp_in_celsius = temp_in_kelvin - 273.15
    temp_in_fahrenheit = temp_in_celsius * 9/5 + 32
    description = weather_data[0]["main"]
    humidity = main_data["humidity"]
    wind_mps = wind_data["speed"]
    wind = wind_mps * 2.23694

    return render_template('result.html', temp = temp_in_fahrenheit, description = description, humidity = humidity, wind = wind)

@app.route("/finished", methods=['GET', 'POST'])
def finished():

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=1d09975e1c6267c23a4e02549672280c"

    response = requests.get(weather_url)
    response_json = response.json()
    comment = request.form['comment']
    weather_data = response_json["weather"]
    description = weather_data[0]["main"]

    return render_template('finished.html', comment = comment, description = description)


if __name__ == "__main__":
    app.run
