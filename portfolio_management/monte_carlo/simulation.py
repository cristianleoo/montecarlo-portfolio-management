import numpy as np

class MonteCarloSimulation:
    def __init__(self, returns, initial_investment=1, weights=None):
        self.returns = returns
        self.mean = returns.mean()
        self.covariance = returns.cov()
        self.initial_investment = initial_investment
        num_assets = len(self.mean)
        if weights is None:
            self.weights = np.ones(num_assets) / num_assets
        else:
            self.weights = np.array(weights)

    def run_simulation(self, num_simulations, time_horizon):
        all_cumulative_returns = np.zeros((time_horizon, num_simulations))
        final_portfolio_values = np.zeros(num_simulations)

        for sim in range(num_simulations):
            simulated_returns = np.random.multivariate_normal(
                self.mean, self.covariance, time_horizon
            )
            cumulative_returns = np.cumprod(1 + simulated_returns, axis=0)
            portfolio_cumulative_returns = cumulative_returns.dot(self.weights)
            all_cumulative_returns[:, sim] = portfolio_cumulative_returns * self.initial_investment
            final_portfolio_values[sim] = portfolio_cumulative_returns[-1] * self.initial_investment
        return all_cumulative_returns, final_portfolio_values
