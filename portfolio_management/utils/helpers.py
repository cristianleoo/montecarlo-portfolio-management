import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dateutil.relativedelta import relativedelta

def convert_time_steps_to_dates(start_date_str, time_steps):
    # Convert the start date string to a datetime object
    start_date = pd.to_datetime(start_date_str)
    
    # Calculate the actual dates
    actual_dates = [pd.to_datetime(start_date + relativedelta(days=int(step))).strftime('%Y-%m-%d') for step in time_steps]
    
    return actual_dates

def plot_interactive_simulation_results(all_cumulative_returns, final_portfolio_values, start_date):
    # Plot cumulative return paths
    num_simulations_to_plot = min(100, all_cumulative_returns.shape[1])  # Limit to avoid clutter
    time_steps = np.arange(all_cumulative_returns.shape[0])

    fig = make_subplots(rows=1, cols=2, subplot_titles=(
        'Monte Carlo Simulation - Cumulative Returns',
        'Distribution of Final Portfolio Values'
    ))

    # Cumulative Returns Plot
    for i in range(num_simulations_to_plot):
        fig.add_trace(
            go.Scatter(
                x=convert_time_steps_to_dates(start_date, time_steps),
                y=all_cumulative_returns[:, i],
                mode='lines',
                line=dict(width=1),
                showlegend=False
            ),
            row=1,
            col=1
        )
    fig.update_xaxes(title_text='Time Steps', row=1, col=1)
    fig.update_yaxes(title_text='Portfolio Value ($)', row=1, col=1)

    # Histogram of Final Portfolio Values
    hist_data = [final_portfolio_values]
    fig.add_trace(
        go.Histogram(
            x=final_portfolio_values,
            nbinsx=50,
            marker_color='blue',
            opacity=0.75,
            showlegend=False
        ),
        row=1,
        col=2
    )
    mean_value = np.mean(final_portfolio_values)
    var_95 = np.percentile(final_portfolio_values, 5)

    # Add mean and VaR lines
    fig.add_vline(x=mean_value, line=dict(color='red', dash='dash'), row=1, col=2)
    fig.add_vline(x=var_95, line=dict(color='green', dash='dash'), row=1, col=2)

    fig.update_xaxes(title_text='Final Portfolio Value ($)', row=1, col=2)
    fig.update_yaxes(title_text='Frequency', row=1, col=2)

    fig.update_layout(height=500, width=1000)

    st.plotly_chart(fig)

def get_simulation_insights(sim_results, initial_investment):
    mean_return = np.mean(sim_results)
    median_return = np.median(sim_results)
    std_dev = np.std(sim_results)
    percentile_5 = np.percentile(sim_results, 5)
    var_95 = initial_investment - percentile_5  # VaR at 95% confidence
    cvar_95 = initial_investment - np.mean(sim_results[sim_results <= percentile_5])
    prob_loss = np.mean(sim_results < initial_investment) * 100
    sharpe_ratio = (mean_return - initial_investment) / std_dev  # Assuming risk-free rate is 0

    insights = {
        'Initial Investment': f"${initial_investment:,.2f}",
        'Expected Final Portfolio Value': f"${mean_return:,.2f}",
        'Median Final Portfolio Value': f"${median_return:,.2f}",
        'Standard Deviation of Final Portfolio Value': f"${std_dev:,.2f}",
        'Value at Risk (VaR 95%)': f"${var_95:,.2f}",
        'Conditional Value at Risk (CVaR 95%)': f"${cvar_95:,.2f}",
        'Probability of Loss': f"{prob_loss:.2f}%",
        'Sharpe Ratio': f"{sharpe_ratio:.4f}"
    }
    return insights

def display_optimal_weights(tickers, weights, streamlit_display=False):
    weights_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})
    weights_df['Weight'] = weights_df['Weight'].map("{:.4f}".format)
    if streamlit_display:
        st.table(weights_df)
    else:
        print(weights_df)
