import argparse
import pandas as pd
import numpy as np

# Add command-line argument support
parser = argparse.ArgumentParser(description='Moving Average Crossover Trading Strategy')
parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., AAPL)')
parser.add_argument('--data-file', type=str, required=True, help='Path to historical data CSV file')
args = parser.parse_args()

# Load historical stock data from the specified CSV file
try:
    data = pd.read_csv(args.data_file)
except FileNotFoundError:
    print(f"Error: The specified data file '{args.data_file}' was not found.")
    exit(1)

# Define moving average window periods
short_window = 50
long_window = 200

# Function to check moving average crossover
def moving_average_cross(data):
    short_ma = data['close'].rolling(window=short_window).mean()
    long_ma = data['close'].rolling(window=long_window).mean()
    if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
        return 'buy'
    elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
        return 'sell'
    else:
        return None

# Function to execute trades based on signals
def execute_trades(symbol, action, quantity):
    if action == 'buy':
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f'Bought {quantity} shares of {symbol} at market price.')
    elif action == 'sell':
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print(f'Sold {quantity} shares of {symbol} at market price.')

while True:
    try:
        # Fetch historical stock data
        data = api.get_barset(symbol, 'day', limit=long_window + 1).df[symbol]
        action = moving_average_cross(data)

        if action == 'buy':
            execute_trades(symbol, 'buy', 1)  # Buy 1 share
        elif action == 'sell':
            execute_trades(symbol, 'sell', 1)  # Sell 1 share

    except Exception as e:
        print(f"An error occurred: {str(e)}")
