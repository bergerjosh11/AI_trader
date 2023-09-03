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

# Add more utility functions as needed for trading strategies
