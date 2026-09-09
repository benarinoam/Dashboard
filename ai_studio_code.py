import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📊 Morning Stock Momentum Dashboard")

# --- Tab 1: After-Hours Gainers ---
tab1, tab2 = st.tabs(["🌙 After-Hours Gainers", "🔥 14-Day Streaks"])

with tab1:
    st.header("Stocks Up After-Hours (Yesterday)")
    # Note: For 'all' stocks, a paid API like Polygon or FMP is better.
    # Here we demo with a sample list using yfinance.
    tickers = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "META"] # Replace with full list
    
    after_hours_data = []
    for t in tickers:
        stock = yf.Ticker(t)
        # yfinance can get prepost data using 'download' or 'fast_info'
        fast = stock.fast_info
        close = fast['previousClose']
        current = fast['lastPrice'] 
        change = ((current - close) / close) * 100
        
        if change > 0:
            after_hours_data.append({"Ticker": t, "Growth %": round(change, 2), "Price": round(current, 2)})
    
    st.table(pd.DataFrame(after_hours_data).sort_values(by="Growth %", ascending=False))

# --- Tab 2: 14-Day Streaks ---
with tab2:
    st.header("Top 10 Stocks with Longest Up-Streaks")
    
    def get_streak(ticker):
        hist = yf.download(ticker, period="14d", interval="1d", progress=False)
        hist['Diff'] = hist['Close'].diff()
        # Count consecutive positives
        streak = 0
        for val in reversed(hist['Diff'].values):
            if val > 0: streak += 1
            else: break
        total_growth = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-(streak+1)]) / hist['Close'].iloc[-(streak+1)]) * 100 if streak > 0 else 0
        return streak, round(total_growth, 2)

    streak_results = []
    for t in tickers:
        days, growth = get_streak(t)
        if days > 0:
            streak_results.append({"Ticker": t, "Days in Row": days, "Total Growth %": growth})

    df_streaks = pd.DataFrame(streak_results).sort_values(by=["Days in Row", "Total Growth %"], ascending=False).head(10)
    st.table(df_streaks)