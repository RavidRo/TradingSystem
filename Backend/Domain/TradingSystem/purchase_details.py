from Backend.response import Parsable
import datetime
from dataclasses import dataclass

from typing import List


@dataclass
class PurchaseDetails(Parsable):
    username: str
    store_name: str
    store_id: str
    product_names: List[str]
    date: datetime
    total_price: float

    def parse(self):
        return PurchaseDetailsData(self.username, self.store_name, self.store_id, self.product_names, self.date, self.total_price)


@dataclass
class PurchaseDetailsData:
    username: str
    store_name: str
    store_id: str
    product_names: List[str]
    date: datetime
    total_price: float