import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.asset_classes import Stock, Crypto
from src.services.portfolio_manager import Portfolio

st.set_page_config(layout="wide")
st.title("Advanced Portfolio Simulator (OOP & Streamlit)")

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = Portfolio()
    
    # Attempt to load saved data first
    loaded = st.session_state.portfolio.load_portfolio()
    
    if not loaded or not st.session_state.portfolio.get_assets():
        # Load initial samples if no data was found
        st.session_state.portfolio.add_asset(Stock(ticker="GOOG", quantity=5, purchase_price=100.0))
        st.session_state.portfolio.add_asset(Crypto(ticker="BTC", quantity=0.5, purchase_price=50000.0))
        st.session_state.portfolio.update_all_prices()

portfolio = st.session_state.portfolio

with st.sidebar:
    st.header("Add New Asset")
    
    asset_type = st.selectbox("Asset Type", ["Stock", "Crypto"])
    ticker = st.text_input("Ticker", value="TSLA" if asset_type == "Stock" else "ETH")
    quantity = st.number_input("Quantity", min_value=0.01, value=1.0)
    purchase_price = st.number_input("Purchase Price", min_value=0.01, value=100.0)

    if st.button("Add to Portfolio"):
        if asset_type == "Stock":
            new_asset = Stock(ticker, quantity, purchase_price)
        else:
            new_asset = Crypto(ticker, quantity, purchase_price)
            
        portfolio.add_asset(new_asset)
        new_asset.fetch_current_price()
        portfolio.save_portfolio() # Save after adding
        st.success(f"{ticker} added to portfolio.")

if st.button("Update Prices (Polymorphism Process)"):
    st.session_state.portfolio.update_all_prices()
    st.session_state.portfolio.save_portfolio() # Save after updating
    st.rerun()

st.header("Investment Portfolio Summary")

if not portfolio.get_assets():
    st.info("Your portfolio is empty. Add an asset.")
else:
    summary_data = portfolio.get_portfolio_summary()
    df_summary = pd.DataFrame(summary_data)
    
    col1, col2, col3 = st.columns(3)
    
    total_value = portfolio.get_total_value()
    total_gain = portfolio.calculate_total_gain()
    
    col1.metric("Total Portfolio Value", f"${total_value:,.2f}")
    col2.metric("Total Gain/Loss ($)", f"${total_gain:,.2f}", f"{total_gain / (total_value - total_gain) * 100:.2f}%")
    col3.metric("Number of Assets", len(portfolio.get_assets()))

    st.subheader("Detailed Asset Table")
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    st.subheader("Asset Distribution in Portfolio")
    
    fig_pie = px.pie(df_summary, values='Current Value', names='Ticker', 
                      title='Percentage Share of Each Asset', hole=.3)
    st.plotly_chart(fig_pie, use_container_width=True)