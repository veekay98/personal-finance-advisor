import yfinance as yf
from langchain_community.llms import OpenAI
from langchain.agents import initialize_agent
from dotenv import load_dotenv
import os
from fastapi import APIRouter
from langchain.agents import AgentType
from langchain.tools import Tool
from langchain_experimental.tools import PythonREPLTool  # Corrected Import
from langchain_community.llms import OpenAI
from langchain.agents import initialize_agent, AgentType

# Initialize the Python REPL Tool
python_repl_tool = PythonREPLTool()

# List of tools for the agent
tools = [python_repl_tool]  # Adding at least one tool

router = APIRouter()

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key!")

llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

# Manually fetch stock data
def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    return stock.history(period="1mo").to_dict()

# Create agent (without using `load_tools`)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def get_financial_insights():
    return {"advice": agent.run("Analyze my spending and recommend better saving strategies.")}

@router.get("/insights")
def insights():
    return get_financial_insights()
