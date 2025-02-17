from fastapi import FastAPI
import yfinance as yf
import requests

from expenses import router as expense_router
from ai_agents import router as ai_router  # Import AI Agent Router

from stable_baselines3 import DQN
import numpy as np

ALPHA_VANTAGE_API_KEY = "08XT6EGZIZ135ROK"

app = FastAPI()
app.include_router(expense_router)

# Include the AI insights router
app.include_router(ai_router)

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    return stock.history(period="1mo").to_dict()


@app.get("/market/{symbol}")
def get_market_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json()

# Load trained model
model = DQN.load("budget_model")

@app.get("/budget/predict")
def predict_budget_action(current_balance: float = 1000):
    obs = np.array([current_balance], dtype=np.float32)
    action, _states = model.predict(obs)

    action_mapping = {0: "Save", 1: "Invest", 2: "Spend"}

    return {"recommended_action": action_mapping[int(action)]}  # ✅ Convert NumPy array to int
