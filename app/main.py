import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API token securely
API_TOKEN = os.getenv("LANGFLOW_API_TOKEN")

# Endpoint URL of the deployed Langflow flow
url = os.getenv("LANGFLOW_FLOW_URL")  # Langflow "run" endpoint for your deployed flow

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# Function to call Langflow API
def run_flow(user_input):
    payload = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()

# Streamlit UI
def main():
    try:
        st.markdown("<h1 style='color: #d72638;'>Fidelidade Smart Assistant</h1>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            html, body, .appview-container, .main {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            .reportview-container .main .block-container {
                padding-top: 2rem;
                padding-right: 2rem;
                padding-left: 2rem;
                padding-bottom: 2rem;
            }
            .stTextArea textarea {
                background-color: #fff5f5;
                border: 1px solid #d72638;
                color: #000000;
            }
            .stButton>button {
                background-color: #d72638;
                color: white;
                border-radius: 8px;
                height: 3em;
                width: 100%;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #b51f2e;
                color: white;
            }
            .stAlert[data-baseweb="notification"] {
                background-color: #ffe6e6 !important;
                color: #000000 !important;
                font-weight: 600;
                border: 1px solid #d72638;
                padding: 1rem;
                font-size: 1rem;
            }
            </style>
        """, unsafe_allow_html=True)

        message = st.text_area("Message", placeholder="Type your question about My Savings, PPR Evoluir, or insurance...")

        if st.button("Ask the Assistant"):
            if not message.strip():
                st.error("Please enter a message.")
                return

            try:
                with st.spinner("Running flow..."):
                    result = run_flow(message)

                response_text = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                st.markdown(response_text)

            except Exception as e:
                st.error(f" Error while running flow: {e}")
    except Exception as e:
        st.error(f" Critical startup error: {e}")

if __name__ == "__main__":
    main()