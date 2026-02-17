import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("📈 Smart Stock Analyzer")

uploaded = st.file_uploader("Upload Kaggle Stock CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)

    st.success("Dataset Loaded")

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")

    st.subheader("Dataset Preview")
    st.dataframe(df.tail())

    # Moving Average
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df['RSI'] = 100 - (100/(1+rs))

    latest = df.iloc[-1]

    close = latest['Close']
    ma20 = latest['MA20']
    ma50 = latest['MA50']
    rsi = latest['RSI']

    # Recommendation Logic
    if close > ma20 and rsi < 70:
        signal = "🟢 BUY"
    elif rsi > 70:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"

    st.header(f"Recommendation: {signal}")

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Close", round(close,2))
    col2.metric("MA20", round(ma20,2))
    col3.metric("MA50", round(ma50,2))
    col4.metric("RSI", round(rsi,2))

    # Price Chart
    fig1 = plt.figure()
    plt.plot(df['Date'], df['Close'], label="Close")
    plt.plot(df['Date'], df['MA20'], label="MA20")
    plt.plot(df['Date'], df['MA50'], label="MA50")
    plt.legend()
    st.pyplot(fig1)

    # RSI Chart
    fig2 = plt.figure()
    plt.plot(df['Date'], df['RSI'])
    plt.axhline(70)
    plt.axhline(30)
    st.pyplot(fig2)

    st.info("RSI > 70 = Overbought | RSI < 30 = Oversold")

else:
    st.info("Upload CSV to begin")
