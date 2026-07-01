import streamlit as st
import sys
import os
import json
import time
from datetime import datetime
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weather import get_all_weather
from agent import analyze_weather_for_trading

# Page config
st.set_page_config(
    page_title="Weather Trading Agent",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #2d3147; }
    .yes-badge { background-color: #00c853; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    .no-badge { background-color: #d50000; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    .city-card { background-color: #1e2130; padding: 20px; border-radius: 15px; border: 1px solid #2d3147; margin: 10px 0; }
    .header-text { color: #00b4d8; font-size: 14px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; }
    .big-number { font-size: 48px; font-weight: 700; color: white; }
    div[data-testid="stSidebarNav"] { background-color: #1e2130; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/partly-cloudy-day.png", width=80)
    st.title("⚙️ Control Panel")
    st.markdown("---")
    
    bankroll = st.number_input("💰 Bankroll ($)", value=1000, min_value=100, max_value=100000, step=100)
    hot_threshold = st.slider("🌡️ Hot Threshold (°C)", min_value=20, max_value=40, value=25)
    auto_refresh = st.toggle("🔄 Auto Refresh (5 min)", value=False)
    
    st.markdown("---")
    st.markdown("**📊 Mode:** Paper Trade")
    st.markdown("**🌍 Cities:** 5")
    st.markdown("**🤖 Model:** Cohere Free")
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("# 🌤️ Weather Trading Agent")
    st.caption("AI-powered Polymarket prediction market trader | Paper Trade Mode")
with col2:
    st.metric("💰 Bankroll", f"${bankroll:,}")
with col3:
    st.metric("🏙️ Markets", "5 Cities")

st.markdown("---")

# Initialize session state for history
if "trade_history" not in st.session_state:
    st.session_state.trade_history = []

# Run button
run_col, status_col = st.columns([1, 3])
with run_col:
    run_button = st.button("🚀 Run Trading Agent", type="primary", use_container_width=True)

if run_button:
    # Progress bar
    progress = st.progress(0, text="Starting agent...")
    
    # Step 1: Weather
    progress.progress(20, text="🌍 Fetching live weather data...")
    weather_data = get_all_weather()
    time.sleep(0.5)
    
    # Step 2: AI Analysis
    progress.progress(60, text="🤖 AI analyzing markets...")
    analysis = analyze_weather_for_trading(weather_data)
    time.sleep(0.5)
    
    progress.progress(100, text="✅ Done!")
    time.sleep(0.5)
    progress.empty()

    st.success(f"✅ Analysis complete at {datetime.now().strftime('%H:%M:%S')}")

    # ---- WEATHER CARDS ----
    st.markdown("## 🌍 Live Weather Data")
    
    weather_icons = {
        "clear sky": "☀️",
        "few clouds": "🌤️",
        "scattered clouds": "⛅",
        "broken clouds": "🌥️",
        "overcast clouds": "☁️",
        "light rain": "🌦️",
        "moderate rain": "🌧️",
        "heavy intensity rain": "⛈️",
        "thunderstorm": "⛈️",
        "snow": "❄️",
        "mist": "🌫️",
    }

    cols = st.columns(5)
    for i, w in enumerate(weather_data):
        with cols[i]:
            icon = weather_icons.get(w.get("condition", ""), "🌡️")
            temp = w.get("temperature", 0)
            feels = w.get("feels_like", temp)
            is_hot = feels > hot_threshold
            
            border_color = "#ff6b6b" if is_hot else "#00b4d8"
            
            st.markdown(f"""
            <div style="background:#1e2130; padding:20px; border-radius:15px; 
                        border: 2px solid {border_color}; text-align:center; margin-bottom:10px;">
                <div style="font-size:40px">{icon}</div>
                <div style="font-size:13px; color:#888; font-weight:600; letter-spacing:1px">{w['city'].upper()}</div>
                <div style="font-size:36px; font-weight:700; color:white">{temp}°C</div>
                <div style="font-size:12px; color:#aaa">Feels like {feels}°C</div>
                <div style="font-size:12px; color:#aaa; margin-top:5px">{w.get('condition','').title()}</div>
                <div style="margin-top:10px; font-size:12px; color:#888">
                    💧 {w.get('humidity','N/A')}% &nbsp; 💨 {w.get('wind_speed','N/A')} m/s
                </div>
                <div style="margin-top:10px">
                    <span style="background:{'#ff6b6b' if is_hot else '#00b4d8'}; color:white; 
                                 padding:3px 12px; border-radius:20px; font-size:12px; font-weight:bold">
                        {'🔥 HOT' if is_hot else '❄️ COOL'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ---- TEMPERATURE CHART ----
    st.markdown("## 📊 Temperature Comparison")
    
    chart_data = pd.DataFrame({
        "City": [w["city"] for w in weather_data],
        "Temperature (°C)": [w.get("temperature", 0) for w in weather_data],
        "Feels Like (°C)": [w.get("feel_like", w.get("temperature", 0)) for w in weather_data],
    })
    
    st.bar_chart(chart_data.set_index("City"))

    # ---- AI ANALYSIS ----
    st.markdown("## 🤖 AI Trading Analysis")
    with st.expander("View Full AI Analysis", expanded=True):
        st.markdown(analysis)

    # ---- TRADE HISTORY ----
    trade_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "cities": len(weather_data),
        "bankroll": f"${bankroll:,}",
        "hottest_city": max(weather_data, key=lambda x: x.get("temperature", 0))["city"],
        "max_temp": max(weather_data, key=lambda x: x.get("temperature", 0)).get("temperature", 0),
    }
    st.session_state.trade_history.append(trade_entry)

    # ---- SUMMARY ----
    st.markdown("## 💰 Trade Summary")
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    with sum_col1:
        st.metric("Bankroll", f"${bankroll:,}")
    with sum_col2:
        st.metric("Cities Analyzed", len(weather_data))
    with sum_col3:
        hottest = max(weather_data, key=lambda x: x.get("temperature", 0))
        st.metric("Hottest City", hottest["city"], f"{hottest.get('temperature')}°C")
    with sum_col4:
        hot_count = sum(1 for w in weather_data if w.get("feels_like", 0) > hot_threshold)
        st.metric("YES Markets", f"{hot_count}/5")

    # ---- PRIOR PREDICTIONS ----
    if len(st.session_state.trade_history) > 1:
        st.markdown("## 📈 Prior Predictions")
        history_df = pd.DataFrame(st.session_state.trade_history)
        st.dataframe(history_df, use_container_width=True)

else:
    # Landing state
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:80px">🌤️</div>
        <h2 style="color:white">Weather Trading Agent Ready</h2>
        <p style="color:#888; font-size:16px">
            Click <b>Run Trading Agent</b> to fetch live weather data and get AI-powered 
            trading signals for Polymarket weather markets across 5 global cities.
        </p>
        <br>
        <p style="color:#555">
            📍 London &nbsp;|&nbsp; 🗽 New York &nbsp;|&nbsp; 🗼 Tokyo &nbsp;|&nbsp; 🦘 Sydney &nbsp;|&nbsp; 🇮🇳 Mumbai
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show empty metrics
    st.markdown("### 📊 What you'll see after running:")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("🌡️ Live temperatures for 5 cities")
    with c2:
        st.info("🤖 AI YES/NO trading signals")
    with c3:
        st.info("📊 Kelly Criterion bet sizes")
    with c4:
        st.info("📈 Trade history tracking")