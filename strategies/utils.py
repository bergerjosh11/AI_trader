import pandas as pd

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    """
    Calculate Simple Moving Average (SMA) for a given DataFrame column.
    
    Parameters:
        - data: DataFrame containing price data
        - window: Window size for the moving average
    
    Returns:
        - Series containing the SMA values
    """
    return data['Close'].rolling(window=window).mean()

# Function to generate buy/sell signals based on moving average crossovers
def moving_average_cross(data, short_window, long_window):
    """
    Generate buy/sell signals based on moving average crossovers.
    
    Parameters:
        - data: DataFrame containing price data
        - short_window: Short-term moving average window
        - long_window: Long-term moving average window
    
    Returns:
        - Series with buy/sell/hold signals
    """
    short_ma = calculate_sma(data, short_window)
    long_ma = calculate_sma(data, long_window)
    
    signals = []
    position = 'out'  # 'out' indicates no position
    
    for i in range(len(data)):
        if short_ma.iloc[i] > long_ma.iloc[i] and position == 'out':
            signals.append('buy')
            position = 'in'  # Enter long position
        elif short_ma.iloc[i] < long_ma.iloc[i] and position == 'in':
            signals.append('sell')
            position = 'out'  # Exit long position
        else:
            signals.append('hold')
    
    return pd.Series(signals, index=data.index)

def calculate_rsi(data, window=14):
    """
    Calculate Relative Strength Index (RSI) for a given DataFrame column.
    
    Parameters:
        - data: DataFrame containing price data
        - window: Window size for RSI calculation
    
    Returns:
        - Series containing RSI values
    """
    price_diff = data['Close'].diff(1)
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calculate Bollinger Bands for a given DataFrame column.
    
    Parameters:
        - data: DataFrame containing price data
        - window: Window size for moving average
        - num_std_dev: Number of standard deviations for the bands
    
    Returns:
        - DataFrame with 'Upper Bollinger Band' and 'Lower Bollinger Band' columns
    """
    sma = calculate_sma(data, window)
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = sma + (num_std_dev * rolling_std)
    lower_band = sma - (num_std_dev * rolling_std)
    bollinger_bands = pd.DataFrame({'Upper Bollinger Band': upper_band, 'Lower Bollinger Band': lower_band})
    return bollinger_bands

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate Moving Average Convergence Divergence (MACD) for a given DataFrame column.
    
    Parameters:
        - data: DataFrame containing price data
        - short_window: Short-term moving average window
        - long_window: Long-term moving average window
        - signal_window: Signal line smoothing window
    
    Returns:
        - DataFrame with 'MACD' and 'Signal Line' columns
    """
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()
    macd_data = pd.DataFrame({'MACD': macd, 'Signal Line': signal_line})
    return macd_data

# Add more utility functions as needed for trading strategies
