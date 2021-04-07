import datetime
from dataclasses import dataclass
from Backend.Domain.TradingSystem.Interfaces.IPurchaseDetails import IPurchaseDetails
from Backend.response import Response, Parsable


@dataclass
class PurchaseDetails(IPurchaseDetails):
        user_name : str
        store_name : str
        product_names : list[str]
        date : datetime
        total_price : float
