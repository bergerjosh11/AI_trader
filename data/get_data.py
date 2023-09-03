import yfinance as yf
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import os

# Fetch the list of all NASDAQ-listed symbols
nasdaq_symbols_url = "https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq"
response = requests.get(nasdaq_symbols_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the symbols from the web page
nasdaq_symbols = [a.text.strip() for a in soup.find_all('a', class_='row-link')]

# Define the date range
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5*365)  # 5 years of data

# Initialize a DataFrame to store all historical data
all_data = pd.DataFrame()

# Create a directory to save historical data
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Fetch historical stock data for each NASDAQ symbol and save it
for symbol in nasdaq_symbols:
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        stock_data['Symbol'] = symbol  # Add a column for the stock symbol
        file_name = os.path.join(data_dir, f'{symbol}_historical_data.csv')
        stock_data.to_csv(file_name)
        print(f'Saved historical data for {symbol} to {file_name}')
    except Exception as e:
        print(f'Error fetching data for {symbol}: {str(e)}')

print(f'Saved all NASDAQ-listed historical data to {data_dir}')
