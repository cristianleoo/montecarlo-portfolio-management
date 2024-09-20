import unittest
import pandas as pd
import numpy as np
from portfolio_management.portfolio.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):
    def test_calculate_returns(self):
        dates = pd.date_range('2020-01-01', periods=5)
        data = pd.DataFrame({
            'AAPL': [100, 101, 102, 103, 104],
            'MSFT': [200, 201, 202, 203, 204]
        }, index=dates)
        portfolio = Portfolio(data)
        portfolio.calculate_returns()
        self.assertIsNotNone(portfolio.returns, "Returns should not be None")
        self.assertEqual(portfolio.returns.shape, (4, 2), "Returns should have correct shape")

if __name__ == '__main__':
    unittest.main()
