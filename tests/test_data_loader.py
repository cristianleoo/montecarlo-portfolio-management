import unittest
from portfolio_management.data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data_loader = DataLoader()
        tickers = ['AAPL', 'MSFT']
        start_date = '2020-01-01'
        end_date = '2020-12-31'
        data = data_loader.load_data(tickers, start_date, end_date)
        self.assertFalse(data.empty, "Data should not be empty")
        self.assertTrue(all(ticker in data.columns for ticker in tickers), "All tickers should be in the data")

if __name__ == '__main__':
    unittest.main()
