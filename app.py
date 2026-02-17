import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage

st.set_page_config(layout="wide")

st.title("📈 Smart Stock Analyzer")

uploaded = st.file_uploader("Upload Kaggle Stock CSV", type="csv")

if uploaded:

    df = pd.read_csv(uploaded)

    st.success("Dataset Loaded")

    # ---- change column name if needed ----
    stock_column = "Symbol"   # adjust if your CSV differs

    stocks = df[stock_column].unique()

    selected_stock = st.selectbox("🔍 Search / Select Stock", stocks)

    stock_df = df[df[stock_column] == selected_stock]

    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stock_df = stock_df.sort_values("Date")

    # Moving Average
    stock_df['MA20'] = stock_df['Close'].rolling(20).mean()

    # RSI
    delta = stock_df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    stock_df['RSI'] = 100 - (100/(1+rs))

    latest = stock_df.iloc[-1]

    close = latest['Close']
    ma20 = latest['MA20']
    rsi = latest['RSI']

    # Recommendation
    if close > ma20 and rsi < 70:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"

    st.subheader(f"📊 Recommendation: {signal}")

    col1,col2,col3 = st.columns(3)
    col1.metric("Close", round(close,2))
    col2.metric("MA20", round(ma20,2))
    col3.metric("RSI", round(rsi,2))

    # Charts
    fig = plt.figure()
    plt.plot(stock_df['Date'], stock_df['Close'], label="Close")
    plt.plot(stock_df['Date'], stock_df['MA20'], label="MA20")
    plt.legend()
    st.pyplot(fig)

    fig2 = plt.figure()
    plt.plot(stock_df['Date'], stock_df['RSI'])
    plt.axhline(70)
    plt.axhline(30)
    st.pyplot(fig2)

    # ================= EMAIL FEATURE =================

    st.subheader("📧 Get Full Report on Email")

    user_email = st.text_input("Enter your email")

    if st.button("Send Report"):

        body = f"""
Stock: {selected_stock}

Close Price: {close}
MA20: {ma20}
RSI: {rsi}

Recommendation: {signal}

RSI > 70 = Overbought
RSI < 30 = Oversold

Generated from Stock Analyzer App
"""

        EMAIL = "yourgmail@gmail.com"
        PASSWORD = "your-app-password"

        msg = EmailMessage()
        msg['Subject'] = f"Stock Report – {selected_stock}"
        msg['From'] = EMAIL
        msg['To'] = user_email
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(EMAIL,PASSWORD)
                smtp.send_message(msg)

            st.success("Email sent successfully!")

        except:
            st.error("Email failed – check credentials")

else:
    st.info("Upload CSV to begin")

