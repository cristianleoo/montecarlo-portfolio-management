import unittest
import pandas as pd
import numpy as np
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation

class TestMonteCarloSimulation(unittest.TestCase):
    def test_run_simulation(self):
        dates = pd.date_range('2020-01-01', periods=5)
        returns = pd.DataFrame({
            'AAPL': np.random.normal(0.001, 0.02, size=5),
            'MSFT': np.random.normal(0.001, 0.02, size=5)
        }, index=dates)
        simulation = MonteCarloSimulation(returns)
        all_cumulative_returns, final_portfolio_values = simulation.run_simulation(num_simulations=10, time_horizon=5)
        self.assertEqual(all_cumulative_returns.shape, (5, 10), "Cumulative returns should have correct shape")
        self.assertEqual(final_portfolio_values.shape, (10,), "Final portfolio values should have correct shape")

if __name__ == '__main__':
    unittest.main()
