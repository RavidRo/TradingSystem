from dataclasses import dataclass

from typing import Dict


@dataclass
class ShoppingBagData:
    store_id: str
    store_name: str
    product_ids_to_quantities: Dict[str, int]