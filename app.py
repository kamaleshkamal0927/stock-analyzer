import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np

st.set_page_config(page_title="Stock Analyzer ML", layout="wide")

st.title("📈 NIFTY 50 Stock Analyzer")

df = pd.read_csv("nifty50_small.csv")

df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Select Stock")
ticker = st.sidebar.selectbox("Ticker", df["Ticker"].unique())

stock = df[df["Ticker"] == ticker].sort_values("Date")

st.subheader("Preview")
st.dataframe(stock.tail(30))

st.line_chart(stock.set_index("Date")["Close"])

ml = stock.dropna()

X = ml[["Open","High","Low","Volume","MA_50","MA_200"]]
y = ml["Close"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,shuffle=False)

model = RandomForestRegressor()
model.fit(X_train,y_train)

pred = model.predict(X_test)

mae = mean_absolute_error(y_test,pred)

st.metric("MAE", round(mae,2))

next_price = model.predict(X.iloc[-1:].values)[0]

st.success(f"Next Close Prediction ₹{round(next_price,2)}")


