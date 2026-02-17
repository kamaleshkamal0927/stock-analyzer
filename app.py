import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Analyzer", layout="wide")

st.title("📈 Stock Analyzer – Buy / Sell / Hold")

uploaded_file = st.file_uploader("Upload your Stock CSV (Kaggle)", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    st.success("Dataset Loaded!")

    st.subheader("Dataset Preview")
    st.dataframe(df.tail())

    # ===== Moving Averages =====
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    # ===== RSI =====
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # ===== Signal Logic =====
    latest_close = df['Close'].iloc[-1]
    ma20 = df['MA20'].iloc[-1]
    rsi = df['RSI'].iloc[-1]

    if latest_close > ma20 and rsi < 70:
        signal = "🟢 BUY"
    elif rsi > 70:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"

    st.subheader("📊 Recommendation")
    st.markdown(f"## {signal}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Close", round(latest_close,2))
    col2.metric("MA20", round(ma20,2))
    col3.metric("RSI", round(rsi,2))

    # ===== Price Chart =====
    st.subheader("Price + Moving Average")

    fig1 = plt.figure()
    plt.plot(df['Date'], df['Close'], label="Close Price")
    plt.plot(df['Date'], df['MA20'], label="MA20")
    plt.plot(df['Date'], df['MA50'], label="MA50")
    plt.legend()
    st.pyplot(fig1)

    # ===== RSI Chart =====
    st.subheader("RSI Indicator")

    fig2 = plt.figure()
    plt.plot(
