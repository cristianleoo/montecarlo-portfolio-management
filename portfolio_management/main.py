from portfolio_management.data.data_loader import DataLoader
from portfolio_management.portfolio.portfolio import Portfolio
from portfolio_management.portfolio.optimizer import PortfolioOptimizer
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation
from portfolio_management.utils.helpers import plot_simulation_results, print_simulation_insights

def main():
    # Load data
    data_loader = DataLoader()
    stock_data = data_loader.load_data(['AAPL', 'MSFT', 'GOOG'], '2020-01-01', '2023-01-01')

    # Create portfolio
    portfolio = Portfolio(stock_data)
    portfolio.calculate_returns()

    # Annualize returns and covariance
    expected_returns = portfolio.returns.mean() * 252
    covariance_matrix = portfolio.returns.cov() * 252

    # Optimize portfolio
    optimizer = PortfolioOptimizer(expected_returns, covariance_matrix, risk_free_rate=0.02)
    optimal_weights = optimizer.maximize_sharpe_ratio()

    # Display optimal weights
    print("\nOptimal Portfolio Weights to Maximize Sharpe Ratio:")
    for ticker, weight in zip(stock_data.columns, optimal_weights):
        print(f"{ticker}: {weight:.4f}")

    # Perform Monte Carlo Simulation with optimal weights
    initial_investment = 1000
    simulation = MonteCarloSimulation(portfolio.returns, initial_investment, weights=optimal_weights)
    all_cumulative_returns, final_portfolio_values = simulation.run_simulation(10000, 252)

    # Analyze Results
    print_simulation_insights(final_portfolio_values, initial_investment)

    # Plot results
    plot_simulation_results(all_cumulative_returns, final_portfolio_values)

if __name__ == '__main__':
    main()
