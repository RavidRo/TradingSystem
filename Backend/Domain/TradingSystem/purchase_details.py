import datetime
from dataclasses import dataclass

from typing import List


@dataclass
class PurchaseDetails:
    username: str
    store_name: str
    store_id: str
    product_names: List[str]
    date: datetime
    total_price: float
