import requests

API_KEY = "D2MyI4eYNXDNJzpYT4N6nTQ2amVbJaG5"
BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_income_statement(ticker):
    url = f"{BASE_URL}/income-statement/{ticker}?limit=1&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()[0]
        return {
            "revenue": data.get("revenue", 0),
            "netIncome": data.get("netIncome", 0),
            "eps": data.get("eps", 0)
        }
    except:
        return None

def get_ratios(ticker):
    url = f"{BASE_URL}/ratios/{ticker}?limit=1&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()[0]
        return {
            "priceEarningsRatio": data.get("priceEarningsRatio", 0),
            "returnOnEquity": data.get("returnOnEquity", 0),
            "debtEquityRatio": data.get("debtEquityRatio", 0)
        }
    except:
        return None
