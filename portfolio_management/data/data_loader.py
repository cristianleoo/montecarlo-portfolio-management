import pandas as pd
import yfinance as yf

class DataLoader:
    def load_data(self, tickers, start_date, end_date):
        stock_data = {}
        for ticker in tickers:
            try:
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not data.empty:
                    stock_data[ticker] = data['Adj Close']
                else:
                    print(f"No data found for {ticker}")
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame(stock_data)
