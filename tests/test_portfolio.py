import unittest
from unittest.mock import patch
from src.models.asset_classes import Stock, Crypto
from src.services.portfolio_manager import Portfolio

class TestAssetLogic(unittest.TestCase):
    
    def test_stock_gain_calculation(self):
        stock = Stock(ticker="TEST", quantity=10, purchase_price=100.0)
        stock.current_price = 120.0 
        self.assertAlmostEqual(stock.calculate_gain_percent(), 20.0, places=2)
        
        stock.current_price = 80.0
        self.assertAlmostEqual(stock.calculate_gain_percent(), -20.0, places=2)

    def test_price_validation(self):
        stock = Stock(ticker="ERR", quantity=1, purchase_price=10)
        with self.assertRaises(ValueError):
            stock.current_price = -100

class TestPortfolioManager(unittest.TestCase):
    
    def setUp(self):
        self.stock_patcher = patch.object(Stock, 'fetch_current_price', lambda self: setattr(self, '_current_price', 150.00))
        self.crypto_patcher = patch.object(Crypto, 'fetch_current_price', lambda self: setattr(self, '_current_price', 60000.00))
        
        self.stock_patcher.start()
        self.crypto_patcher.start()
        
        self.portfolio = Portfolio()
        self.stock1 = Stock(ticker="GOOG", quantity=2, purchase_price=100.0)
        self.crypto1 = Crypto(ticker="BTC", quantity=0.1, purchase_price=50000.0)
        self.portfolio.add_asset(self.stock1)
        self.portfolio.add_asset(self.crypto1)
        self.portfolio.update_all_prices()

    def tearDown(self):
        self.stock_patcher.stop()
        self.crypto_patcher.stop()

    def test_total_value_calculation(self): 
        expected_total = 6300.00
        self.assertAlmostEqual(self.portfolio.get_total_value(), expected_total, places=2)

    def test_total_gain_calculation(self): 
        expected_gain = 1100.00
        self.assertAlmostEqual(self.portfolio.calculate_total_gain(), expected_gain, places=2)