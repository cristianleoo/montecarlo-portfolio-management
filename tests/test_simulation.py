import unittest
import pandas as pd
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation

class TestMonteCarloSimulation(unittest.TestCase):
    def test_run_simulation(self):
        returns = pd.DataFrame({
            'AAPL': [0.01, -0.02, 0.015],
            'MSFT': [-0.005, 0.02, 0.01]
        })
        simulation = MonteCarloSimulation(returns)
        results = simulation.run_simulation(num_simulations=10, time_horizon=5)
        self.assertEqual(results.shape, (5, 10), "Results shape should match time_horizon and num_simulations")

if __name__ == '__main__':
    unittest.main()
