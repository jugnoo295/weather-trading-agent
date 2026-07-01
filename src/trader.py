import os
from dotenv import load_dotenv
from weather import get_all_weather
from agent import analyze_weather_for_trading

load_dotenv()

BANKROLL = 1000  # Paper trading bankroll in USD

def run_trading_agent():
    print("=" * 50)
    print("WEATHER TRADING AGENT - PAPER TRADE")
    print("=" * 50)
    
    # Step 1: Fetch weather
    print("\n[1] Fetching weather data...")
    weather_data = get_all_weather()
    
    # Step 2: AI Analysis
    print("\n[2] Asking AI for trading analysis...")
    analysis = analyze_weather_for_trading(weather_data)
    
    # Step 3: Show results
    print("\n[3] TRADING DECISIONS:")
    print("-" * 50)
    print(analysis)
    print("-" * 50)
    print(f"\nBankroll: ${BANKROLL}")
    print("Mode: PAPER TRADE (no real money)")

if __name__ == "__main__":
    run_trading_agent()