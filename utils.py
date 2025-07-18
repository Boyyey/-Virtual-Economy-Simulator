"""
Utility functions for the Virtual Economy Simulator.
"""
import random
import numpy as np

def set_random_seed(seed):
    """
    Set random seed for reproducibility.
    """
    random.seed(seed)
    np.random.seed(seed) 