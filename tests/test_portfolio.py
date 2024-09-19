import unittest
import pandas as pd
from portfolio_management.portfolio.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):
    def test_calculate_returns(self):
        price_data = pd.DataFrame({
            'AAPL': [150, 152, 154, 153],
            'MSFT': [210, 212, 215, 213]
        })
        portfolio = Portfolio(price_data)
        portfolio.calculate_returns()
        self.assertIsNotNone(portfolio.returns, "Returns should not be None")
        self.assertFalse(portfolio.returns.empty, "Returns DataFrame should not be empty")

if __name__ == '__main__':
    unittest.main()
