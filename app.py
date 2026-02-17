import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(layout="wide")

st.title("📈 Smart Stock Analyzer Pro")

uploaded = st.file_uploader("Upload Stock CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)
    st.write("Columns detected:", df.columns)

    # ---- AUTO DETECT MODE ----
    if 'Symbol' in df.columns:
        symbols = df['Symbol'].unique()
        stock = st.sidebar.selectbox("Select Stock", symbols)
        data = df[df['Symbol']==stock]
    else:
        st.warning("Single stock dataset detected")
        stock = "Uploaded Stock"
        data = df

    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values("Date")

    # Indicators
    data['MA20'] = data['Close'].rolling(20).mean()

    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean()/loss.rolling(14).mean()
    data['RSI'] = 100-(100/(1+rs))

    latest = data.iloc[-1]
    close = latest['Close']
    rsi = latest['RSI']
    ma20 = latest['MA20']

    if close > ma20 and rsi < 70:
        signal = "🟢 BUY"
    elif rsi > 70:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"

    st.subheader(f"{stock} → {signal}")

    col1,col2,col3 = st.columns(3)
    col1.metric("Close",round(close,2))
    col2.metric("MA20",round(ma20,2))
    col3.metric("RSI",round(rsi,2))

    # Minimal Charts
    fig = plt.figure(figsize=(6,3))
    plt.plot(data['Date'],data['Close'],linewidth=1)
    plt.plot(data['Date'],data['MA20'],linewidth=1)
    st.pyplot(fig)

    fig2 = plt.figure(figsize=(6,2))
    plt.plot(data['Date'],data['RSI'],linewidth=1)
    plt.axhline(70)
    plt.axhline(30)
    st.pyplot(fig2)

else:
    st.info("Upload CSV")
