from dataclasses import dataclass


@dataclass
class ProductData:
    id: str
    name: str
    price: float