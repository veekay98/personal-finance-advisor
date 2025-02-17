import gymnasium as gym
import numpy as np
from stable_baselines3 import DQN
from finance_env import FinanceEnv

# Initialize the environment
env = FinanceEnv()

# Create DQN model
model = DQN("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save trained model
model.save("budget_model")
