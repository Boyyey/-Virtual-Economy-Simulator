"""
Simulation configuration and parameters for the Virtual Economy Simulator.
Edit these values to run different experiments.
"""

# --- Simulation Parameters ---
NUM_AGENTS = 200  # Number of agents in the simulation
NUM_BUSINESSES = 10  # Number of business agents
NUM_ROUNDS = 1000  # Number of time steps
GOODS = ['GoodA']  # List of tradable goods
INITIAL_WEALTH = 1000  # Starting wealth for each agent
INITIAL_BUSINESS_WEALTH = 5000
RISK_PROFILES = ['cautious', 'neutral', 'risk_taker']

# --- LLM / Agent Reasoning ---
USE_LLM = False  # Set True to use LLMs for agent decisions
LLM_MODEL = 'gpt-3.5-turbo'  # or 'phi-3', 'mistral', etc.
LLM_API_KEY = ''  # Set your OpenAI or local LLM API key
LLM_MAX_TOKENS = 64
LLM_TEMPERATURE = 0.7

# --- Policy Layer ---
ENABLE_UBI = False
UBI_AMOUNT = 50
ENABLE_WEALTH_TAX = False
WEALTH_TAX_RATE = 0.01  # 1% per round
ENABLE_MARKET_SHOCKS = True

# --- Visualization ---
PLOT_INTERVAL = 10  # Plot every N rounds
ENABLE_DASHBOARD = True

# --- Data Storage ---
SAVE_RESULTS = True
RESULTS_PATH = 'results/'

# --- Random Seed ---
RANDOM_SEED = 42 