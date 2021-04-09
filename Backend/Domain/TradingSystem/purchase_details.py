import datetime
from dataclasses import dataclass


@dataclass
class PurchaseDetails:
    user_name: str
    store_name: str
    product_names: list
    date: datetime
    total_price: float
