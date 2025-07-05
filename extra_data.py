import requests
import streamlit as st

API_KEY = "D2MyI4eYNXDNJzpYT4N6nTQ2amVbJaG5"
BASE_URL = "https://financialmodelingprep.com/api/v3"

@st.cache_data(ttl=3600)
def get_profile(ticker):
    url = f"{BASE_URL}/profile/{ticker}?apikey={API_KEY}"
    try:
        data = requests.get(url).json()
        return data[0] if data else None
    except:
        return None

@st.cache_data(ttl=3600)
def get_key_metrics(ticker):
    url = f"{BASE_URL}/key-metrics/{ticker}?limit=1&apikey={API_KEY}"
    try:
        data = requests.get(url).json()
        return data[0] if data else None
    except:
        return None
