import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import time

# Page Configuration
st.set_page_config(page_title="CryptoScalp: Momentum Scanner", layout="wide")

# Custom CSS for Trading Terminal Look
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    h1 { color: #00FFA3; font-family: 'JetBrains Mono', monospace; }
    .metric-container { border: 1px solid #333; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("⚡ CryptoScalp: Algorithmic Scalping Tool")
st.markdown("""
This tool utilizes **Mean Reversion Strategy** combined with **Momentum Indicators** to identify potential 
scalping opportunities in real-time. It detects price anomalies using Bollinger Bands and RSI divergence.
""")

# Sidebar Controls
st.sidebar.header("Strategy Parameters")
ticker = st.sidebar.text_input("Asset Ticker", value="BTC-USD")
interval = st.sidebar.selectbox("Time Interval", ["1m", "5m", "15m", "1h"], index=2)
period = st.sidebar.selectbox("Lookback Period", ["1d", "5d", "1mo"], index=1)

st.sidebar.divider()
st.sidebar.subheader("Signal Sensitivity")
rsi_upper = st.sidebar.slider("Overbought Threshold (RSI)", 70, 90, 75)
rsi_lower = st.sidebar.slider("Oversold Threshold (RSI)", 10, 30, 25)

def fetch_data(symbol, interval, period):
    """Fetches real-time crypto data."""
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def apply_strategy(df):
    """Calculates technical indicators."""
    # RSI
    df['RSI'] = df.ta.rsi(length=14)
    
    # Bollinger Bands
    bbands = df.ta.bbands(length=20, std=2)
    df = pd.concat([df, bbands], axis=1)
    
    # Rename columns for clarity (pandas_ta naming convention varies)
    df.rename(columns={
        'BBL_20_2.0': 'BB_Lower',
        'BBM_20_2.0': 'BB_Middle',
        'BBU_20_2.0': 'BB_Upper'
    }, inplace=True)

    return df

def generate_signals(df):
    """Generates Buy/Sell signals based on strategy logic."""
    buy_signals = []
    sell_signals = []
    
    for i in range(len(df)):
        # Scalping Logic:
        # BUY if Price touches Lower Band AND RSI is Oversold
        if df['Close'].iloc[i] < df['BB_Lower'].iloc[i] and df['RSI'].iloc[i] < rsi_lower:
            buy_signals.append(df['Close'].iloc[i])
            sell_signals.append(None)
        
        # SELL if Price touches Upper Band AND RSI is Overbought
        elif df['Close'].iloc[i] > df['BB_Upper'].iloc[i] and df['RSI'].iloc[i] > rsi_upper:
            sell_signals.append(df['Close'].iloc[i])
            buy_signals.append(None)
        
        else:
            buy_signals.append(None)
            sell_signals.append(None)
            
    df['Buy_Signal'] = buy_signals
    df['Sell_Signal'] = sell_signals
    return df

# Main Execution
if st.sidebar.button("Scan Market"):
    with st.spinner(f"Analyzing {ticker} market data..."):
        df = fetch_data(ticker, interval, period)
        
        if df is not None and not df.empty:
            df = apply_strategy(df)
            df = generate_signals(df)
            
            # --- Metrics Dashboard ---
            last_close = df['Close'].iloc[-1]
            last_rsi = df['RSI'].iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${last_close:,.2f}")
            col2.metric("RSI (14)", f"{last_rsi:.2f}", delta_color="inverse")
            
            # Signal Status
            status = "NEUTRAL"
            if last_rsi > rsi_upper: status = "OVERBOUGHT (Sell Zone)"
            elif last_rsi < rsi_lower: status = "OVERSOLD (Buy Zone)"
            
            col3.metric("Market Condition", status)
            col4.metric("Volatility (BB Width)", f"{(df['BB_Upper'].iloc[-1] - df['BB_Lower'].iloc[-1]):.2f}")

            # --- Advanced Charting ---
            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'],
                name='Price Action'))

            # Bollinger Bands
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='gray', width=1), name='Upper BB'))
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='gray', width=1), name='Lower BB', fill='tonexty', fillcolor='rgba(128,128,128,0.1)'))

            # Signals
            fig.add_trace(go.Scatter(x=df.index, y=df['Buy_Signal'], mode='markers', 
                                     marker=dict(symbol='triangle-up', size=12, color='#00FFA3'), name='Buy Signal'))
            fig.add_trace(go.Scatter(x=df.index, y=df['Sell_Signal'], mode='markers', 
                                     marker=dict(symbol='triangle-down', size=12, color='#FF4B4B'), name='Sell Signal'))

            fig.update_layout(
                title=f"{ticker} Scalping Chart ({interval})",
                height=600,
                xaxis_rangeslider_visible=False,
                template="plotly_dark",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117"
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- Data & Logic Explanation ---
            with st.expander("See Underlying Data & Logic"):
                st.dataframe(df.tail(10))
                st.info("""
                **Algorithm Logic:**
                1. **Mean Reversion:** Prices tend to return to the average over time.
                2. **Entry Condition:** Price dips below Lower Bollinger Band + RSI < 30 (Panic Selling).
                3. **Exit Condition:** Price spikes above Upper Bollinger Band + RSI > 70 (FOMO Buying).
                """)
        else:
            st.error("Data not found. Please verify the ticker symbol.")

else:
    st.info("Select parameters and click 'Scan Market' to start.")
