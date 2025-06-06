# app.py

import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
fred_api_key = os.getenv("FRED_API_KEY")

# Page configuration
st.set_page_config(page_title="Macro Dashboard", layout="wide")

# Title and introduction
st.title("🌍 Macro Dashboard")
st.subheader("Your expanding window into the global economy")

st.markdown("""
This dashboard will gradually include:
- 📊 Sector-based macroeconomic data
- 🤖 AI-generated insights
- 🔗 Visual linkages between indicators
""")

st.info("Still in early development — sector foundations are being laid.")

# -----------------------------------------------
# Section structure
# Each section imports from data_sources/*.py
# -----------------------------------------------

# ₿ Bitcoin & Crypto
from data_sources.bitcoin_data import fetch_data as fetch_bitcoin
st.markdown("---")
st.header("₿ Bitcoin & Crypto")

with st.spinner("Fetching Bitcoin data..."):
    btc_df = fetch_bitcoin()
    if not btc_df.empty:
        st.metric("Current BTC Price", f"${btc_df['BTC Price (USD)'].iloc[0]:,.2f}")
        st.line_chart(btc_df.sort_values('Date').set_index('Date')["BTC Price (USD)"])
    else:
        st.warning("No Bitcoin data available.")


# 🇺🇸 Inflation & Monetary Policy
from data_sources.inflation_data import fetch_data as fetch_inflation
from data_sources.interest_rates_data import fetch_data as fetch_interest_rates
from data_sources.employment_data import fetch_data as fetch_employment

st.markdown("---")
st.header("🇺🇸 Inflation & Monetary Policy")

# Inflation
with st.spinner("Fetching US inflation data..."):
    inflation_df = fetch_inflation(fred_api_key)
    if not inflation_df.empty:
        st.metric("Latest Monthly Inflation (%)", f"{inflation_df['Monthly Inflation (%)'].iloc[-1]:.2f}%")
        st.line_chart(inflation_df.set_index('Date')['Monthly Inflation (%)'])
    else:
        st.warning("No inflation data.")

# Interest Rates
with st.spinner("Fetching interest rate data..."):
    ir_df = fetch_interest_rates(fred_api_key)
    if not ir_df.empty:
        st.line_chart(ir_df.set_index("Date")["Effective Federal Funds Rate (%)"])
    else:
        st.warning("No interest rate data.")

# Employment
with st.spinner("Fetching employment data..."):
    emp_df = fetch_employment(fred_api_key)
    if not emp_df.empty:
        st.line_chart(emp_df.set_index("Date")["Unemployment Rate (%)"])
    else:
        st.warning("No employment data.")


# 🛢️ Commodities & Energy
from data_sources.commodities_data import fetch_data as fetch_commodities
st.markdown("---")
st.header("🛢️ Commodities & Energy")

# Placeholder - real data to be added later
commodities_df = fetch_commodities()
if not commodities_df.empty:
    st.dataframe(commodities_df)
else:
    st.warning("Commodities data not yet available.")


# 📈 Equities & Financial Markets
from data_sources.equities_data import fetch_data as fetch_equities
st.markdown("---")
st.header("📈 Equities & Financial Markets")

equities_df = fetch_equities()
if not equities_df.empty:
    st.dataframe(equities_df)
else:
    st.warning("Equities data not yet available.")


# 💸 Fund Flows
from data_sources.fund_flows_data import fetch_data as fetch_flows
st.markdown("---")
st.header("💸 Capital Flows & ETF Trends")

flows_df = fetch_flows()
if not flows_df.empty:
    st.dataframe(flows_df)
else:
    st.warning("Fund flows data not yet available.")


# 🏠 Real Estate
from data_sources.real_estate_data import fetch_data as fetch_real_estate
st.markdown("---")
st.header("🏠 Real Estate")

real_estate_df = fetch_real_estate()
if not real_estate_df.empty:
    st.dataframe(real_estate_df)
else:
    st.warning("Real estate data not yet available.")


# 🔗 Supply Chains
from data_sources.supply_chains_data import fetch_data as fetch_supply_chains
st.markdown("---")
st.header("🔗 Supply Chains")

supply_df = fetch_supply_chains()
if not supply_df.empty:
    st.dataframe(supply_df)
else:
    st.warning("Supply chain data not yet available.")


# 🧭 Macro Themes
from data_sources.macro_themes_data import fetch_data as fetch_macro_themes
st.markdown("---")
st.header("🧭 Macro Themes")

themes_df = fetch_macro_themes()
if not themes_df.empty:
    st.dataframe(themes_df)
else:
    st.warning("Macro theme data not yet available.")


# 🔮 AI Insights - placeholder
st.markdown("---")
st.header("🔮 AI Insights")
st.info("Coming soon — AI-generated macroeconomic interpretations.")


# Footer
st.markdown("---")
st.caption("Built with ❤️ by Jakob | Work in Progress")
