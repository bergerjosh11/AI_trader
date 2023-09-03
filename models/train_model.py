import os
import joblib
import alpaca_trade_api as tradeapi  # Replace with your data source API library

class TrainedModels:
    def __init__(self, model_folder='models/saved_models'):
        self.model_folder = model_folder
        self.models = {}  # A dictionary to store loaded models
        self.load_models()

    def load_models(self):
        # Clear any existing models
        self.models = {}

        # Load models from the model folder
        for filename in os.listdir(self.model_folder):
            if filename.endswith("_model.pkl"):
                symbol = filename.split("_")[0]  # Extract the stock symbol
                model_path = os.path.join(self.model_folder, filename)
                model = joblib.load(model_path)
                self.models[symbol] = model

    def get_model(self, symbol):
        if symbol in self.models:
            return self.models[symbol]
        else:
            print(f"Model for {symbol} not found.")
            return None

if __name__ == "__main__":
    # Initialize the data source API (e.g., Alpaca)
    api = tradeapi.REST('YOUR_API_KEY', 'YOUR_API_SECRET', base_url='https://paper-api.alpaca.markets')

    # Fetch a list of stock symbols dynamically from your data source
    stock_symbols = [asset.symbol for asset in api.list_assets() if asset.tradable]

    # Initialize the TrainedModels class to load saved models
    trained_models = TrainedModels()

    for symbol_to_check in stock_symbols:
        # Retrieve the trained model for each symbol
        model_for_symbol = trained_models.get_model(symbol_to_check)

        if model_for_symbol:
            # You can use the loaded model for predictions or other tasks
            print(f"Loaded model for {symbol_to_check}.")
        else:
            print(f"Model for {symbol_to_check} not found.")
