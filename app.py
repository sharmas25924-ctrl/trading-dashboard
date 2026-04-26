st.rerun()
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def trader_dashboard():
    st.title(f"📈 Trader Terminal: {st.session_state.user}")
    
    # --- 1. SYMBOL SELECTION DROPDOWN ---
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_stock = st.selectbox(
            "Select Market/Stock",
            ["NIFTY 50", "BANK NIFTY", "RELIANCE", "HDFC BANK", "SBIN"],
            index=0
        )
    
    # Symbols Mapping for yfinance
    symbols = {
        "NIFTY 50": "^NSEI",
        "BANK NIFTY": "^NSEBANK",
        "RELIANCE": "RELIANCE.NS",
        "HDFC BANK": "HDFCBANK.NS",
        "SBIN": "SBIN.NS"
    }
    ticker = symbols[selected_stock]

    # --- 2. LIVE CHART LOGIC ---
    try:
        # 15-minute interval candles for the last 5 days
        df = yf.download(ticker, period="5d", interval="15m")
        
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])
            
            fig.update_layout(
                title=f"{selected_stock} Live Chart (15 min)",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                height=450,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Market data fetch nahi ho raha. Check Internet.")
    except Exception as e:
        st.error(f"Chart Error: {e}")

    # --- 3. RISK MANAGEMENT SECTION ---
    st.divider()
    # Yahan aapka purana P&L aur Block status wala code rahega
    # ...
