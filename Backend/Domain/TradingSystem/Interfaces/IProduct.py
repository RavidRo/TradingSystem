from abc import abstractmethod

from Backend.response import Parsable


class IProduct(Parsable):
    @abstractmethod
    def __init__(self, product_name: str, category, price: float):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_name: str, category: str, price: float):
        """Edit product's details with received product_info"""
        raise NotImplementedError
