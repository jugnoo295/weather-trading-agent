import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = [
    "London",
    "New York",
    "Tokyo",
    "Sydney",
    "Mumbai"
]

def get_weather(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "city": city,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
            }
        else:
            print(f"API Error for {city}: {data.get('message')}")
            
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")
    
    return {"city": city, "error": "Failed to fetch"}

def get_all_weather() -> list:
    results = []
    for city in CITIES:
        weather = get_weather(city)
        results.append(weather)
        print(f"Fetched: {weather}")
    return results

if __name__ == "__main__":
    data = get_all_weather()
    print("\nAll Weather Data:")
    for d in data:
        print(d)