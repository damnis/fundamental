import requests
import streamlit as st

API_KEY = "D2MyI4eYNXDNJzpYT4N6nTQ2amVbJaG5"
BASE_URL = "https://financialmodelingprep.com/api/v3"

@st.cache_data(ttl=3600)
def get_income_statement(ticker, years=5):
    url = f"{BASE_URL}/income-statement/{ticker}?limit={years}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return []

@st.cache_data(ttl=3600)
def get_ratios(ticker, years=5):
    url = f"{BASE_URL}/ratios/{ticker}?limit={years}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return []
