"""
Data storage and analysis utilities for the Virtual Economy Simulator.
Handles saving/loading results as CSV.
"""
import pandas as pd
import os

def save_wealth_history(agents, round_num, save_path):
    """
    Save agent wealths to CSV.
    """
    data = {'agent_id': [a.agent_id for a in agents], 'wealth': [a.wealth for a in agents]}
    df = pd.DataFrame(data)
    os.makedirs(save_path, exist_ok=True)
    df.to_csv(os.path.join(save_path, f"wealth_{round_num}.csv"), index=False)

def save_price_history(market, save_path):
    """
    Save price history for all goods to CSV.
    """
    os.makedirs(save_path, exist_ok=True)
    for name, history in market.history.items():
        df = pd.DataFrame({'price': history})
        df.to_csv(os.path.join(save_path, f"{name}_prices.csv"), index=False)

def save_gini_history(gini_history, save_path):
    """
    Save Gini coefficient history to CSV.
    """
    os.makedirs(save_path, exist_ok=True)
    df = pd.DataFrame({'gini': gini_history})
    df.to_csv(os.path.join(save_path, "gini.csv"), index=False) 