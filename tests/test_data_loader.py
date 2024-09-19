import unittest
from portfolio_management.data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data_loader = DataLoader()
        data = data_loader.load_data(['AAPL'], '2020-01-01', '2020-12-31')
        self.assertFalse(data.empty, "Data should not be empty")

if __name__ == '__main__':
    unittest.main()
