import numpy as np
from scipy.optimize import minimize

class PortfolioOptimizer:
    def __init__(self, expected_returns, covariance_matrix, risk_free_rate=0.0):
        self.expected_returns = expected_returns
        self.covariance_matrix = covariance_matrix
        self.risk_free_rate = risk_free_rate

    def maximize_sharpe_ratio(self):
        num_assets = len(self.expected_returns)
        args = (self.expected_returns, self.covariance_matrix, self.risk_free_rate)
        constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
        bounds = tuple((0, 1) for _ in range(num_assets))

        result = minimize(
            self._neg_sharpe_ratio,
            x0=num_assets * [1.0 / num_assets],
            args=args,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        return result.x

    def minimize_volatility(self, target_return):
        num_assets = len(self.expected_returns)
        args = (self.covariance_matrix,)
        constraints = (
            {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
            {'type': 'eq', 'fun': lambda weights: np.dot(weights, self.expected_returns) - target_return}
        )
        bounds = tuple((0, 1) for _ in range(num_assets))

        result = minimize(
            self._portfolio_volatility,
            x0=num_assets * [1.0 / num_assets],
            args=args,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        return result.x

    @staticmethod
    def _neg_sharpe_ratio(weights, expected_returns, covariance_matrix, risk_free_rate):
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        return -sharpe_ratio  # Negative because we maximize Sharpe Ratio

    @staticmethod
    def _portfolio_volatility(weights, covariance_matrix):
        return np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
