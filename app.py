import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import smtplib
from email.message import EmailMessage

st.set_page_config(layout="wide")

st.title("📈 Smart Stock Analyzer Pro")

uploaded = st.file_uploader("Upload Multi-Stock Kaggle CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)

    st.sidebar.header("Controls")

    df['Date'] = pd.to_datetime(df['Date'])

    symbols = df['Symbol'].unique()
    stock = st.sidebar.selectbox("🔍 Select Stock", symbols)

    data = df[df['Symbol']==stock].sort_values("Date")

    # Indicators
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()

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

    # ML Prediction
    data2 = data.dropna()
    X = np.arange(len(data2)).reshape(-1,1)
    y = data2['Close']

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(X)+5]])[0]

    st.metric("Predicted Price (5 days)", round(future,2))

    # Email
    st.subheader("📧 Email Report")
    email = st.text_input("Your Email")

    if st.button("Send Report"):

        EMAIL="yourgmail@gmail.com"
        PASSWORD="your-app-password"

        msg=EmailMessage()
        msg['Subject']=f"{stock} Stock Report"
        msg['From']=EMAIL
        msg['To']=email

        msg.set_content(f"""
Stock: {stock}
Close: {close}
RSI: {rsi}
Signal: {signal}
Predicted: {future}
""")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(EMAIL,PASSWORD)
                smtp.send_message(msg)
            st.success("Email Sent!")

        except:
            st.error("Email Failed")

else:
    st.info("Upload CSV")
