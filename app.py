import streamlit as st
import pandas as pd
from fmp_api import get_income_statement, get_ratios
from extra_data import get_profile, get_key_metrics
from tickers import ticker_list

def format_value(value, is_percent=False):
    try:
        if value is None:
            return "-"
        value = float(value)
        if is_percent:
            return f"{value:.2%}"
        if abs(value) >= 200_000:
            return f"{value / 1_000_000:.2f} mln"
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

    if profile and key_metrics:
        with st.expander("🧾 Bedrijfsprofiel & Kerninfo", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("Prijs", format_value(profile.get("price")))
            col1.metric("Marktkapitalisatie", format_value(profile.get("mktCap")))
            col2.metric("Dividend (per aandeel)", format_value(profile.get("lastDiv")))
            col2.metric("Dividendrendement", format_value(key_metrics.get("dividendYield", 0), is_percent=True))
            col3.metric("Payout Ratio", format_value(key_metrics.get("payoutRatio", 0), is_percent=True))
            st.caption(profile.get("description", ""))

    if income_data:
        df_income = pd.DataFrame(income_data)
        with st.expander("📈 Omzet, Winst en EPS"):
            st.dataframe(df_income[["date", "revenue", "netIncome", "eps"]].set_index("date"))

    if ratio_data:
        df_ratio = pd.DataFrame(ratio_data)
        with st.expander("📐 Ratio's over de jaren"):
            st.dataframe(df_ratio[["date", "priceEarningsRatio", "returnOnEquity", "debtEquityRatio"]].set_index("date"))

        with st.expander("🧮 Extra Ratio's"):
            extra_cols = [
                "currentRatio", "quickRatio", "grossProfitMargin",
                "operatingProfitMargin", "netProfitMargin", "returnOnAssets", "inventoryTurnover"
            ]
            available_cols = [col for col in extra_cols if col in df_ratio.columns]
            if available_cols:
                st.dataframe(df_ratio[["date"] + available_cols].set_index("date"))

        with st.expander("📊 Grafieken"):
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df_income.set_index("date")[["revenue", "netIncome"]])
            with col2:
                st.line_chart(df_ratio.set_index("date")[["priceEarningsRatio", "returnOnEquity"]])
    else:
        st.warning("Geen ratio-data gevonden.")
