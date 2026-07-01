import requests

GAMMA_API = "https://gamma-api.polymarket.com"

def get_weather_markets():
    """Fetch active weather markets from Polymarket"""
    try:
        # Get all active events without keyword filter
        response = requests.get(
            f"{GAMMA_API}/events",
            params={
                "active": "true",
                "closed": "false",
                "limit": 100,
            },
            timeout=10
        )
        data = response.json()
        
        weather_keywords = [
            "temperature", "rain", "hot", "cold", "snow", 
            "hurricane", "storm", "celsius", "fahrenheit",
            "precipitation", "forecast", "climate"
        ]
        
        weather_markets = []
        for event in data:
            title = event.get("title", "").lower()
            description = event.get("description", "").lower()
            
            if any(word in title or word in description for word in weather_keywords):
                for market in event.get("markets", []):
                    prices = market.get("outcomePrices", [])
                    weather_markets.append({
                        "event": event.get("title"),
                        "question": market.get("question"),
                        "yes_price": prices[0] if len(prices) > 0 else "N/A",
                        "no_price": prices[1] if len(prices) > 1 else "N/A",
                        "volume": market.get("volume"),
                    })
        
        return weather_markets
        
    except Exception as e:
        print(f"Polymarket API error: {e}")
        return []

if __name__ == "__main__":
    markets = get_weather_markets()
    if markets:
        print(f"Found {len(markets)} weather markets!\n")
        for m in markets[:10]:
            print(f"📊 {m['event']}")
            print(f"   Question: {m['question']}")
            print(f"   YES: {m['yes_price']} | NO: {m['no_price']}")
            print(f"   Volume: {m['volume']}\n")
    else:
        print("No weather markets found currently on Polymarket")