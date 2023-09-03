import pandas as pd
from strategies.utils import moving_average_cross
from models.trained_models import TrainedModels  # Import the TrainedModels class

# Load historical stock data
data = pd.read_csv('historical_stock_data.csv')

# Initialize the TrainedModels class to load saved models
trained_models = TrainedModels()

# Define backtesting logic
def backtest_strategy(data, trained_models):
    signals = []
    for symbol in data['Symbol'].unique():
        stock_data = data[data['Symbol'] == symbol].copy()

        # Retrieve the trained model for the symbol
        model_for_symbol = trained_models.get_model(symbol)

        if model_for_symbol:
            # Generate trading signals using the retrieved model
            action = moving_average_cross(stock_data, model_for_symbol)  # You may need to modify moving_average_cross to accept the model
            signals.append({'symbol': symbol, 'action': action})
        else:
            print(f"Model for {symbol} not found.")

    return pd.DataFrame(signals)

# Backtest the strategy
backtest_results = backtest_strategy(data, trained_models)

# Print or analyze backtest results
print(backtest_results)
