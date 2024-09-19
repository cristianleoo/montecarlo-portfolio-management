import pandas as pd

class Portfolio:
    def __init__(self, price_data):
        self.price_data = price_data
        self.returns = None

    def calculate_returns(self):
        self.returns = self.price_data.pct_change().dropna()
