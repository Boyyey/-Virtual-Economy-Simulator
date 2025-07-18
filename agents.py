"""
Agent classes for the Virtual Economy Simulator.
Includes: BaseAgent, RuleBasedAgent, LLMAgent, BusinessAgent, GovernmentAgent.
"""
import random
from typing import List, Dict, Any
import numpy as np

class BaseAgent:
    """
    Base class for all agents. Handles wealth, memory, risk, and basic actions.
    """
    def __init__(self, agent_id, initial_wealth, risk_profile, memory_length=5):
        self.agent_id = agent_id
        self.wealth = initial_wealth
        self.risk_profile = risk_profile
        self.memory = []  # Stores last N decisions, moods, etc.
        self.memory_length = memory_length
        self.mood = 'neutral'  # 'optimistic', 'pessimistic', etc.
        self.last_action = None

    def update_memory(self, info):
        self.memory.append(info)
        if len(self.memory) > self.memory_length:
            self.memory.pop(0)

    def perceive(self, market_news, prices, policies):
        """Process market news, prices, and policies."""
        pass

    def decide(self, env_state):
        """Decide action based on environment state."""
        raise NotImplementedError

    def act(self, env):
        """Perform action in the environment."""
        pass

class RuleBasedAgent(BaseAgent):
    """
    Agent with simple rule-based decision logic.
    """
    def decide(self, env_state):
        # Example: buy if price dropped, sell if price rose, else hold
        prices = env_state['prices']
        news = env_state['news']
        last_price = self.memory[-1]['price'] if self.memory else prices['GoodA']
        action = 'hold'
        if prices['GoodA'] < last_price:
            action = 'buy'
        elif prices['GoodA'] > last_price:
            action = 'sell'
        # Add risk/mood logic
        if self.risk_profile == 'risk_taker' and random.random() < 0.2:
            action = 'invest'
        self.last_action = action
        return action

class LLMAgent(BaseAgent):
    """
    Agent that uses an LLM or prompt-based logic for decisions.
    """
    def __init__(self, *args, llm_interface=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm_interface = llm_interface

    def decide(self, env_state):
        if self.llm_interface is None:
            return self._rule_based_decision(env_state)
        prompt = self._build_prompt(env_state)
        action = self.llm_interface.get_action(prompt)
        self.last_action = action
        return action

    def _build_prompt(self, env_state):
        # Compose a prompt for the LLM
        profile = f"Agent profile: {self.risk_profile}, wealth: {self.wealth}."
        news = f"Market news: {env_state['news']}"
        options = "Options: buy, sell, save, invest."
        return f"{profile}\n{news}\nWhat will you do? {options}"

    def _rule_based_decision(self, env_state):
        # Fallback: mimic RuleBasedAgent logic
        prices = env_state['prices']
        last_price = self.memory[-1]['price'] if self.memory else prices['GoodA']
        action = 'hold'
        if prices['GoodA'] < last_price:
            action = 'buy'
        elif prices['GoodA'] > last_price:
            action = 'sell'
        if self.risk_profile == 'risk_taker' and random.random() < 0.2:
            action = 'invest'
        self.last_action = action
        return action

class BusinessAgent(BaseAgent):
    """
    Agent that produces goods and sets prices.
    """
    def decide(self, env_state):
        # Simple production/price logic
        action = 'produce'
        if random.random() < 0.5:
            action = 'adjust_price'
        self.last_action = action
        return action

class GovernmentAgent(BaseAgent):
    """
    Special agent that can set policies (UBI, taxes, shocks).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.policies = {}

    def decide(self, env_state):
        # Example: trigger UBI or tax if inequality is high
        gini = env_state.get('gini', 0)
        action = None
        if gini > 0.5:
            action = 'enable_UBI'
        elif gini < 0.3:
            action = 'disable_UBI'
        self.last_action = action
        return action 