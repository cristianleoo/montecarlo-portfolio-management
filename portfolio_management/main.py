import sys
from portfolio_management.data.data_loader import DataLoader
from portfolio_management.portfolio.portfolio import Portfolio
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation
from portfolio_management.utils.helpers import plot_simulation_results

def main():
    # Load data
    data_loader = DataLoader()
    stock_data = data_loader.load_data(['AAPL', 'MSFT', 'GOOG'], '2020-01-01', '2023-01-01')

    # Create portfolio
    portfolio = Portfolio(stock_data)
    portfolio.calculate_returns()

    # Perform Monte Carlo Simulation
    simulation = MonteCarloSimulation(portfolio.returns)
    sim_results = simulation.run_simulation(num_simulations=1000, time_horizon=252)

    # Plot results
    plot_simulation_results(sim_results)

if __name__ == '__main__':
    main()
