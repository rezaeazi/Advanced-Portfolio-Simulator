import yfinance as yf
from abc import ABC, abstractmethod

class Asset(ABC):
    
    def __init__(self, ticker: str, quantity: float, purchase_price: float):
        self._ticker = ticker.upper()
        self._quantity = quantity
        self._purchase_price = purchase_price
        self._current_price = 0.0
        
    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @property
    def current_price(self) -> float:
        return self._current_price
    
    @current_price.setter
    def current_price(self, new_price: float):
        if new_price >= 0:
            self._current_price = new_price
        else:
            raise ValueError("Current price cannot be negative.")

    @abstractmethod
    def fetch_current_price(self):
        pass
    
    def calculate_current_value(self) -> float:
        return self.current_price * self.quantity

    def calculate_gain_percent(self) -> float:
        if self.purchase_price == 0:
            return 0
        gain = self.current_price - self.purchase_price
        return (gain / self.purchase_price) * 100

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'ticker': self._ticker,
            'quantity': self._quantity,
            'purchase_price': self._purchase_price,
        }

class Stock(Asset):
    def fetch_current_price(self):
        try:
            stock_info = yf.Ticker(self.ticker)
            price = stock_info.history(period="1d")['Close'].iloc[-1]
            self.current_price = round(price, 2)
        except Exception as e:
            self.current_price = self.purchase_price

class Crypto(Asset):
    def fetch_current_price(self):
        crypto_ticker = f"{self.ticker}-USD"
        try:
            crypto_info = yf.Ticker(crypto_ticker)
            price = crypto_info.history(period="1d")['Close'].iloc[-1]
            self.current_price = round(price, 4)
        except Exception as e:
            self.current_price = self.purchase_price
            
    def calculate_network_fee(self, amount: float) -> float:
        return amount * 0.005