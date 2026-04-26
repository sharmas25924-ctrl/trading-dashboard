import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Prop Desk Admin", layout="wide")

# --- 1. DATABASE & AUTH INITIALIZATION ---
if 'db' not in st.session_state:
    # 50 Traders + 1 Admin
    users = {
        "admin": {"pwd": "admin123", "role": "admin", "name": "Master Admin"},
    }
    for i in range(1, 51):
        users[f"trader{i}"] = {"pwd": f"pass{i}", "role": "trader", "name": f"Employee {i}"}
    
    st.session_state.db = users

if 'trader_stats' not in st.session_state:
    # Traders ki live performance table
    st.session_state.trader_stats = pd.DataFrame([
        {"UserID": f"trader{i}", "Name": f"Employee {i}", "PnL": 0, "MaxLoss": 5000, "Status": "Active"}
        for i in range(1, 51)
    ])

# --- 2. LOGIN SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.sidebar.title("🔐 Terminal Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username in st.session_state.db and st.session_state.db[username]["pwd"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = st.session_state.db[username]["role"]
            st.rerun()
        else:
            st.sidebar.error("Invalid Username/Password")

if not st.session_state.logged_in:
    login()
    st.info("Please login to access the trading terminal.")
    st.stop()

# --- 3. AUTO-SQUARE OFF LOGIC ---
def auto_square_off():
    # Loop through all traders to check violations
    for index, row in st.session_state.trader_stats.iterrows():
        if row['PnL'] <= -row['MaxLoss'] and row['Status'] == "Active":
            st.session_state.trader_stats.at[index, 'Status'] = "BLOCKED"
            # Actual API Call to close trades would go here

# --- 4. DASHBOARD VIEWS ---

# --- A. MASTER ADMIN VIEW ---
if st.session_state.role == "admin":
    st.title("🛡️ MASTER CONTROL PANEL")
    
    # Summary Cards
    active_count = len(st.session_state.trader_stats[st.session_state.trader_stats['Status'] == "Active"])
    total_pnl = st.session_state.trader_stats['PnL'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Traders", f"{active_count} / 50")
    col2.metric("Total Group P&L", f"₹{total_pnl}", delta=float(total_pnl))
    col3.error(f"Blocked Accounts: {50 - active_count}")

    st.markdown("### 📊 Real-time Monitoring")
    # Admin can edit MaxLoss and Status directly
    updated_df = st.data_editor(st.session_state.trader_stats, hide_index=True, use_container_width=True)
    
    if st.button("Save Changes & Sync Rules"):
        st.session_state.trader_stats = updated_df
        st.success("Configuration Updated!")

# --- B. EMPLOYEE / TRADER VIEW ---
else:
    user_id = st.session_state.user
    user_name = st.session_state.db[user_id]["name"]
    
    st.title(f"📈 Trader Terminal: {user_name}")
    
    # Get current trader data
    idx = st.session_state.trader_stats[st.session_state.trader_stats['UserID'] == user_id].index[0]
    current_data = st.session_state.trader_stats.iloc[idx]

    if current_data['Status'] == "BLOCKED":
        st.error("❌ TRADING DISCONTINUED: You have hit your daily loss limit or Admin has suspended your account.")
    else:
        c1, c2 = st.columns(2)
        # Simulation for testing
        test_pnl = c1.number_input("Current Live P&L (Mock)", value=float(current_data['PnL']))
        st.session_state.trader_stats.at[idx, 'PnL'] = test_pnl
        
        c2.metric("Your Risk Limit", f"₹{current_data['MaxLoss']}")
        
        auto_square_off() # Run risk engine
        
        st.success("Account Status: Active. You are clear to trade.")
        st.button("Execute Order")

# Logout Button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()