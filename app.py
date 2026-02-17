import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Analyzer", layout="centered")

st.title("📈 Stock Analyzer")

uploaded_file = st.file_uploader("Upload your stock CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Basic Info")
    st.write(df.describe())

else:
    st.info("Please upload a CSV file to continue.")



