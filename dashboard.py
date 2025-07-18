"""
Streamlit dashboard for the Virtual Economy Simulator.
Full-featured interactive simulation lab.
"""
import streamlit as st
import pandas as pd
from simulation import Simulation
import types

st.set_page_config(page_title="Virtual Economy Simulator", layout="wide")
st.title("🌍💡 Virtual Economy Simulator Dashboard")

# --- Sidebar: Simulation Controls ---
st.sidebar.header("Simulation Controls")
num_agents = st.sidebar.slider("Number of Agents", 10, 2000, 200, step=10)
num_businesses = st.sidebar.slider("Number of Businesses", 1, 100, 10)
num_rounds = st.sidebar.slider("Number of Rounds", 10, 5000, 1000, step=10)
initial_wealth = st.sidebar.number_input("Initial Wealth (Agents)", 100, 100000, 1000, step=100)
initial_business_wealth = st.sidebar.number_input("Initial Wealth (Businesses)", 100, 100000, 5000, step=100)
risk_profiles = st.sidebar.multiselect("Risk Profiles", ["cautious", "neutral", "risk_taker"], default=["cautious", "neutral", "risk_taker"])
use_llm = st.sidebar.checkbox("Use LLM Agents", value=False)
llm_model = st.sidebar.text_input("LLM Model (if enabled)", "gpt-3.5-turbo")
llm_api_key = st.sidebar.text_input("LLM API Key", type="password")
llm_temp = st.sidebar.slider("LLM Temperature", 0.0, 2.0, 0.7, 0.01)
llm_tokens = st.sidebar.slider("LLM Max Tokens", 16, 256, 64)

# --- Policy Toggles ---
st.sidebar.header("Policy Layer")
enable_ubi = st.sidebar.checkbox("Enable UBI", value=False)
ubi_amount = st.sidebar.number_input("UBI Amount", 0, 10000, 50, step=10)
enable_wealth_tax = st.sidebar.checkbox("Enable Wealth Tax", value=False)
wealth_tax_rate = st.sidebar.slider("Wealth Tax Rate", 0.0, 0.2, 0.01, 0.001)
enable_shocks = st.sidebar.checkbox("Enable Market Shocks", value=True)

# --- Visualization Options ---
st.sidebar.header("Visualization")
plot_interval = st.sidebar.slider("Plot Interval (Rounds)", 1, 100, 10)

# --- Custom News/Events ---
st.sidebar.header("Custom News & Events")
custom_news = st.sidebar.text_area("Custom News (one per line)")

# --- Simulation State ---
if 'sim' not in st.session_state:
    st.session_state['sim'] = None
if 'running' not in st.session_state:
    st.session_state['running'] = False

# --- Parameter Object (use SimpleNamespace for dynamic attributes) ---
params = types.SimpleNamespace()
params.NUM_AGENTS = num_agents
params.NUM_BUSINESSES = num_businesses
params.NUM_ROUNDS = num_rounds
params.GOODS = ['GoodA']
params.INITIAL_WEALTH = initial_wealth
params.INITIAL_BUSINESS_WEALTH = initial_business_wealth
params.RISK_PROFILES = risk_profiles or ["cautious", "neutral", "risk_taker"]
params.USE_LLM = use_llm
params.LLM_MODEL = llm_model
params.LLM_API_KEY = llm_api_key
params.LLM_MAX_TOKENS = llm_tokens
params.LLM_TEMPERATURE = llm_temp
params.ENABLE_UBI = enable_ubi
params.UBI_AMOUNT = ubi_amount
params.ENABLE_WEALTH_TAX = enable_wealth_tax
params.WEALTH_TAX_RATE = wealth_tax_rate
params.ENABLE_MARKET_SHOCKS = enable_shocks
params.PLOT_INTERVAL = plot_interval
params.SAVE_RESULTS = True
params.RESULTS_PATH = 'results/'
params.RANDOM_SEED = 42
params.CUSTOM_NEWS = [line.strip() for line in custom_news.splitlines() if line.strip()]

# --- Controls ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start/Resume Simulation"):
        if st.session_state['sim'] is None or not st.session_state['running']:
            st.session_state['sim'] = Simulation(params)
            st.session_state['running'] = True
            st.success("Simulation started!")
with col2:
    if st.button("Pause Simulation"):
        st.session_state['running'] = False
        st.success("Simulation paused.")
with col3:
    if st.button("Reset Simulation"):
        st.session_state['sim'] = Simulation(params)
        st.session_state['running'] = False
        st.success("Simulation reset.")

# --- Main Simulation Loop ---
if st.session_state['sim'] and st.session_state['running']:
    steps = params.PLOT_INTERVAL
    for _ in range(steps):
        st.session_state['sim'].set_running(True)
        st.session_state['sim'].step()
    st.session_state['sim'].set_running(False)

# --- Results ---
if st.session_state['sim']:
    state = st.session_state['sim'].get_state()
    agents = state['agents']
    market = state['market']
    gini_history = state['gini_history']
    round_num = state['round']
    # Wealth Distribution
    st.subheader(f"Wealth Distribution (Round {round_num})")
    wealths = [a.wealth for a in agents]
    st.bar_chart(pd.Series(wealths, name="Wealth"))
    # Price History
    st.subheader("Price History")
    price_df = pd.DataFrame(market.history)
    st.line_chart(price_df)
    # Gini Coefficient
    st.subheader("Gini Coefficient Over Time")
    st.line_chart(pd.Series(gini_history, name="Gini"))
    # Download Results
    st.subheader("Download Results")
    df = pd.DataFrame({'agent_id': [a.agent_id for a in agents], 'wealth': wealths})
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Wealth Data", csv, "wealth.csv", "text/csv")
    price_csv = price_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Price Data", price_csv, "prices.csv", "text/csv")
    gini_csv = pd.Series(gini_history, name="Gini").to_csv(index=False).encode('utf-8')
    st.download_button("Download Gini Data", gini_csv, "gini.csv", "text/csv")
    # Custom News/Events (display)
    if params.CUSTOM_NEWS:
        st.subheader("Custom News/Events Used")
        for news in params.CUSTOM_NEWS:
            st.info(news)

st.markdown("---")
st.caption("Made with ❤️ for economics, AI, and complexity science.") 