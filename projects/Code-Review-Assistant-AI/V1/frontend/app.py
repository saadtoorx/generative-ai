import streamlit as st
import requests

st.title("Code Review Assistant (DeepSeek-Coder)")

code_input = st.text_area(
    "Paste your code here:",
    height=300
)

if st.button("Get Review"):
    response = requests.post(
        "http://localhost:8000/review/",
        data={"code": code_input}
    )
    review = response.json().get("review", "No feedback returned.")
    st.subheader("Review & Suggestions:")
    st.code(review)