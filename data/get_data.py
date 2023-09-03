import yfinance as yf
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

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

# Fetch historical stock data for each NASDAQ symbol and concatenate it
for symbol in nasdaq_symbols:
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    stock_data['Symbol'] = symbol  # Add a column for the stock symbol
    all_data = pd.concat([all_data, stock_data])

# Save all data to a single CSV file
csv_file_name = 'nasdaq_stock_data.csv'
all_data.to_csv(csv_file_name)

print(f'Saved all NASDAQ-listed historical data to {csv_file_name}')
