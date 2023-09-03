import argparse
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
from trained_models import TrainedModels  # Import the TrainedModels class from trained_models.py
from portfolio_optimization import optimize_portfolio  # Import the portfolio optimization script

# Add command-line argument support
parser = argparse.ArgumentParser(description='AI Trading Strategy')
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

# Initialize the TrainedModels class to load saved models
trained_models = TrainedModels()

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

# Function to assess market risk based on volatility
def assess_dynamic_risk(data):
    # Calculate historical volatility
    historical_volatility = data['Close'].pct_change().rolling(window=30).std() * np.sqrt(252)

    # Determine risk level based on volatility
    if historical_volatility.iloc[-1] > 0.2:
        return 'high'
    elif historical_volatility.iloc[-1] > 0.1:
        return 'medium'
    else:
        return 'low'

# Retrieve the trained model for the specified stock symbol
model_for_symbol = trained_models.get_model(args.symbol)

if model_for_symbol:
    # Main trading loop
    while True:
        try:
            # Fetch historical stock data
            stock_data = data[data['Symbol'] == args.symbol].copy()
            action = moving_average_cross(stock_data)

            # Assess market risk based on volatility
            risk_level = assess_dynamic_risk(stock_data)

            # Get account balance (or use your real account balance)
            account = api.get_account()
            balance = float(account.cash)

            if action == 'buy':
                # Get the optimized portfolio weights
                stock_symbols = [args.symbol]  # List of symbols to optimize (only one in this case)
                expected_returns = [...]  # List of expected returns for each asset
                covariance_matrix = [...]  # Covariance matrix of asset returns
                risk_tolerance = 0.1  # Adjust this based on your risk tolerance

                # Call the portfolio optimization function to get weights
                portfolio_weights = optimize_portfolio(expected_returns, covariance_matrix, risk_tolerance)

                # Calculate the quantity to buy based on weights and balance
                max_buy_quantity = int(portfolio_weights[args.symbol] * balance / stock_data['Close'].iloc[-1])
                if max_buy_quantity > 0:
                    execute_trades(api, args.symbol, 'buy', max_buy_quantity, balance)

            elif action == 'sell':
                # Get the optimized portfolio weights
                stock_symbols = [args.symbol]  # List of symbols to optimize (only one in this case)
                expected_returns = [...]  # List of expected returns for each asset
                covariance_matrix = [...]  # Covariance matrix of asset returns
                risk_tolerance = 0.1  # Adjust this based on your risk tolerance

                # Call the portfolio optimization function to get weights
                portfolio_weights = optimize_portfolio(expected_returns, covariance_matrix, risk_tolerance)

                # Calculate the quantity to sell based on weights and balance
                max_sell_quantity = int(portfolio_weights[args.symbol] * balance / stock_data['Close'].iloc[-1])
                if max_sell_quantity > 0:
                    execute_trades(api, args.symbol, 'sell', max_sell_quantity, balance)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
else:
    print(f"Model for {args.symbol} not found.")
