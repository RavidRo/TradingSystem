from dataclasses import dataclass


@dataclass
class ShoppingBagData:
    store_name: str
    product_ids_to_quantities: dict[str, int]