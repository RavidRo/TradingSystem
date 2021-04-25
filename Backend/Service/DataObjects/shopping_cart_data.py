from typing import List

from Backend.Service.DataObjects.shopping_bag_data import ShoppingBagData
from dataclasses import dataclass


@dataclass
class ShoppingCartData:
    bags: List[ShoppingBagData]
