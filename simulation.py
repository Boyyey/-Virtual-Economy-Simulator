"""
Simulation engine for the Virtual Economy Simulator.
Encapsulates all logic for running, pausing, resetting, and retrieving results.
"""
import config
from agents import BaseAgent, RuleBasedAgent, LLMAgent, BusinessAgent, GovernmentAgent
from environment import Economy
from llm_interface import LLMInterface
from utils import set_random_seed

class Simulation:
    """
    Encapsulates the simulation state and logic for interactive use.
    """
    def __init__(self, params=None):
        self.params = params or config
        self.reset()

    def reset(self):
        set_random_seed(self.params.RANDOM_SEED)
        self.round_num = 0
        self.agents = []
        self.llm_interface = LLMInterface() if getattr(self.params, 'USE_LLM', False) else None
        for i in range(getattr(self.params, 'NUM_AGENTS', 100)):
            risk = self.params.RISK_PROFILES[i % len(self.params.RISK_PROFILES)]
            if getattr(self.params, 'USE_LLM', False):
                agent = LLMAgent(i, self.params.INITIAL_WEALTH, risk, llm_interface=self.llm_interface)
            else:
                agent = RuleBasedAgent(i, self.params.INITIAL_WEALTH, risk)
            self.agents.append(agent)
        self.businesses = [BusinessAgent(f"B{i}", self.params.INITIAL_BUSINESS_WEALTH, 'neutral') for i in range(getattr(self.params, 'NUM_BUSINESSES', 5))]
        self.government = GovernmentAgent("GOV", 0, 'neutral')
        self.env = Economy(self.agents, self.businesses, self.government, self.params)
        self.running = False
        self.done = False

    def step(self):
        if not self.done:
            self.env.step()
            self.round_num += 1
            if self.round_num >= getattr(self.params, 'NUM_ROUNDS', 1000):
                self.done = True
        return self.get_state()

    def run(self, max_steps=None):
        steps = max_steps or getattr(self.params, 'NUM_ROUNDS', 1000)
        for _ in range(steps):
            if self.done or not self.running:
                break
            self.step()
        return self.get_state()

    def get_state(self):
        return {
            'round': self.round_num,
            'agents': self.agents,
            'businesses': self.businesses,
            'government': self.government,
            'market': self.env.market,
            'gini_history': self.env.gini_history,
            'done': self.done,
        }

    def set_running(self, running=True):
        self.running = running

    def set_params(self, params):
        self.params = params
        self.reset() 