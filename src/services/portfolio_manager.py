from typing import List
import json
import os
from src.models.asset_classes import Asset, Stock, Crypto

DATA_FILE = 'portfolio_data.json'

class Portfolio:
    def __init__(self):
        self._assets: List[Asset] = []

    def add_asset(self, asset: Asset):
        self._assets.append(asset)

    def update_all_prices(self):
        for asset in self._assets:
            asset.fetch_current_price()

    def get_total_value(self) -> float:
        total = sum(asset.calculate_current_value() for asset in self._assets)
        return round(total, 2)

    def calculate_total_gain(self) -> float:
        total_current = self.get_total_value()
        total_paid = sum(asset.purchase_price * asset.quantity for asset in self._assets)
        return round(total_current - total_paid, 2)

    def get_portfolio_summary(self) -> List[dict]:
        summary = []
        total_value = self.get_total_value()
        
        for asset in self._assets:
            current_value = asset.calculate_current_value()
            summary.append({
                'Ticker': asset.ticker,
                'Quantity': asset.quantity,
                'Purchase Price': asset.purchase_price,
                'Current Price': asset.current_price,
                'Current Value': current_value,
                'Gain/Loss (%)': round(asset.calculate_gain_percent(), 2),
                'Weight (%)': round((current_value / total_value) * 100, 2) if total_value else 0
            })
        return summary

    def get_assets(self) -> List[Asset]:
        return self._assets

    def save_portfolio(self):
        data = [asset.to_dict() for asset in self._assets]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def load_portfolio(self):
        if not os.path.exists(DATA_FILE):
            return False
            
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return False
        
        self._assets = []
        
        for item in data:
            asset_type = item.pop('type')
            
            if asset_type == 'Stock':
                asset = Stock(**item)
            elif asset_type == 'Crypto':
                asset = Crypto(**item)
            else:
                continue
                
            self._assets.append(asset)
            
        return True