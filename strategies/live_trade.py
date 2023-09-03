# utils.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier  # Replace with your model

# Function to check moving average crossover
def moving_average_cross(data):
    short_ma = data['Close'].rolling(window=50).mean()
    long_ma = data['Close'].rolling(window=200).mean()
    if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
        return 'buy'
    elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
        return 'sell'
    else:
        return 'hold'

# Function to execute trades based on signals and account balance
def execute_trades(api, symbol, action, quantity):
    last_price = api.get_latest_trade(symbol).price
    if action == 'buy':
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='limit',
            limit_price=last_price,
            time_in_force='gtc'
        )
    elif action == 'sell':
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='limit',
            limit_price=last_price,
            time_in_force='gtc'
        )

# Your AI model class should implement the get_signal method
class YourTradingModel:
    def __init__(self):
        # Load your pre-trained machine learning model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)  # Replace with your model

    def get_signal(self, data):
        # Prepare the data for prediction
        features = data[['Close', 'Volume']].values.reshape(1, -1)  # Example features, replace with your features
        prediction = self.model.predict(features)

        # Map the prediction to a trading action
        if prediction == 'buy':
            return 'buy'
        elif prediction == 'sell':
            return 'sell'
        else:
            return 'hold'
