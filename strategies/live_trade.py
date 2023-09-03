import pandas as pd
import alpaca_trade_api as tradeapi
from models.trained_models import TrainedModels
from strategies.utils import execute_trades
from portfolio_optimization.portfolio_optimization import optimize_portfolio_weights

# Initialize Alpaca API with your credentials
api = tradeapi.REST('YOUR_API_KEY', 'YOUR_API_SECRET', base_url='https://paper-api.alpaca.markets')

class YourTradingModel:
    def __init__(self, model_folder='models/saved_models'):
        self.model_folder = model_folder
        self.load_most_recent_model()
        self.trained_models = TrainedModels(self.model_folder)

    def load_most_recent_model(self):
        self.trained_models = TrainedModels(self.model_folder)

    def get_signal(self, symbol):
        stock_data = api.get_barset(symbol, 'day', limit=200).df[symbol]
        signal = self.trained_models.get_model(symbol).predict(stock_data)
        return signal

def determine_symbols_to_trade():
    assets = api.list_assets()
    symbols_to_trade = []

    for asset in assets:
        if asset.tradable:
            model = YourTradingModel()
            signal = model.get_signal(asset.symbol)
            if signal == 'buy':
                symbols_to_trade.append(asset.symbol)

    return symbols_to_trade

def calculate_trade_quantity(account_balance, last_price, weight):
    # Calculate the trade quantity based on the portfolio weight and available capital
    max_allocation = account_balance * 0.1  # Allocate 10% of the account balance
    max_quantity = max_allocation / last_price
    return int(max_quantity * weight)  # Adjust quantity based on weight

if __name__ == "__main__":
    while True:
        try:
            symbols_to_trade = determine_symbols_to_trade()
            if symbols_to_trade:
                for symbol_to_trade in symbols_to_trade:
                    stock_data = api.get_barset(symbol_to_trade, 'day', limit=1).df[symbol_to_trade]
                    last_price = stock_data['close'].iloc[0]
                    account = api.get_account()
                    account_balance = float(account.cash)

                    # Use portfolio optimization to get the optimal weights
                    optimal_weights = optimize_portfolio_weights(symbol_to_trade)

                    # Calculate the trade quantity based on the portfolio weight
                    weight = optimal_weights.get(symbol_to_trade, 0.0)
                    quantity_to_trade = calculate_trade_quantity(account_balance, last_price, weight)

                    model = YourTradingModel()
                    signal = model.get_signal(symbol_to_trade)

                    if signal == 'buy':
                        execute_trades(api, symbol_to_trade, 'buy', quantity_to_trade)
                    elif signal == 'sell':
                        execute_trades(api, symbol_to_trade, 'sell', quantity_to_trade)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
