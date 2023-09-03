import argparse
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import joblib
from sklearn.ensemble import RandomForestClassifier  # Example model, replace with your model

# Add command-line argument support
parser = argparse.ArgumentParser(description='Moving Average Crossover Trading Strategy')
parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., AAPL)')
parser.add_argument('--data-file', type=str, required=True, help='Path to historical data CSV file')
parser.add_argument('--api-key', type=str, required=True, help='Your Alpaca API Key')
parser.add_argument('--api-secret', type=str, required=True, help='Your Alpaca API Secret')
args = parser.parse_args()

# Initialize Alpaca API with your credentials
api = tradeapi.REST(args.api_key, args.api_secret, base_url='https://paper-api.alpaca.markets')  # Use paper trading URL for testing

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
    short_ma = data['Close'].rolling(window=short_window).mean()
    long_ma = data['Close'].rolling(window=long_window).mean()
    if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
        return 'buy'
    elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
        return 'sell'
    else:
        return 'hold'

# Function to execute trades based on signals and account balance
def execute_trades(api, symbol, action, quantity, balance):
    last_price = api.get_latest_trade(symbol).price
    if action == 'buy':
        if balance >= last_price * quantity:
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='limit',
                limit_price=last_price,
                time_in_force='gtc'
            )
            print(f'Bought {quantity} shares of {symbol} at {last_price} per share.')
            balance -= last_price * quantity
        else:
            print(f'Insufficient funds to buy {quantity} shares of {symbol}.')
    elif action == 'sell':
        positions = api.list_positions()
        for position in positions:
            if position.symbol == symbol and position.qty >= quantity:
                api.submit_order(
                    symbol=symbol,
                    qty=quantity,
                    side='sell',
                    type='limit',
                    limit_price=last_price,
                    time_in_force='gtc'
                )
                print(f'Sold {quantity} shares of {symbol} at {last_price} per share.')
                balance += last_price * quantity
                break
        else:
            print(f'No {symbol} position to sell or insufficient shares.')

# Train a simple machine learning model (Example: Random Forest Classifier, replace with your model)
def train_machine_learning_model(data):
    features = data[['Close', 'Volume']]  # Use relevant features from your data
    labels = data['Signal']  # Assuming you have a 'Signal' column with 'buy', 'sell', or 'hold' labels
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)
    return model

# Train your machine learning model
model = train_machine_learning_model(data)

# Save the trained model to the 'saved_models' folder
model_filename = f'saved_models/{args.symbol}_model.pkl'
joblib.dump(model, model_filename)
print(f'Saved the trained model to {model_filename}')

# Initialize a starting balance for simulation (or connect to your real account)
balance = 100000  # Starting balance in dollars
shares_held = 0   # Number of shares currently held

# Main trading loop
while True:
    try:
        # Fetch historical stock data
        stock_data = data[data['Symbol'] == args.symbol].copy()
        action = moving_average_cross(stock_data)

        # Get account balance (or use your real account balance)
        account = api.get_account()
        balance = float(account.cash)

        if action == 'buy':
            # Define the quantity to buy based on your balance
            # For example, you can allocate 50% of your balance to this trade
            max_buy_quantity = int(balance * 0.5 / stock_data['Close'].iloc[-1])
            if max_buy_quantity > 0:
                execute_trades(api, args.symbol, 'buy', max_buy_quantity, balance)
        elif action == 'sell':
            # Define the quantity to sell based on your current position size
            # For example, you can sell half of your current position
            max_sell_quantity = int(balance * 0.5 / stock_data['Close'].iloc[-1])
            if max_sell_quantity > 0:
                execute_trades(api, args.symbol, 'sell', max_sell_quantity, balance)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
