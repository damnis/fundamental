import streamlit as st
import pandas as pd
from fmp_api import get_income_statement, get_ratios
from extra_data import (
    get_profile, get_key_metrics, get_earning_calendar,
    get_dividend_history, get_quarterly_eps, get_eps_forecast
)
from tickers import ticker_list

def format_value(value, is_percent=False):
    try:
        if value is None:
            return "-"
        value = float(value)
        if is_percent:
            return f"{value:.2%}"
        if abs(value) >= 99_000_000:
            return f"{value / 1_000_000_000:,.2f} mld"
        return f"{value:,.2f}"
    except:
        return "-"

st.set_page_config(page_title="Fundamentele Analyse Tool", layout="wide")
st.title("📊 Fundamentool: Ratio-analyse van aandelen")

ticker = st.selectbox("Selecteer een ticker", ticker_list)

if ticker:
    st.info(f"📥 Data wordt opgehaald voor: {ticker}")

    profile = get_profile(ticker)
    key_metrics = get_key_metrics(ticker)
    income_data = get_income_statement(ticker)
    ratio_data = get_ratios(ticker)
    earnings = get_earning_calendar(ticker)
    dividends = get_dividend_history(ticker)
    eps_quarters = get_quarterly_eps(ticker)
    eps_forecast = get_eps_forecast(ticker)

    if profile and key_metrics:
        with st.expander("🧾 Bedrijfsprofiel & Kerninfo", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("Prijs", format_value(profile.get("price")))
            col1.metric("Marktkapitalisatie", format_value(profile.get("mktCap")))
            col2.metric("Dividend (per aandeel)", format_value(profile.get("lastDiv")))
            col2.metric("Dividendrendement", format_value(key_metrics.get("dividendYield", 0), is_percent=True))
            col3.metric("Payout Ratio", format_value(key_metrics.get("payoutRatio", 0), is_percent=True))
            st.caption(profile.get("description", ""))

    with st.expander("📅 Belangrijke datums"):
        if isinstance(earnings, list) and len(earnings) > 0 and isinstance(earnings[0], dict):
            df_earn = pd.DataFrame(earnings)
            df_earn = df_earn[["date", "eps", "epsEstimated"]]
            df_earn.columns = ["Datum", "Werkelijke EPS", "Verwachte EPS"]
            st.subheader("Earnings kalender:")
            st.dataframe(df_earn.set_index("Datum"))

        if isinstance(dividends, list) and len(dividends) > 0 and isinstance(dividends[0], dict):
            df_div = pd.DataFrame(dividends)
            df_div = df_div[["date", "dividend"]]
            df_div.columns = ["Datum", "Dividend"]
            st.subheader("Dividend historie:")
            st.dataframe(df_div.set_index("Datum"))

    with st.expander("📈 EPS analyse"):
        if isinstance(eps_quarters, list) and len(eps_quarters) > 0 and isinstance(eps_quarters[0], dict):
            df_epsq = pd.DataFrame(eps_quarters)
            df_epsq = df_epsq[["date", "eps"]]
            df_epsq.columns = ["Datum", "EPS"]
            df_epsq["Datum"] = pd.to_datetime(df_epsq["Datum"])
            df_epsq = df_epsq.sort_values("Datum")
            df_epsq["EPS_fmt"] = df_epsq["EPS"].apply(format_value)

            st.subheader("EPS per kwartaal")
            st.dataframe(df_epsq.set_index("Datum")[["EPS_fmt"]])
            st.line_chart(df_epsq.set_index("Datum")[["EPS"]])

        if isinstance(eps_forecast, list) and len(eps_forecast) > 0 and isinstance(eps_forecast[0], dict):
            st.subheader("🔮 Verwachte EPS")
            for f in eps_forecast:
                st.write(f"Periode: {f.get('period')}, Verwachte EPS: {f.get('estimatedEps')}")

