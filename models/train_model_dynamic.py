import requests
import pandas as pd
import alpaca_trade_api as tradeapi
import joblib
from sklearn.ensemble import RandomForestClassifier  # Example model, replace with your model

# Alpaca API credentials
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"  # Use paper trading URL for testing
APCA_API_KEY_ID = "YOUR_API_KEY_ID"
APCA_API_SECRET_KEY = "YOUR_API_SECRET_KEY"

# Initialize Alpaca API
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

# Function to get a list of NASDAQ stock tickers from finnhub.io
def get_nasdaq_tickers():
    finnhub_api_key = "YOUR_FINNHUB_API_KEY"  # Replace with your Finnhub API key
    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&mic=XNAS&token={finnhub_api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        nasdaq_tickers = [item['symbol'] for item in data]
        return nasdaq_tickers
    else:
        print("Failed to fetch NASDAQ tickers from Finnhub API.")
        return []

# Define date range for historical data
start_date = "2020-01-01"
end_date = "2021-01-01"

# Fetch NASDAQ stock tickers
nasdaq_tickers = get_nasdaq_tickers()

# Loop through each NASDAQ ticker
for symbol in nasdaq_tickers:
    try:
        # Fetch historical data from Alpaca for the current ticker
        historical_data = api.get_barset(symbol, "day", start=start_date, end=end_date).df[symbol]

        # Define moving average window periods
        short_window = 50
        long_window = 200

        # Function to create trading signals (example: moving average crossover)
        def generate_signals(data):
            signals = pd.DataFrame(index=data.index)
            signals["Signal"] = 0  # Initialize with 'hold' signals

            # Calculate moving averages
            signals["Short_MA"] = data["close"].rolling(window=short_window).mean()
            signals["Long_MA"] = data["close"].rolling(window=long_window).mean()

            # Create 'buy' signals
            signals.loc[signals["Short_MA"] > signals["Long_MA"], "Signal"] = 1

            # Create 'sell' signals
            signals.loc[signals["Short_MA"] < signals["Long_MA"], "Signal"] = -1

            return signals

        # Generate trading signals based on the historical data
        signals = generate_signals(historical_data)

        # Prepare features (X) and labels (y)
        X
