import unittest
import numpy as np
from portfolio_management.portfolio.optimizer import PortfolioOptimizer

class TestPortfolioOptimizer(unittest.TestCase):
    def test_maximize_sharpe_ratio(self):
        expected_returns = np.array([0.1, 0.12])
        covariance_matrix = np.array([[0.04, 0.006], [0.006, 0.09]])
        optimizer = PortfolioOptimizer(expected_returns, covariance_matrix)
        weights = optimizer.maximize_sharpe_ratio()
        self.assertAlmostEqual(weights.sum(), 1.0, places=5, msg="Weights should sum to 1")
        self.assertTrue(all(0 <= w <= 1 for w in weights), "Weights should be between 0 and 1")

if __name__ == '__main__':
    unittest.main()
