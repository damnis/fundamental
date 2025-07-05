import streamlit as st
from fmp_api import get_income_statement, get_ratios
from tickers import ticker_list

st.set_page_config(page_title="Fundamentele Analyse Tool", layout="wide")
st.title("📊 Fundamentool: Ratio-analyse van aandelen")

ticker = st.selectbox("Selecteer een ticker", ticker_list)

if ticker:
    st.info(f"📥 Data wordt opgehaald voor: {ticker}")

    income = get_income_statement(ticker)
    ratios = get_ratios(ticker)

    if income and ratios:
        st.subheader("📈 Kerncijfers")
        st.metric("Omzet", f"${income['revenue']:,}")
        st.metric("Winst", f"${income['netIncome']:,}")
        st.metric("EPS", f"${income['eps']}")

        st.subheader("📐 Belangrijke ratio's")
        st.metric("K/W-ratio", round(ratios['priceEarningsRatio'], 2))
        st.metric("ROE", f"{round(ratios['returnOnEquity']*100, 2)}%")
        st.metric("Debt/Equity", round(ratios['debtEquityRatio'], 2))
    else:
        st.error("Kon geen data ophalen. Probeer een andere ticker.")
