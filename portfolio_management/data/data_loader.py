import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

class DataLoader:
    def load_data(self, tickers, start_date, end_date):
        stock_data = {}
        for ticker in tickers:
            try:
                data = web.DataReader(ticker, 'yahoo', start_date, end_date)
                stock_data[ticker] = data['Adj Close']
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame(stock_data)
