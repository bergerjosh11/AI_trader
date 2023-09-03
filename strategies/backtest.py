# backtest.py
import pandas as pd
import joblib
from strategies.utils import moving_average_cross

# Load historical stock data
data = pd.read_csv('historical_stock_data.csv')

# Load the trained machine learning model
model = joblib.load('saved_models/model.pkl')

# Define backtesting logic
def backtest_strategy(data, model):
    signals = []
    for symbol in data['Symbol'].unique():
        stock_data = data[data['Symbol'] == symbol].copy()
        action = moving_average_cross(stock_data)
        signals.append({'symbol': symbol, 'action': action})
    return pd.DataFrame(signals)

# Backtest the strategy
backtest_results = backtest_strategy(data, model)

# Print or analyze backtest results
print(backtest_results)
