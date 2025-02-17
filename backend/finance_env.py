import gymnasium as gym
import numpy as np
from gymnasium import spaces

class FinanceEnv(gym.Env):
    def __init__(self):
        super(FinanceEnv, self).__init__()

        # Budget starts at $1000
        self.balance = 1000

        # Actions: 0 = Save, 1 = Invest, 2 = Spend
        self.action_space = spaces.Discrete(3)

        # Observations: Current balance
        self.observation_space = spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)

    def step(self, action):
        if action == 0:  # Save
            self.balance += 50
        elif action == 1:  # Invest
            self.balance *= np.random.uniform(0.9, 1.2)  # Randomized investment returns
        elif action == 2:  # Spend
            self.balance -= 50

        done = self.balance <= 0  # ✅ Terminate if balance is depleted
        reward = self.balance / 1000  # Reward is proportional to balance

        return np.array([self.balance], dtype=np.float32), reward, done, False, {}

    def reset(self, seed=None, options=None):
        self.balance = 1000
        return np.array([self.balance], dtype=np.float32), {}

    def render(self):
        print(f"Current Balance: ${self.balance}")
