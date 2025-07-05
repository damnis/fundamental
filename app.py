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
        df_income_fmt = df_income.copy()
        df_income_fmt["revenue"] = df_income_fmt["revenue"].apply(format_value)
        df_income_fmt["netIncome"] = df_income_fmt["netIncome"].apply(format_value)
        df_income_fmt["eps"] = df_income_fmt["eps"].apply(format_value)
        df_income_fmt.rename(columns={
            "revenue": "Omzet",
            "netIncome": "Winst",
            "eps": "WPA",
            "date": "Jaar"
        }, inplace=True)

        with st.expander("📈 Omzet, Winst en EPS"):
            st.dataframe(df_income_fmt.set_index("Jaar")[["Omzet", "Winst", "WPA"]])

    if ratio_data:
        df_ratio = pd.DataFrame(ratio_data)
        df_ratio_fmt = df_ratio.copy()
        df_ratio_fmt["priceEarningsRatio"] = df_ratio_fmt["priceEarningsRatio"].apply(format_value)
        df_ratio_fmt["returnOnEquity"] = df_ratio_fmt["returnOnEquity"].apply(lambda x: format_value(x * 100, is_percent=False))
        df_ratio_fmt["debtEquityRatio"] = df_ratio_fmt["debtEquityRatio"].apply(format_value)
        df_ratio_fmt.rename(columns={
            "priceEarningsRatio": "K/W",
            "returnOnEquity": "ROE (%)",
            "debtEquityRatio": "Debt/Equity",
            "date": "Jaar"
        }, inplace=True)

        with st.expander("📐 Ratio's over de jaren"):
            st.dataframe(df_ratio_fmt.set_index("Jaar")[["K/W", "ROE (%)", "Debt/Equity"]])

        with st.expander("🧮 Extra Ratio's"):
            df_extra = df_ratio.copy()
            df_extra.rename(columns={
                "currentRatio": "Current ratio",
                "quickRatio": "Quick ratio",
                "grossProfitMargin": "Bruto marge",
                "operatingProfitMargin": "Operationele marge",
                "netProfitMargin": "Netto marge",
                "returnOnAssets": "Rentabiliteit",
                "inventoryTurnover": "Omloopsnelheid",
                "date": "Jaar"
            }, inplace=True)
            for col in ["Bruto marge", "Operationele marge", "Netto marge"]:
                if col in df_extra.columns:
                    df_extra[col] = df_extra[col].apply(lambda x: format_value(x, is_percent=True))
            for col in ["Current ratio", "Quick ratio", "Rentabiliteit", "Omloopsnelheid"]:
                if col in df_extra.columns:
                    df_extra[col] = df_extra[col].apply(format_value)
            extra_cols = [col for col in df_extra.columns if col != "Jaar"]
            if extra_cols:
                st.dataframe(df_extra.set_index("Jaar")[extra_cols])

        with st.expander("📊 Grafieken"):
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df_income.set_index("date")[["revenue", "netIncome"]])
            with col2:
                chart_df = df_ratio.set_index("date")[["priceEarningsRatio", "returnOnEquity"]].copy()
                chart_df["returnOnEquity"] *= 100
                chart_df.rename(columns={
                    "priceEarningsRatio": "K/W",
                    "returnOnEquity": "ROE (%)"
                }, inplace=True)
                st.line_chart(chart_df)

    with st.expander("📅 Belangrijke datums"):
        st.info("Deze module wordt binnenkort gevuld met earnings en dividend data.")

    with st.expander("📈 EPS analyse"):
        st.info("EPS per kwartaal en jaar komt hier binnenkort beschikbaar.")
