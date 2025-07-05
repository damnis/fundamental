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

@st.cache_data(ttl=3600)
def get_earning_calendar(ticker):
    url = f"{BASE_URL}/earning_calendar/{ticker}?limit=10&apikey={API_KEY}"
    try:
        return requests.get(url).json()
    except:
        return []

@st.cache_data(ttl=3600)
def get_dividend_history(ticker):
    url = f"{BASE_URL}/historical-price-full/stock_dividend/{ticker}?apikey={API_KEY}"
    try:
        return requests.get(url).json().get("historical", [])
    except:
        return []

@st.cache_data(ttl=3600)
def get_quarterly_eps(ticker):
    url = f"{BASE_URL}/income-statement/{ticker}?period=quarter&limit=6&apikey={API_KEY}"
    try:
        return requests.get(url).json()
    except:
        return []

@st.cache_data(ttl=3600)
def get_eps_forecast(ticker):
    url = f"{BASE_URL}/analyst-estimates/{ticker}?limit=1&apikey={API_KEY}"
    try:
        return requests.get(url).json()
    except:
        return []
