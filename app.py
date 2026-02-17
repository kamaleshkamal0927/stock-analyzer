import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(layout="wide")
st.title("📈 Smart Stock Analyzer")

uploaded = st.file_uploader("Upload Stock CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)

    # Auto stock detect
    if 'Symbol' in df.columns:
        stock = st.sidebar.selectbox("Select Stock", df['Symbol'].unique())
        data = df[df['Symbol']==stock]
    else:
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

    # Clean NaNs (IMPORTANT)
    data = data.dropna()

    latest = data.iloc[-1]

    close = latest['Close']
    rsi = latest['RSI']
    ma20 = latest['MA20']

    # Signal
    if close > ma20 and rsi < 70:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"

    # Cap logic
    if close < 500:
        cap = "Small Cap"
    elif close < 2000:
        cap = "Mid Cap"
    else:
        cap = "Large Cap"

    # ML Prediction
    X = np.arange(len(data)).reshape(-1,1)
    y = data['Close'].values

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(X)+5]])[0]

    # Dashboard
    st.subheader(stock)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Close",round(close,2))
    c2.metric("RSI",round(rsi,2))
    c3.metric("Signal",signal)
    c4.metric("Category",cap)

    st.metric("Predicted Price (5 days)",round(future,2))

    # Small Charts
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
