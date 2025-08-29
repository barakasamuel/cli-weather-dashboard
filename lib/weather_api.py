import requests

API_KEY = "1c08d25f857f7892f6a28b5bca665385"
BASE_URL = "http://api.openweathermap.org/data/2.5"

def get_current_weather(city, unit='C'):
    """Fetch current weather for a city"""
    try:
        units = 'metric' if unit == 'C' else 'imperial'
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={units}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 404:
            return {"error": "City not found"}
        if response.status_code != 200:
            return {"error": "Weather service unavailable"}
            
        data = response.json()
        return {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "condition": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "feels_like": round(data["main"]["feels_like"]),
            "unit": "°C" if unit == 'C' else "°F"
        }
    except:
        return {"error": "Failed to fetch weather"}

def get_forecast(city, unit='C'):
    """Fetch 5-day forecast for a city"""
    try:
        units = 'metric' if unit == 'C' else 'imperial'
        url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={units}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 404:
            return {"error": "City not found"}
        if response.status_code != 200:
            return {"error": "Weather service unavailable"}
            
        data = response.json()
        forecasts = []
        
        for i in range(0, min(40, len(data["list"])), 8):
            item = data["list"][i]
            forecasts.append({
                "date": item["dt_txt"][:10],
                "temperature": round(item["main"]["temp"]),
                "condition": item["weather"][0]["description"].title(),
                "unit": "°C" if unit == 'C' else "°F"
            })
        
        return {"city": data["city"]["name"], "forecasts": forecasts}
    except:
        return {"error": "Failed to fetch forecast"}

def format_weather(weather_data):
    """Format weather data for display"""
    if "error" in weather_data:
        return f"❌ {weather_data['error']}"
    
    icons = {"clear": "☀️", "sun": "☀️", "rain": "🌧️", "cloud": "☁️", "snow": "❄️"}
    icon = "🌤️"
    for key, emoji in icons.items():
        if key in weather_data["condition"].lower():
            icon = emoji
            break
    
    return f"""
{icon} {weather_data['city']}
Temperature: {weather_data['temperature']}{weather_data['unit']} (feels like {weather_data['feels_like']}{weather_data['unit']})
Condition: {weather_data['condition']}
Humidity: {weather_data['humidity']}%
Wind: {weather_data['wind_speed']} m/s
"""

def format_forecast(forecast_data):
    """Format forecast data for display"""
    if "error" in forecast_data:
        return f"❌ {forecast_data['error']}"
    
    result = f"\n📅 5-Day Forecast for {forecast_data['city']}\n"
    for day in forecast_data["forecasts"]:
        result += f"{day['date']}: {day['temperature']}{day['unit']} - {day['condition']}\n"
    
    return result