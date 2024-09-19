import matplotlib.pyplot as plt
import numpy as np

def plot_simulation_results(sim_results):
    plt.figure(figsize=(10, 6))
    plt.plot(sim_results)
    plt.title('Monte Carlo Simulation Results')
    plt.xlabel('Time Horizon')
    plt.ylabel('Cumulative Returns')
    plt.show()
