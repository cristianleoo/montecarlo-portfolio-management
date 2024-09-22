import pandas as pd
import yfinance as yf
from typing import List, Dict, Union

class DataLoader:
    def load_data(self, tickers: List[str], start_date: Union[str, pd.Timestamp], end_date: Union[str, pd.Timestamp]) -> pd.DataFrame:
        stock_data: Dict[str, pd.Series] = {}
        for ticker in tickers:
            try:
                data: pd.DataFrame = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not data.empty:
                    stock_data[ticker] = data['Adj Close']
                else:
                    print(f"No data found for {ticker}")
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame(stock_data)

if __name__ == "__main__":
    data_loader: DataLoader = DataLoader()
    tickers: List[str] = ['AAPL', 'MSFT', 'GOOG']
    start_date: str = '2020-01-01'
    end_date: str = '2023-01-01'
    stock_data: pd.DataFrame = data_loader.load_data(tickers, start_date, end_date)
    print(stock_data.head())