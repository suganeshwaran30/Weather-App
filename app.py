# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Get your API key from https://openweathermap.org/
API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use 'imperial' for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': data['message']}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)