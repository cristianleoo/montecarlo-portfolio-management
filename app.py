import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from portfolio_management.data.data_loader import DataLoader
from portfolio_management.portfolio.portfolio import Portfolio
from portfolio_management.portfolio.optimizer import PortfolioOptimizer
from portfolio_management.monte_carlo.simulation import MonteCarloSimulation
from portfolio_management.utils.helpers import (
    plot_interactive_simulation_results,
    get_simulation_insights,
    display_optimal_weights
)

def main():
    st.title('Portfolio Management with Monte Carlo Simulation')

    st.write("""
    Welcome to the Portfolio Management application. Input your investment preferences below and run a Monte Carlo simulation to forecast potential portfolio performance.
    """)

    # Load list of tickers for autocomplete suggestions
    @st.cache_data
    def load_ticker_list():
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(sp500_url)
        sp500_tickers = tables[0]['Symbol'].tolist()
        return sp500_tickers

    ticker_list = load_ticker_list()

    # Input: Stock Tickers
    st.header('1. Select Stocks and Date Range')
    st.write("Start typing a stock ticker and select from the suggestions.")
    selected_tickers = st.multiselect(
        'Select Stock Tickers:',
        options=ticker_list,
        help='Type to search and select stock tickers.'
    )

    if not selected_tickers:
        st.info('Please select at least one stock ticker to proceed.')
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', value=pd.to_datetime('2020-01-01'), help='The start date for historical data.')
    with col2:
        end_date = st.date_input('End Date', value=pd.to_datetime(datetime.today() - relativedelta(days=1)), help='The end date for historical data.')

    tickers = selected_tickers

    # Input: Investment Options
    st.header('2. Investment Preferences')
    risk_free_rate = st.number_input(
        'Risk-Free Rate:',
        value=0.02,
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        help='The risk-free rate used for calculations, typically a treasury bond yield.'
    )
    investment_option = st.radio(
        'Choose Investment Input Option:',
        ('Use Weights and Initial Investment', 'Use Dollar Amounts per Stock'),
        help='Select how you want to input your investment allocations.'
    )

    weights = None
    initial_investment = 1000.0  # Default value

    if investment_option == 'Use Weights and Initial Investment':
        st.subheader('Weights and Initial Investment')
        st.write('Input weights for each stock or choose to optimize the portfolio.')

        # Optimization Options
        optimize = st.checkbox('Optimize Portfolio', value=False, help='Select to automatically calculate optimal weights for your portfolio.')
        if optimize:
            optimization_choice = st.selectbox(
                'Optimization Strategy',
                ('Maximize Sharpe Ratio', 'Balanced Portfolio'),
                help='Choose an optimization strategy.'
            )
            balanced = (optimization_choice == 'Balanced Portfolio')
            custom_weights = None
        else:
            balanced = False
            # Create editable table for weights
            st.write("Edit the weights for each stock below. The weights should sum to 1.0.")
            default_weight = 1.0 / len(tickers)
            weights_df = pd.DataFrame({
                'Ticker': tickers,
                'Weight': [default_weight] * len(tickers)
            })
            st.info('You can edit the weights in the table below. The weights should sum to 1.0.')
            weights_df = st.data_editor(
                weights_df,
                num_rows="dynamic",
                use_container_width=True,
                key='weights_editor',
            )
            # Validate weights
            total_weight = weights_df['Weight'].sum()
            if abs(total_weight - 1.0) > 1e-6:
                st.error(f'Total weights must sum to 1. Currently summing to {total_weight:.4f}')
                st.stop()
            weights = weights_df['Weight'].tolist()

        initial_investment = st.number_input(
            'Initial Investment ($):',
            value=1000.0,
            min_value=0.0,
            help='Total amount you plan to invest.'
        )

    else:
        # Use Dollar Amounts per Stock
        st.subheader('Dollar Amounts per Stock')
        st.write('Input the dollar amount you wish to invest in each stock.')
        amounts = []
        for ticker in tickers:
            amount = st.number_input(
                f'Amount for {ticker} ($):',
                value=100.0,
                min_value=0.0,
                help=f'Amount to invest in {ticker}.'
            )
            amounts.append(amount)
        total_investment = sum(amounts)
        if total_investment == 0:
            st.error('Total investment cannot be zero.')
            st.stop()
        weights = [amount / total_investment for amount in amounts]
        initial_investment = total_investment
        optimize = False  # Disable optimization when dollar amounts are provided

    # Input: Simulation Parameters
    st.header('3. Simulation Parameters')
    col1, col2 = st.columns(2)
    with col1:
        num_simulations = st.number_input(
            'Number of Simulations:',
            value=10000,
            min_value=100,
            step=100,
            help='Number of Monte Carlo simulations to run.'
        )
    with col2:
        time_horizon = st.number_input(
            'Time Horizon (Days):',
            value=252,
            min_value=1,
            step=1,
            help='Investment period in days (e.g., 252 for one year).'
        )

    # Button to Run Simulation
    run_simulation = st.button('Run Monte Carlo Simulation')
    if run_simulation:
        # Load data
        data_loader = DataLoader()
        stock_data = data_loader.load_data(tickers, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if stock_data.empty:
            st.error('Failed to load stock data. Please check the tickers and date range.')
            return

        # Create portfolio
        portfolio = Portfolio(stock_data)
        portfolio.calculate_returns()

        # Annualize returns and covariance
        expected_returns = portfolio.returns.mean() * 252
        covariance_matrix = portfolio.returns.cov() * 252

        # Determine weights
        if investment_option == 'Use Weights and Initial Investment':
            if optimize:
                optimizer = PortfolioOptimizer(
                    expected_returns,
                    covariance_matrix,
                    risk_free_rate=risk_free_rate
                )
                if balanced:
                    weights = optimizer.minimize_volatility(target_return=expected_returns.mean())
                    st.subheader('Optimal Balanced Portfolio Weights:')
                else:
                    weights = optimizer.maximize_sharpe_ratio()
                    st.subheader('Optimal Portfolio Weights to Maximize Sharpe Ratio:')
                display_optimal_weights(tickers, weights, streamlit_display=True)
            else:
                st.subheader('Using Custom Weights:')
                display_optimal_weights(tickers, weights, streamlit_display=True)
        else:
            # Weights have been calculated from dollar amounts
            st.subheader('Calculated Weights from Dollar Amounts:')
            display_optimal_weights(tickers, weights, streamlit_display=True)
            st.write(f"**Total Investment Amount:** ${initial_investment:.2f}")

        # Perform Monte Carlo Simulation
        simulation = MonteCarloSimulation(portfolio.returns, initial_investment, weights)
        all_cumulative_returns, final_portfolio_values = simulation.run_simulation(
            int(num_simulations), int(time_horizon)
        )

        # Analyze Results
        st.header('4. Simulation Results')
        st.subheader('Monte Carlo Simulation Insights:')
        insights = get_simulation_insights(final_portfolio_values, initial_investment)
        for key, value in insights.items():
            st.write(f"**{key}:** {value}")

        # Plot results
        st.subheader('Interactive Plots')
        plot_interactive_simulation_results(all_cumulative_returns, final_portfolio_values, end_date)

if __name__ == '__main__':
    main()
