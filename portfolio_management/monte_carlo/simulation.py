import numpy as np

class MonteCarloSimulation:
    def __init__(self, returns):
        self.returns = returns
        self.mean = returns.mean()
        self.covariance = returns.cov()

    def run_simulation(self, num_simulations, time_horizon):
        num_assets = len(self.mean)
        results = np.zeros((time_horizon, num_simulations))

        for sim in range(num_simulations):
            simulated_returns = np.random.multivariate_normal(
                self.mean, self.covariance, time_horizon)
            cumulative_returns = np.cumprod(1 + simulated_returns, axis=0)
            results[:, sim] = cumulative_returns[-1, :]

        return results
