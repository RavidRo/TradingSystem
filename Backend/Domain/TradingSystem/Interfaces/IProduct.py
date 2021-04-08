from abc import ABC, abstractmethod

from Backend.response import Response, ParsableList, Parsable


class IProduct(Parsable, metaclass=ABC):

    @abstractmethod
    def __init__(self, product_name: str, price: float, qunatity: int):
        """Create a new store with it's specified info"""
        raise NotImplementedError

    @abstractmethod
    def edit_product_details(self, product_name: str, price: float):
        """Edit product's details with received product_info"""
        raise NotImplementedError