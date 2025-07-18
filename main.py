"""
Main entry point for the Virtual Economy Simulator.
Initializes agents, environment, runs simulation, saves and visualizes results.
"""
import config
from agents import BaseAgent, RuleBasedAgent, LLMAgent, BusinessAgent, GovernmentAgent
from environment import Economy
from llm_interface import LLMInterface
from news import generate_news
from visualization import plot_wealth_distribution, plot_price_history, plot_gini
from data import save_wealth_history, save_price_history, save_gini_history
from utils import set_random_seed
import os

if __name__ == "__main__":
    set_random_seed(config.RANDOM_SEED)
    # --- Initialize agents ---
    agents = []
    llm_interface = LLMInterface() if config.USE_LLM else None
    for i in range(config.NUM_AGENTS):
        risk = config.RISK_PROFILES[i % len(config.RISK_PROFILES)]
        if config.USE_LLM:
            agent = LLMAgent(i, config.INITIAL_WEALTH, risk, llm_interface=llm_interface)
        else:
            agent = RuleBasedAgent(i, config.INITIAL_WEALTH, risk)
        agents.append(agent)
    # --- Initialize businesses ---
    businesses = [BusinessAgent(f"B{i}", config.INITIAL_BUSINESS_WEALTH, 'neutral') for i in range(config.NUM_BUSINESSES)]
    # --- Initialize government ---
    government = GovernmentAgent("GOV", 0, 'neutral')
    # --- Initialize environment ---
    env = Economy(agents, businesses, government, config)
    # --- Run simulation ---
    for round_num in range(config.NUM_ROUNDS):
        env.step()
        if config.SAVE_RESULTS:
            save_wealth_history(agents, round_num, config.RESULTS_PATH)
        if round_num % config.PLOT_INTERVAL == 0:
            plot_wealth_distribution(agents, round_num, config.RESULTS_PATH)
    # --- Save and plot summary results ---
    if config.SAVE_RESULTS:
        save_price_history(env.market, config.RESULTS_PATH)
        save_gini_history(env.gini_history, config.RESULTS_PATH)
        plot_price_history(env.market, config.RESULTS_PATH)
        plot_gini(env.gini_history, config.RESULTS_PATH)
    # --- Optionally launch dashboard ---
    if config.ENABLE_DASHBOARD:
        try:
            import dashboard
            dashboard.show_dashboard(config.RESULTS_PATH)
        except Exception as e:
            print(f"Dashboard error: {e}") 