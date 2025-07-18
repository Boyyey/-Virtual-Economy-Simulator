"""
Visualization utilities for the Virtual Economy Simulator.
Plots wealth, prices, Gini coefficient, and agent networks.
"""
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_wealth_distribution(agents, round_num, save_path=None):
    """
    Plot histogram of agent wealth.
    """
    wealths = [a.wealth for a in agents]
    plt.figure(figsize=(8, 4))
    plt.hist(wealths, bins=30, color='skyblue', edgecolor='black')
    plt.title(f"Wealth Distribution (Round {round_num})")
    plt.xlabel("Wealth")
    plt.ylabel("Number of Agents")
    if save_path:
        plt.savefig(os.path.join(save_path, f"wealth_{round_num}.png"))
    plt.close()

def plot_price_history(market, save_path=None):
    """
    Plot price history for all goods.
    """
    for name, history in market.history.items():
        plt.plot(history, label=name)
    plt.title("Price History")
    plt.xlabel("Round")
    plt.ylabel("Price")
    plt.legend()
    if save_path:
        plt.savefig(os.path.join(save_path, "prices.png"))
    plt.close()

def plot_gini(gini_history, save_path=None):
    """
    Plot Gini coefficient over time.
    """
    plt.plot(gini_history, color='purple')
    plt.title("Gini Coefficient Over Time")
    plt.xlabel("Round")
    plt.ylabel("Gini Coefficient")
    if save_path:
        plt.savefig(os.path.join(save_path, "gini.png"))
    plt.close() 