import json
from portfolio_management.data.data_loader import DataLoader
from portfolio_management.portfolio.portfolio import Portfolio
from portfolio_management.portfolio.optimizer import PortfolioOptimizer
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation
from portfolio_management.utils.helpers import (
    plot_simulation_results,
    print_simulation_insights,
    display_optimal_weights
)

def main():
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Extract configuration parameters
    tickers = config.get('tickers', [])
    start_date = config.get('start_date')
    end_date = config.get('end_date')
    initial_investment = config.get('initial_investment', 1000)
    num_simulations = config.get('num_simulations', 10000)
    time_horizon = config.get('time_horizon', 252)
    risk_free_rate = config.get('risk_free_rate', 0.0)
    custom_weights = config.get('weights')
    optimization_config = config.get('optimization', {})
    optimize = optimization_config.get('optimize', False)
    balanced = optimization_config.get('balanced', True)

    # Load data
    data_loader = DataLoader()
    stock_data = data_loader.load_data(tickers, start_date, end_date)

    # Create portfolio
    portfolio = Portfolio(stock_data)
    portfolio.calculate_returns()

    # Annualize returns and covariance
    expected_returns = portfolio.returns.mean() * 252
    covariance_matrix = portfolio.returns.cov() * 252

    # Determine weights
    if optimize:
        optimizer = PortfolioOptimizer(
            expected_returns,
            covariance_matrix,
            risk_free_rate=risk_free_rate
        )
        if balanced:
            optimal_weights = optimizer.minimize_volatility(target_return=expected_returns.mean())
            print("\nOptimal Balanced Portfolio Weights:")
        else:
            optimal_weights = optimizer.maximize_sharpe_ratio()
            print("\nOptimal Portfolio Weights to Maximize Sharpe Ratio:")
        display_optimal_weights(stock_data.columns, optimal_weights)
        weights = optimal_weights
    elif custom_weights:
        weights = custom_weights
        print("\nUsing Custom Weights:")
        display_optimal_weights(stock_data.columns, weights)
    else:
        num_assets = len(expected_returns)
        weights = [1.0 / num_assets] * num_assets
        print("\nUsing Equal Weights:")
        display_optimal_weights(stock_data.columns, weights)

    # Perform Monte Carlo Simulation
    simulation = MonteCarloSimulation(portfolio.returns, initial_investment, weights)
    all_cumulative_returns, final_portfolio_values = simulation.run_simulation(
        num_simulations, time_horizon
    )

    # Analyze Results
    print_simulation_insights(final_portfolio_values, initial_investment)

    # Plot results
    plot_simulation_results(all_cumulative_returns, final_portfolio_values)

if __name__ == '__main__':
    main()
