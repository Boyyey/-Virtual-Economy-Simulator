"""
Environment and market classes for the Virtual Economy Simulator.
Handles prices, goods, supply/demand, shocks, and aggregate actions.
"""
import numpy as np
import random
from typing import Dict, List

class Good:
    """
    Represents a tradable good in the economy.
    """
    def __init__(self, name, base_price=100):
        self.name = name
        self.price = base_price
        self.supply = 0
        self.demand = 0

    def update_price(self):
        # Simple price adjustment based on supply/demand
        if self.supply == 0:
            self.price *= 1.05
        else:
            self.price *= (1 + 0.01 * (self.demand - self.supply) / max(self.supply, 1))
        self.price = max(1, self.price)

class Market:
    """
    The market where agents trade goods.
    """
    def __init__(self, goods: List[str]):
        self.goods = {name: Good(name) for name in goods}
        self.history = {name: [] for name in goods}

    def record(self):
        for name, good in self.goods.items():
            self.history[name].append(good.price)

    def clear(self):
        for good in self.goods.values():
            good.supply = 0
            good.demand = 0

    def update_prices(self):
        for good in self.goods.values():
            good.update_price()

class Economy:
    """
    The main environment: manages agents, market, policies, and shocks.
    """
    def __init__(self, agents, businesses, government, config):
        self.agents = agents
        self.businesses = businesses
        self.government = government
        self.config = config
        self.market = Market(config.GOODS)
        self.round = 0
        self.news = ""
        self.policies = {}
        self.gini_history = []

    def step(self):
        # 1. Generate news/shocks
        self.news = self._generate_news()
        # 2. Agents perceive and decide
        env_state = self._get_env_state()
        for agent in self.agents + self.businesses:
            agent.perceive(self.news, self.market.goods, self.policies)
            action = agent.decide(env_state)
            self._apply_action(agent, action)
        # 3. Government acts
        gov_action = self.government.decide(env_state)
        self._apply_gov_action(gov_action)
        # 4. Update market
        self.market.update_prices()
        self.market.record()
        self.market.clear()
        # 5. Update stats
        self.gini_history.append(self._gini())
        self.round += 1

    def _generate_news(self):
        # Placeholder: random news
        if self.config.ENABLE_MARKET_SHOCKS and random.random() < 0.05:
            return "Shock: sudden interest rate change!"
        return "Normal trading day."

    def _get_env_state(self):
        prices = {name: good.price for name, good in self.market.goods.items()}
        return {
            'prices': prices,
            'news': self.news,
            'policies': self.policies,
            'gini': self._gini(),
        }

    def _apply_action(self, agent, action):
        # Example: buy/sell logic
        if action == 'buy' and agent.wealth > self.market.goods['GoodA'].price:
            agent.wealth -= self.market.goods['GoodA'].price
            self.market.goods['GoodA'].demand += 1
        elif action == 'sell':
            agent.wealth += self.market.goods['GoodA'].price
            self.market.goods['GoodA'].supply += 1
        elif action == 'invest':
            agent.wealth *= 1.01  # Small return
        elif action == 'save':
            pass  # No-op
        elif action == 'produce':
            self.market.goods['GoodA'].supply += 1
        elif action == 'adjust_price':
            self.market.goods['GoodA'].price *= random.uniform(0.95, 1.05)

    def _apply_gov_action(self, action):
        if action == 'enable_UBI':
            self.policies['UBI'] = True
        elif action == 'disable_UBI':
            self.policies['UBI'] = False
        # Apply UBI
        if self.policies.get('UBI', False):
            for agent in self.agents:
                agent.wealth += self.config.UBI_AMOUNT
        # Apply wealth tax
        if self.config.ENABLE_WEALTH_TAX:
            for agent in self.agents:
                tax = agent.wealth * self.config.WEALTH_TAX_RATE
                agent.wealth -= tax

    def _gini(self):
        # Calculate Gini coefficient for wealth
        wealths = np.array([a.wealth for a in self.agents])
        if len(wealths) == 0:
            return 0
        diffsum = np.sum(np.abs(wealths[:, None] - wealths))
        return diffsum / (2 * len(wealths)**2 * np.mean(wealths)) 