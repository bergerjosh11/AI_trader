import os
import joblib
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier  # Replace with your desired model
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Add command-line argument support
parser = argparse.ArgumentParser(description='Train AI Trading Models')
parser.add_argument('--data-file', type=str, required=True, help='Path to historical data CSV file')
parser.add_argument('--output-folder', type=str, required=True, help='Folder to save trained models')
args = parser.parse_args()

# Load historical stock data from the specified CSV file
try:
    data = pd.read_csv(args.data_file)
except FileNotFoundError:
    print(f"Error: The specified data file '{args.data_file}' was not found.")
    exit(1)

# Define features (customize as needed)
features = ['Close', 'Volume']  # Example features, replace with your features

# Define target variable (customize as needed)
target = 'Signal'  # Example target variable, replace with your target

# Initialize a dictionary to store trained models
trained_models = {}

# Split the data into training and testing sets
for symbol in data['Symbol'].unique():
    stock_data = data[data['Symbol'] == symbol].copy()
    X = stock_data[features]
    y = stock_data[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train your machine learning model (replace with your model)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy on the test set (customize as needed)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy for {symbol}: {accuracy:.2f}")

    # Save the trained model to the specified output folder
    model_filename = os.path.join(args.output_folder, f"{symbol}_model.pkl")
    joblib.dump(model, model_filename)
    print(f"Saved model for {symbol} to {model_filename}")

    # Store the trained model in the dictionary
    trained_models[symbol] = model

# You can now use the trained_models dictionary for trading decisions
# Example: trained_models[symbol].predict(new_data)
