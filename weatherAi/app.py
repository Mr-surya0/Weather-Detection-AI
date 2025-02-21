from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Replace with your OpenWeatherMap API key
API_KEY = 'e981d0821ac0edfba78a418e530ea38a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'

def get_weather_data(city, api_key, forecast=False):
    url = FORECAST_URL if forecast else BASE_URL
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')  # Serve the frontend

@app.route('/weather', methods=['POST'])
def weather():
    data = request.json
    intent = data.get('intent')
    city = data.get('city')

    if not city:
        return jsonify({'error': 'City not provided'}), 400

    if intent == 'GetCurrentWeather':
        weather_data = get_weather_data(city, API_KEY)
        if weather_data.get('cod') != 200:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
        current_weather = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        response = {
            'city': city,
            'current_weather': current_weather,
            'temperature': f'{temperature}°C'
        }
        return jsonify(response)

    elif intent == 'GetWeatherForecast':
        forecast_data = get_weather_data(city, API_KEY, forecast=True)
        if forecast_data.get('cod') != '200':
            return jsonify({'error': 'Failed to fetch forecast data'}), 500
        forecast_list = forecast_data['list'][:5]  # Get the first 5 forecasts
        forecasts = []
        for item in forecast_list:
            forecasts.append({
                'datetime': item['dt_txt'],
                'weather': item['weather'][0]['description'],
                'temperature': f"{item['main']['temp']}°C"
            })
        response = {
            'city': city,
            'forecasts': forecasts
        }
        return jsonify(response)

    else:
        return jsonify({'error': 'Unknown intent'}), 400

if __name__ == '__main__':
    app.run(debug=True)
