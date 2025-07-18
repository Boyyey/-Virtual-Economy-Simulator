"""
Market news and policy event generation for the Virtual Economy Simulator.
"""
import random

NEWS_EVENTS = [
    "Interest rates rose today.",
    "Interest rates fell today.",
    "Government announced new stimulus.",
    "Major bank failure reported.",
    "Tech innovation boosts productivity.",
    "Trade war escalates.",
    "No significant news today.",
]

SHOCK_EVENTS = [
    "Sudden market crash!",
    "Unexpected boom!",
    "Currency devaluation.",
    "Pandemic outbreak.",
    "Energy crisis.",
]

def generate_news(round_num, enable_shocks=True):
    """
    Generate market news, with occasional shocks.
    """
    if enable_shocks and random.random() < 0.05:
        return random.choice(SHOCK_EVENTS)
    if round_num % 50 == 0:
        return "Quarterly economic report released."
    return random.choice(NEWS_EVENTS) 