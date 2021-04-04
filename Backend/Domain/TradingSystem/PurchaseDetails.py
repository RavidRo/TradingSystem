import datetime
from dataclasses import dataclass
from Backend.Domain.TradingSystem.Interfaces.IPurchaseDetails import IPurchaseDetails
from Backend.response import Response


@dataclass
class PurchaseDetails(IPurchaseDetails):
    def __init__(self, user_name: str, store_name: str, products: list, date: datetime, total_price: float):
        self.user_name = user_name
        self.products = products
        self.store_name = store_name
        self.date = date
        self.total_price = total_price
