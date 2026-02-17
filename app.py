import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import smtplib
from email.message import EmailMessage

st.set_page_config(layout="wide")
st.title("📈 Smart Stock Analyzer Ultimate")

uploaded = st.file_uploader("Upload Stock CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)

    st.sidebar.header("Controls")

    # AUTO STOCK DETECTION
    if 'Symbol' in df.columns:
        symbols = df['Symbol'].unique()
        stock = st.sidebar.selectbox("🔍 Select Stock", symbols)
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

    latest = data.iloc[-1]

    close = latest['Close']
    rsi = latest['RSI']
    ma20 = latest['MA20']

    # Buy Sell Hold
    if close > ma20 and rsi < 70:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"

    # Cap Classification (proxy logic)
    if close < 500:
        cap = "Small Cap"
    elif close < 2000:
        cap = "Mid Cap"
    else:
        cap = "Large Cap"

    # ML Prediction
    clean = data.dropna()
    X = np.arange(len(clean)).reshape(-1,1)
    y = clean['Close']

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(X)+5]])[0]

    # Dashboard
    st.subheader(f"{stock}")
    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Close",round(close,2))
    col2.metric("RSI",round(rsi,2))
    col3.metric("Signal",signal)
    col4.metric("Category",cap)

    st.metric("Predicted Price (5 days)",round(future,2))

    # Small charts
    fig = plt.figure(figsize=(6,3))
    plt.plot(data['Date'],data['Close'],linewidth=1)
    plt.plot(data['Date'],data['MA20'],linewidth=1)
    st.pyplot(fig)

    fig2 = plt.figure(figsize=(6,2))
    plt.plot(data['Date'],data['RSI'],linewidth=1)
    plt.axhline(70)
    plt.axhline(30)
    st.pyplot(fig2)

    # EMAIL
    st.subheader("📧 Email Full Report")
    email = st.text_input("Enter Email")

    if st.button("Send Report"):

        EMAIL="yourgmail@gmail.com"
        PASSWORD="your-app-password"

        body = f"""
Stock: {stock}
Close: {close}
RSI: {rsi}
Signal: {signal}
Category: {cap}
Predicted: {future}
"""

        msg=EmailMessage()
        msg['Subject']="Stock Analysis Report"
        msg['From']=EMAIL
        msg['To']=email
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(EMAIL,PASSWORD)
                smtp.send_message(msg)
            st.success("Email Sent")

        except:
            st.error("Email Failed")

else:
    st.info("Upload CSV")
