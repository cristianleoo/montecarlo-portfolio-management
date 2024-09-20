import matplotlib.pyplot as plt
import numpy as np

def plot_simulation_results(all_cumulative_returns, final_portfolio_values):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot cumulative return paths
    num_simulations_to_plot = 100  # Limit to 100 simulations to avoid clutter
    axes[0].plot(all_cumulative_returns[:, :num_simulations_to_plot])
    axes[0].set_title('Monte Carlo Simulation - Cumulative Returns')
    axes[0].set_xlabel('Time Steps')
    axes[0].set_ylabel('Portfolio Value ($)')
    axes[0].grid(True)

    # Plot histogram of final portfolio values
    axes[1].hist(final_portfolio_values, bins=50, edgecolor='k', alpha=0.65)
    axes[1].set_title('Distribution of Final Portfolio Values')
    axes[1].set_xlabel('Final Portfolio Value ($)')
    axes[1].set_ylabel('Frequency')
    axes[1].axvline(np.mean(final_portfolio_values), color='r', linestyle='dashed', linewidth=2, label=f'Mean: ${np.mean(final_portfolio_values):.2f}')
    axes[1].axvline(np.percentile(final_portfolio_values, 5), color='g', linestyle='dashed', linewidth=2, label=f'VaR 95%: ${np.percentile(final_portfolio_values, 5):.2f}')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

def print_simulation_insights(sim_results, initial_investment):
    mean_return = np.mean(sim_results)
    median_return = np.median(sim_results)
    std_dev = np.std(sim_results)
    percentile_5 = np.percentile(sim_results, 5)
    var_95 = initial_investment - percentile_5  # VaR at 95% confidence
    cvar_95 = initial_investment - np.mean(sim_results[sim_results <= percentile_5])
    prob_loss = np.mean(sim_results < initial_investment) * 100
    sharpe_ratio = (mean_return - initial_investment) / std_dev  # Assuming risk-free rate is 0

    print("\nMonte Carlo Simulation Insights:")
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Expected Final Portfolio Value: ${mean_return:.2f}")
    print(f"Median Final Portfolio Value: ${median_return:.2f}")
    print(f"Standard Deviation of Final Portfolio Value: ${std_dev:.2f}")
    print(f"Value at Risk (VaR 95%): ${var_95:.2f}")
    print(f"Conditional Value at Risk (CVaR 95%): ${cvar_95:.2f}")
    print(f"Probability of Loss: {prob_loss:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")


def display_optimal_weights(tickers, weights):
    print("\nOptimal Portfolio Weights:")
    for ticker, weight in zip(tickers, weights):
        print(f"{ticker}: {weight:.4f}")
