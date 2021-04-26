from dataclasses import dataclass


@dataclass
class ProductData:
    id: str
    name: str
    category: str
    price: float