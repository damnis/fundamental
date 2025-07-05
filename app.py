import streamlit as st
import pandas as pd
from fmp_api import get_income_statement, get_ratios
from tickers import ticker_list

st.set_page_config(page_title="Fundamentele Analyse Tool", layout="wide")
st.title("📊 Fundamentool: Ratio-analyse van aandelen")

ticker = st.selectbox("Selecteer een ticker", ticker_list)

if ticker:
    st.info(f"📥 Data wordt opgehaald voor: {ticker}")

    income_data = get_income_statement(ticker)
    ratio_data = get_ratios(ticker)

    if income_data and ratio_data:
        df_income = pd.DataFrame(income_data)
        df_ratio = pd.DataFrame(ratio_data)

        st.subheader("📈 Kerncijfers over laatste jaren")
        st.dataframe(df_income[["date", "revenue", "netIncome", "eps"]].set_index("date"))

        st.subheader("📐 Belangrijke ratio's over tijd")
        st.dataframe(df_ratio[["date", "priceEarningsRatio", "returnOnEquity", "debtEquityRatio"]].set_index("date"))

        st.subheader("📊 Visualisaties")

        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(df_income.set_index("date")[["revenue", "netIncome"]])
        with col2:
            st.line_chart(df_ratio.set_index("date")[["priceEarningsRatio", "returnOnEquity"]])
    else:
        st.error("Kon geen data ophalen. Probeer een andere ticker.")
