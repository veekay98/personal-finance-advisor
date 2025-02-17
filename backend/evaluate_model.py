from stable_baselines3 import DQN
from finance_env import FinanceEnv

# Load the trained model
model = DQN.load("budget_model")

# Initialize environment
env = FinanceEnv()

obs, _ = env.reset()
done = False
step_count = 0  # ✅ Add step counter

while not done and step_count < 100:  # ✅ Prevent infinite loops
    action, _states = model.predict(obs)
    obs, reward, done, truncated, _ = env.step(action)
    env.render()
    step_count += 1  # ✅ Increase step count

print("✅ Evaluation completed in", step_count, "steps")
