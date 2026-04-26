import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. Page Setup
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# 2. Market Data & Chart Function
def show_market_chart():
    st.subheader("📊 Live Market Chart")
    symbol = st.selectbox("Select Asset", ["^NSEI", "^NSEBANK", "RELIANCE.NS", "SBIN.NS"])
    
    try:
        data = yf.download(symbol, period="1mo", interval="1d")
        if not data.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Data fetch nahi ho raha hai.")
    except Exception as e:
        st.error(f"Error: {e}")

# 3. Simple Login Logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Terminal")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong ID/Password")
else:
    # Dashboard Content
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title("📈 Trading Terminal - Welcome Sonu")
    
    # Show Chart
    show_market_chart()
    
    st.divider()
    st.success("Account Status: Active")
