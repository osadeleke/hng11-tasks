#!/usr/bin/python3
"""
Flask app to return user ip, location and weather
"""
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
OPENWEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Returns a JSON response with the client's IP address,
    location, and weather information,
    along with a personalized greeting.

    URL:
        /api/hello

    Method:
        GET

    Parameters:
        visitor_name (string, required):
        The name of the visitor. This is passed as a query parameter.

    Headers:
        X-Forwarded-For (string, optional):
        The client's IP address, typically set by a reverse proxy
        or load balancer. If not provided,
        the server's IP address will be used.

    Response:
        JSON object with the following fields:
            - client_ip (string):
            The IP address of the client making the request.

            - location (string):
            The city where the client is located, based on the IP address.

            - greeting (string):
            A personalized greeting message that includes the visitor's name
            and the current temperature in their city.

    Example Request:
        GET /api/hello?visitor_name=JohnDoe
    """
    visitor = request.args.get('visitor_name').strip('"')
    # client_ip = request.headers.getlist("X-Forwarded-For")[0]
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    response = requests.get(f'http://ip-api.com/json/{client_ip}')
    location_data = response.json()
    city = location_data.get('city')

    if city != None:
        weather = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather',
            params={'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'metric'}
        )
        weather_data = weather.json()
        temperature = weather_data['main']['temp']
    else:
        city = 'Unknown'
        temperature = 'Unknown'

    greet1 = f'Hello, {visitor}!, the temperature '
    greet2 = f'is {temperature} degrees Celsius in {city}'
    greeting = greet1 + greet2

    return jsonify({
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting
    })


if __name__ == "__main__":
    app.run()
