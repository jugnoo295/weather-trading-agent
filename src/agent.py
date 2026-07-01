import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_llm(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    
    models = [
    "cohere/north-mini-code:free",
    "nvidia/nemotron-3-ultra:free",
    "google/gemma-4-31b:free",
]
    
    for model in models:
        for attempt in range(3):
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                data = response.json()
                if "choices" in data:
                    print(f"Success with model: {model}")
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"Model {model} failed: {data.get('error', {}).get('message')}")
                    time.sleep(5)
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(3)
    
    return "All models failed"


def analyze_weather_for_trading(weather_data: list) -> str:
    prompt = f"""
    You are a prediction market trading analyst.
    
    Given this weather data for multiple cities:
    {weather_data}
    
    For each city, analyze:
    1. Current weather conditions
    2. Should we BET YES or NO on "Will it be hot today?" market
    3. Confidence level (0-100%)
    4. Kelly Criterion bet size (bankroll = $1000)
    
    Kelly Formula: f = (bp - q) / b
    where b = odds-1, p = probability of winning, q = 1-p
    
    Return a structured analysis for each city.
    """
    
    return ask_llm(prompt)

if __name__ == "__main__":
    # Test with dummy data first
    test_data = [
        {"city": "London", "temperature": 28, "condition": "clear sky", "humidity": 45},
        {"city": "Tokyo", "temperature": 35, "condition": "hot and sunny", "humidity": 60},
    ]
    
    print("Asking AI to analyze weather for trading...\n")
    result = analyze_weather_for_trading(test_data)
    print(result)
# Agent architecture inspired by Hermes Agent framework
# Tools: weather_tool, analysis_tool
# LLM: OpenRouter (Cohere)
# Flow: fetch → analyze → decide → trade