import streamlit as st
import requests
import os

# Read API endpoint from an environment variable, with a default fallback
API_ENDPOINT = os.environ.get('API_ENDPOINT', 'http://localhost:5000/inference')

# Streamlit Interface
st.title("LLM Inference App")
input_text = st.text_area("Enter your query:")
if st.button("Submit"):
    response = requests.post(API_ENDPOINT, json={"query": input_text})
    if response.status_code == 200:
        st.write("Response:", response.json().get("output", "No output returned"))
    else:
        st.write(f"Error {response.status_code}: {response.text}")
